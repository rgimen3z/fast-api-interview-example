from datetime import date, datetime
from enum import Enum

import crud
from database import SessionLocal


class TransactionType(Enum):
    SALE = "SALE"
    REFUND = "REFUND"


class SettlementCalculator:
    """
    Calculate settlement from data in our DB, does not reach out to ACME's old API.
    """

    def __init__(self, merchant_id, db: SessionLocal):
        self.merchant_id = merchant_id
        self.db = db

    def calculate_settlement_for_date(self, given_date: date = date.today()):

        # Get all transactions by merchant.
        all_merchant_txns = crud.get_all_transactions_for_merchant_id(db=self.db, merchant_id=self.merchant_id)

        settlement_amount = 0

        # Filter them by date.
        merchant_txns_on_or_before_date = [
            txn for txn in all_merchant_txns
            if datetime.strptime(txn.created_at, "%Y-%m-%dT%H:%M:%SZ").date() <= given_date
        ]
        for txn in merchant_txns_on_or_before_date:
            if txn.type == TransactionType.SALE.value:
                settlement_amount += txn.amount
            elif txn.type == TransactionType.REFUND.value:
                settlement_amount -= txn.amount
            else:
                raise ValueError(f"Found unexpected transaction type for txn id: {txn.id}")

        return settlement_amount


if __name__ == "__main__":
    sc = SettlementCalculator("03338d50-87d3-476c-a3a2-60c5edb1f96e", SessionLocal())
    print(sc.calculate_settlement_for_date(date.today()))

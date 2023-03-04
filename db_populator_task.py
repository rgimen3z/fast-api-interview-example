from acme_api import AcmeAPI
from crud import create_transaction, create_merchant

from database import SessionLocal
from schemas import TransactionCreate, MerchantCreate


class DBPopulatorTask:
    """
    This could be an Airflow task or something similar that runs periodically
    to backfill our DB with data from Acme.
    """

    def __init__(self, acme_api: AcmeAPI, db: SessionLocal):
        self.acme_api = acme_api
        self.db = db

    def populate_transactions(self):
        next_page = 1
        while next_page is not None:
            response = self.acme_api.get_all_transactions(page_number=next_page)

            for result in response.get("results", []):
                transaction = TransactionCreate(
                    id=result.get("id"),
                    created_at=result.get("created_at"),
                    updated_at=result.get("updated_at"),
                    amount=result.get("amount"),
                    type=result.get("type"),
                    customer_id=result.get("customer"),
                    merchant_id=result.get("merchant"),
                    order_id=result.get("order"),
                )
                try:
                    create_transaction(db=self.db, transaction=transaction)
                finally:
                    self.db.close()

            next_page = response.get("next")
            if next_page is not None:
                next_page = next_page.rsplit("page=")[1]  # TODO: this feels hacky, figure out better way.

    def populate_merchants(self):
        next_page = 1
        while next_page is not None:
            response = self.acme_api.get_all_merchants(page_number=next_page)

            for result in response.get("results", []):
                merchant = MerchantCreate(
                    id=result.get("id"),
                    created_at=result.get("created_at"),
                    updated_at=result.get("updated_at"),
                    name=result.get("name"),
                )
                try:
                    create_merchant(db=self.db, merchant=merchant)
                finally:
                    self.db.close()

            next_page = response.get("next")
            if next_page is not None:
                next_page = next_page.rsplit("page=")[1]  # TODO: this feels hacky, figure out better way.


if __name__ == "__main__":
    db_populator_task = DBPopulatorTask(AcmeAPI(), SessionLocal())
    db_populator_task.populate_transactions()
    db_populator_task.populate_merchants()

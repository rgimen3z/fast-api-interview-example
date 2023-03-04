from sqlalchemy.orm import Session

import models
import schemas


def get_merchant(db: Session, merchant_id: str):
    return db.query(models.Merchant).filter(models.Merchant.id == merchant_id).first()


def get_merchants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Merchant).offset(skip).limit(limit).all()


def create_merchant(db: Session, merchant: schemas.MerchantCreate):
    merchant_already_exists = get_merchant(db=db, merchant_id=merchant.id) is not None

    if merchant_already_exists:
        # TODO: update prints to log.info/log.debug
        print(f"Skipped creating merchant with id {merchant.id} because it already exists in our DB!")
        return None

    db_merchant = models.Merchant(
        id=merchant.id,
        created_at=merchant.created_at,
        updated_at=merchant.updated_at,
        name=merchant.name,
    )
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant


def get_transaction(db: Session, transaction_id: str):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    txn_already_exists = get_transaction(db=db, transaction_id=transaction.id) is not None

    if txn_already_exists:
        # TODO: update prints to log.info/log.debug
        print(f"Skipped creating txn with id {transaction.id} because it already exists in our DB!")
        return None

    db_transaction = models.Transaction(
        id=transaction.id,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        amount=transaction.amount,
        type=transaction.type,
        customer_id=transaction.customer_id,
        merchant_id=transaction.merchant_id,
        order_id=transaction.order_id,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_all_transactions_for_merchant_id(db: Session, merchant_id: str):
    merchant = get_merchant(db=db, merchant_id=merchant_id)
    return merchant.transactions

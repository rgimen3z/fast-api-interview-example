from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    created_at = Column(String)
    updated_at = Column(String)
    amount = Column(Float)
    type = Column(String)
    customer_id = Column(String)
    merchant_id = Column(String, ForeignKey("merchants.id"))
    order_id = Column(String)

    merchant = relationship("Merchant", back_populates="transactions")


class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(String, primary_key=True)
    created_at = Column(String)
    updated_at = Column(String)
    name = Column(String)

    transactions = relationship("Transaction", back_populates="merchant")

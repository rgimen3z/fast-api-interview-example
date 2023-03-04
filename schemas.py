from pydantic import BaseModel


class TransactionBase(BaseModel):
    id: str
    created_at: str
    updated_at: str
    amount: float
    type: str
    customer_id: str
    merchant_id: str
    order_id: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    class Config:
        orm_mode = True


class MerchantBase(BaseModel):
    id: str
    created_at: str
    updated_at: str
    name: str


class MerchantCreate(MerchantBase):
    pass


class Merchant(MerchantBase):
    class Config:
        orm_mode = True

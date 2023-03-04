from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import models
import schemas
from acme_api import AcmeAPI
from database import SessionLocal, engine
from settlement_calculator import SettlementCalculator

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

acme_api = AcmeAPI()


# Dependency.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/merchants/", response_model=list[schemas.Merchant])
async def get_merchants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    merchants = crud.get_merchants(db, skip, limit)
    return merchants


@app.get("/settlement/{merchant_id}")
async def get_merchant_settlement_for_date(
        merchant_id: str,
        date_str: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """
    By default, include all transactions up to current date in settlement calculation.
    """
    if date_str is None:
        given_date = datetime.now().date()
    else:
        given_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    settlement_calculator = SettlementCalculator(merchant_id, db)
    settlement_amount = settlement_calculator.calculate_settlement_for_date(given_date)

    return {"settlement": {"merchant_id": merchant_id, "date": str(given_date), "amount": settlement_amount}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

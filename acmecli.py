import click
from database import SessionLocal
from datetime import datetime, date
from crud import get_merchants
from settlement_calculator import SettlementCalculator

db = SessionLocal()


@click.group()
def acmecli():
    pass


@click.command()
def get_all_merchants():
    all_merchants = get_merchants(db)
    for merchant in all_merchants:
        click.echo(merchant.name)


@click.command()
@click.option("--as-of", default=str(date.today()))
@click.argument("merchant_id")
def get_settlement_for_merchant(as_of, merchant_id):
    if as_of is None:
        given_date = datetime.now().date()
    else:
        given_date = datetime.strptime(as_of, "%Y-%m-%d").date()

    settlement_calculator = SettlementCalculator(merchant_id, db)
    settlement_amount = settlement_calculator.calculate_settlement_for_date(given_date)

    click.echo(settlement_amount)


acmecli.add_command(get_all_merchants)
acmecli.add_command(get_settlement_for_merchant)


if __name__ == "__main__":
    acmecli()

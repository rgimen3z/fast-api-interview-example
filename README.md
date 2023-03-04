## Summary
Create a service that integrates with Acme Payments core API to retrieve data, process it and expose
a settlement endpoint which can be used to determine the settlement amount for a merchant on a given date.


## Design
FastApi + SQLite DB

One of the constraints given was that the current ACME core API is slow and randomly fails, so we're going to run
a task to store a copy of the data in-house. This task could be something like an Airflow task that runs periodically.
The backfilled data will get stored in our own SQLite DB.


## Setup
This already assumes you're using MacOS/Linux and have python3.9 installed.

From the home directory for this project: 
- Create venv (feel free to pick a different name): python3.9 -m venv venv
- Activate venv: source venv/bin/activate
- Install requirements: pip install -r requirements.txt


## Backfilling data


Going forward, we don't need to backfill every single transaction and merchant, just
the ones updated since the the last backfill (query for the last udpdated row in our DB to figure out last
backfill date)
- To run the initial backfill: python -m db_populator_task


## Running our server
Our server will calculate settlements per merchant and return them to us by querying our in-house
DB directly, which has already been backfilled in the previous step.

Problem: we need to make sure all the data up to the requested settlement_date has been properly
backfilled before returning to the user.
Solution: need to better understand the use case. If we need to support the latest transactions coming
from the old Acme API, we may need to query from both our DB and the Acme API and combine the data

- To run our server in "dev" mode: uvicorn main:app --reload


## Getting a settlement amount for a merchant and a date
With the server running, go to http://127.0.0.1:8000/settlement and pass in a merchant_id

Date defaults to current day:
Example: http://127.0.0.1:8000/settlement/03338d50-87d3-476c-a3a2-60c5edb1f96e
Response: {"settlement":{"merchant_id":"03338d50-87d3-476c-a3a2-60c5edb1f96e","date":"2023-03-03","amount":186540.16999999998}}

If date_str is passed as a query param, transactions are filtered:
Example: http://127.0.0.1:8000/settlement/03338d50-87d3-476c-a3a2-60c5edb1f96e?date_str=2022-12-25
{"settlement":{"merchant_id":"03338d50-87d3-476c-a3a2-60c5edb1f96e","date":"2022-12-25","amount":18034.559999999998}}


## Using the cli
Learn about available commands: python -m acmecli
> Usage: python -m acmecli [OPTIONS] COMMAND [ARGS]...
>
> Options:
  --help  Show this message and exit.
>
>Commands:
>  get-all-merchants
>  get-settlement-for-merchant


Calculate settlement amount for merchant by id and date:
python -m acmecli get-settlement-for-merchant 03338d50-87d3-476c-a3a2-60c5edb1f96e
> 186540.16999999998


## Future improvements:
- Use a Docker container to avoid issues with OS and python version
- Host the service online in AWS Free tier, fly.io, etc.

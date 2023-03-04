from json import JSONDecodeError

import backoff
import requests


def fatal_code(e):
    if isinstance(e, JSONDecodeError):
        return False
    return 400 <= e.response.status_code < 500


class AcmeAPI:
    def __init__(self):
        self.base_url = "https://api-engine-dev.clerq.io/tech_assessment"

    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, JSONDecodeError), max_tries=10, giveup=fatal_code)
    def get_all_merchants(self, page_number: 1):
        full_url = "/".join([self.base_url, "merchants"])
        params = {"page": page_number, "ordering": "updated_at"}

        response = requests.get(full_url, params=params)
        res = response.json()

        return res

    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException, JSONDecodeError), max_tries=10, giveup=fatal_code)
    def get_all_transactions(self, page_number: 1):
        full_url = "/".join([self.base_url, "transactions"])
        params = {"page": page_number, "ordering": "updated_at"}

        response = requests.get(full_url, params=params)
        res = response.json()

        return res


# TESTS
if __name__ == "__main__":
    acme_api = AcmeAPI()
    # print(acme_api.get_merchants())
    acme_api.get_all_transactions()

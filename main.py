"""Countries CLI — explore country data from the countries.dev API."""

import sys

import requests

BASE_URL = "https://countries.dev/countries"


def fetch_countries(url=BASE_URL, params=None, timeout=10):
    """Fetch the country list from the API.

    Returns the parsed JSON list, or None if the request fails.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error: could not fetch data from the API ({error})")
        return None


def main():
    print("Fetching country data from countries.dev ...")
    countries = fetch_countries()
    if countries is None:
        sys.exit(1)
    print(f"Loaded {len(countries)} countries.")


if __name__ == "__main__":
    main()
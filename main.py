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


def parse_countries(raw_countries):
    """Reduce raw API records to the fields the CLI needs.

    Uses .get() with defaults so records missing a field (e.g. a
    territory with no capital) do not crash the program.
    """
    countries = []
    for record in raw_countries:
        countries.append({
            "name": record.get("name", "Unknown"),
            "capital": record.get("capital") or "N/A",
            "region": record.get("region") or "N/A",
            "population": record.get("population") or 0,
            "area": record.get("area") or 0,
            "density": record.get("populationDensity") or 0,
        })
    return countries


def main():
    print("Fetching country data from countries.dev ...")
    raw_countries = fetch_countries()
    if raw_countries is None:
        sys.exit(1)
    countries = parse_countries(raw_countries)
    print(f"Loaded {len(countries)} countries.")


if __name__ == "__main__":
    main()
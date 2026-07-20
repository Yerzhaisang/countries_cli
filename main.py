"""Countries CLI — explore country data from the countries.dev API.

Fetches all countries once at startup, then lets the user filter by
region, compare two countries side by side, or rank countries by
population from an interactive menu.
"""

import sys

import requests

BASE_URL = "https://countries.dev/countries"


# --- API integration ---

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


# --- Data transformation ---

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


# --- Processing ---

def filter_by_region(countries, region):
    """Return countries whose region matches, case-insensitively."""
    region = region.lower()
    return [c for c in countries if c["region"].lower() == region]


def find_country(countries, name):
    """Return the country whose name matches case-insensitively, or None."""
    name = name.lower()
    for country in countries:
        if country["name"].lower() == name:
            return country
    return None


def top_by_population(countries, count):
    """Return the `count` most populous countries, largest first."""
    ranked = sorted(countries, key=lambda c: c["population"], reverse=True)
    return ranked[:count]


def available_regions(countries):
    """Return the sorted region names present in the data."""
    return sorted({c["region"] for c in countries if c["region"] != "N/A"})


# --- Display ---

def display_table(countries):
    """Print countries as an aligned table."""
    print(f"\n{'Name':<36} {'Capital':<22} {'Population':>12} {'Area (km2)':>12}")
    print("-" * 85)
    for c in countries:
        print(f"{c['name'][:35]:<36} {c['capital'][:21]:<22} "
              f"{c['population']:>12,} {c['area']:>12,.0f}")
    print(f"\n{len(countries)} countries shown.\n")


def display_comparison(country_a, country_b):
    """Print two countries side by side, one attribute per row."""
    rows = [
        ("Region", "region", "{}"),
        ("Capital", "capital", "{}"),
        ("Population", "population", "{:,}"),
        ("Area (km2)", "area", "{:,.0f}"),
        ("People per km2", "density", "{:,.1f}"),
    ]
    print(f"\n{'':<16} {country_a['name'][:24]:<26} {country_b['name'][:24]:<26}")
    print("-" * 68)
    for label, key, fmt in rows:
        print(f"{label:<16} {fmt.format(country_a[key]):<26} "
              f"{fmt.format(country_b[key]):<26}")
    print()


# --- Menu handlers ---

def handle_filter(countries):
    """Ask for a region and list its countries."""
    region = input("Enter a region name (e.g. Asia, Europe): ").strip()
    if not region:
        print("Please enter a region name.\n")
        return
    matches = filter_by_region(countries, region)
    if not matches:
        print(f"No countries found in '{region}'. "
              f"Available regions: {', '.join(available_regions(countries))}\n")
        return
    display_table(matches)


def handle_compare(countries):
    """Ask for two country names and show them side by side."""
    name_a = input("First country name: ").strip()
    name_b = input("Second country name: ").strip()
    if not name_a or not name_b:
        print("Please enter both country names.\n")
        return
    country_a = find_country(countries, name_a)
    country_b = find_country(countries, name_b)
    for name, found in ((name_a, country_a), (name_b, country_b)):
        if found is None:
            print(f"No country named '{name}' found. Check the spelling and try again.")
    if country_a is None or country_b is None:
        print()
        return
    display_comparison(country_a, country_b)


def handle_top(countries):
    """Ask for N and show the N most populous countries."""
    raw_count = input("How many countries to show? ").strip()
    try:
        count = int(raw_count)
    except ValueError:
        print(f"'{raw_count}' is not a whole number.\n")
        return
    if count < 1:
        print("Please enter a number of 1 or more.\n")
        return
    display_table(top_by_population(countries, count))


MENU = """\
1. Filter countries by region
2. Compare two countries
3. Top N countries by population
4. Quit
"""


def main():
    print("Fetching country data from countries.dev ...")
    raw_countries = fetch_countries()
    if raw_countries is None:
        sys.exit(1)
    countries = parse_countries(raw_countries)
    print(f"Loaded {len(countries)} countries.\n")

    handlers = {"1": handle_filter, "2": handle_compare, "3": handle_top}
    while True:
        print(MENU)
        try:
            choice = input("Choose an option (1-4): ").strip()
            if choice == "4":
                print("Goodbye!")
                break
            handler = handlers.get(choice)
            if handler is None:
                print(f"'{choice}' is not a menu option. Enter 1, 2, 3 or 4.\n")
                continue
            handler(countries)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
# Project Plan — Countries CLI

## What the tool will do

A user runs the program and sees a numbered menu with three options:
(1) filter countries by region, (2) compare two countries side by side, or
(3) show the top N most populous countries. The tool fetches all countries
from the countries.dev API once at startup. For option 1, the user enters a
region name (e.g., "Asia") and the tool prints each matching country's name,
capital, population, and area in an aligned table. For option 2, the user
enters two country names and the tool prints their region, capital,
population, area, and population density side by side. For option 3, the
user enters a number N and the tool prints the N most populous countries
ranked. If the API request fails due to a network error or bad status code,
the program prints a clear error message and exits gracefully instead of
showing a traceback. If the user enters an empty string, an unknown region
or country name, or a non-numeric value for N, the program prints a helpful
message and returns to the menu. Countries missing a field (such as capital)
are displayed with "N/A" rather than crashing the program.

## API exploration notes (Step 2)

1. **Top-level shape:** the response is a JSON list of country objects
   (not a dict wrapping a list).
2. **Fields per record:** name, capital, region, subregion, population,
   area, populationDensity, languages, currencies, flags, maps, timezones,
   borders, translations, and more.
3. **Nested fields:** `maps`, `flags`, and `translations` are dicts inside
   dicts; `languages`, `currencies`, and `regionalBlocs` are lists of dicts;
   `timezones`, `borders`, and `latlng` are lists of plain values.
4. **Missing fields:** not every record has every key — some territories
   lack `borders`, `gini`, or `cioc`, and a few records have no `capital`.
   The code must use `.get()` with defaults to avoid KeyError crashes.

## Rubric self-check

- Uses 6 fields from the API: name, capital, region, population, area,
  populationDensity.
- Three interaction modes: filter, comparison, ranking.
- Error cases handled: network failure, empty input, unknown region or
  country, non-numeric N, missing fields.
- Structure: fetching, parsing, processing, and display live in separate
  functions; `main()` only wires them together.
# Countries CLI

A command-line tool for exploring country data from the
[countries.dev](https://countries.dev/docs) API. Built as the pre-work
assignment for Code the Dream's *Python for Data Analysis* course.

## What it does

The tool fetches all 250 countries once at startup, then shows an
interactive menu with three modes:

1. **Filter by region** — enter a region name (e.g. `Asia`) and get an
   aligned table of every country in it with name, capital, population,
   and area.
2. **Compare two countries** — enter two country names and see their
   region, capital, population, area, and population density side by side.
3. **Top N by population** — enter a number and get the N most populous
   countries, ranked.

Matching is case-insensitive. Fields used from the API: `name`,
`capital`, `region`, `population`, `area`, `populationDensity`.

## Error handling

- Network errors and bad status codes are caught with `try/except`; the
  program prints a clear message and exits instead of showing a traceback.
- Empty input, unknown regions or country names, and non-numeric values
  print a helpful message and return to the menu.
- Records missing a field (e.g. Antarctica has no capital) display `N/A`
  via `.get()` defaults instead of crashing.

## How to run

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Project structure

- `main.py` — all code, organized into separate functions for fetching
  (`fetch_countries`), transformation (`parse_countries`), processing
  (`filter_by_region`, `find_country`, `top_by_population`), display
  (`display_table`, `display_comparison`), and menu handling.
- `PLAN.md` — the project plan and API exploration notes written before
  coding.
- `requirements.txt` — the single dependency, `requests`.
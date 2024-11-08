#!/usr/bin/python
"""
Create a Markdown table of countries visited by the Transcontinental Race
and write to README.md.

python tcr_countries.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
from collections import Counter

from prettytable import PrettyTable, TableStyle

# from pprint import pprint
# from rich import print

EDITIONS = {
    "10. 2024": [
        "FR",
        "BE",
        "NL",
        "DE",
        "LU",
        "CH",
        "AT",
        "IT",
        "SI",
        "HR",
        "LI",
        "BA",
        "ME",
        "RS",
        "XK",
        "MK",
        "GR",
        "BG",
        "TR",
        "AL",
    ],
    "9. 2023": [
        "BE",
        "FR",
        "LU",
        "DE",
        "CH",
        "LI",
        "IT",
        "AT",
        "SI",
        "HR",
        "BA",
        "ME",
        "AL",
        "MK",
        "GR",
        "RS",
        "XK",
    ],
    "8. 2022": [
        "BE",
        "NL",
        "DE",
        "CZ",
        "AT",
        "IT",
        "CH",
        "SI",
        "HR",
        "BA",
        "ME",
        "RS",
        "RO",
        "BG",
    ],
    "7. 2019": ["BG", "RS", "HR", "XK", "BA", "SI", "AT", "IT", "LI", "CH", "FR", "HU"],
    "6. 2018": [
        "BE",
        "FR",
        "NL",
        "DE",
        "LU",
        "CH",
        "LI",
        "AT",
        "IT",
        "SI",
        "CZ",
        "PL",
        "HU",
        "HR",
        "BA",
        "SK",
        "ME",
        "AL",
        "GR",
        "MK",
        "RS",
        "XK",
    ],
    "5. 2017": [
        "BE",
        "FR",
        "NL",
        "DE",
        "LU",
        "AT",
        "CH",
        "LI",
        "IT",
        "SI",
        "HU",
        "SK",
        "RO",
        "HR",
        "UA",
        "BG",
        "RS",
        "MK",
        "GR",
    ],
    "4. 2016": [
        "BE",
        "FR",
        "CH",
        "IT",
        "SI",
        "HR",
        "BA",
        "ME",
        "AT",
        "RS",
        "BG",
        "XK",
        "TR",
        "LI",
        "MK",
        "GR",
        "AL",
    ],
    "3. 2015": [
        "BE",
        "FR",
        "IT",
        "SI",
        "HR",
        "BA",
        "ME",
        "AL",
        "RS",
        "MK",
        "BG",
        "XK",
        "TR",
        "GR",
    ],
    "2. 2014": [
        "GB",
        "FR",
        "CH",
        "IT",
        "DE",
        "AT",
        "LI",
        "SI",
        "HR",
        "BA",
        "ME",
        "RS",
        "AL",
        "BG",
        "MK",
        "TR",
        "XK",
    ],
    "1. 2013": [
        "GB",
        "FR",
        "BE",
        "LU",
        "CH",
        "DE",
        "IT",
        "AT",
        "SI",
        "HR",
        "RS",
        "BG",
        "TR",
        "AL",
        "MK",
        "GR",
    ],
}
editions_type = dict[str, list[str]]
editions_list_type = list[list[str]]

FLAG = "![](https://hugovk.github.io/flag-icon/png/16/country-4x3/{}.png)"


def timestamp() -> str:
    """Create a timestamp and the filename with path"""
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%A, %d %B %Y, %H:%M UTC")
    return f"Last updated {stamp} by {os.path.basename(__file__)}"


def add_total_countries(editions: editions_type) -> editions_type:
    """Append a list that contains all editions' countries, no repeats"""
    all_countries = []
    for countries in editions.values():
        for country in countries:
            if country not in all_countries:
                all_countries.append(country)
    editions["All"] = all_countries

    return editions


def format_countries(editions: editions_type, *, add_flags=False) -> editions_type:
    """Add flag images to countries and italics to very first seen"""
    seen = set()
    for countries in editions.values():
        for i, country in enumerate(countries):
            flag = FLAG.format(country.lower()) + " " if add_flags else ""

            if country not in seen:
                # Italicise
                seen.add(country)
                country = f"*{country}*"

            countries[i] = f"{flag}{country}"

    return editions


def dict_to_list(editions: editions_type) -> editions_list_type:
    """Convert:
    {"1. 2013": ["GB", "FR"], "6. 2018": ["BE", "FR"]}
    into:
    [["1. 2013", "GB, FR"], ["6. 2018", "BE", "FR"]]
    """
    return [[year] + countries for year, countries in editions.items()]


def pad_editions_list(editions: editions_list_type) -> editions_list_type:
    """Given lists of different lengths:
    [["GB", "FR", "TR"], ["BE", "SI"]]
    pad the shorter ones:
    [["GB", "FR", "TR"], ["BE", "SI", "  "]]
    """
    # Find longest list length
    max_length = max(len(edition) for edition in editions)

    # https://stackoverflow.com/a/3438818/724176
    return [edition + ["  "] * (max_length - len(edition)) for edition in editions]


def add_total_index(editions: editions_list_type) -> editions_list_type:
    """Prepend a list like ["", 1, 2, 3, 4]"""
    numbers = [""] + list(range(1, len(editions[0]) + 1))
    editions.insert(0, numbers)
    return editions


def update_readme(new_table: str) -> None:
    with open("README.md") as f:
        contents = f.read()

    before, delim1, remainder = contents.partition(
        "[start_generated]: # (start_generated)\n"
    )
    old_table, delim2, _ = remainder.partition("[end_generated]: # (end_generated)\n")

    if new_table.strip() == old_table.strip():
        print("No changes to README.md")
        return

    output = (
        before + delim1 + "\n" + new_table + "\n\n" + delim2 + "\n" + timestamp() + "\n"
    )

    with open("README.md", "w") as f:
        f.write(output)
    print("README.md updated")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-f", "--no-flag", action="store_true", help="Don't add flag images"
    )
    args = parser.parse_args()

    for year, countries in EDITIONS.items():
        assert len(countries) == len(set(countries)), (
            f"Duplicate countries for {year}: "
            f"{[country for country, count in Counter(countries).items() if count > 1]}"
        )

    editions = dict(reversed(EDITIONS.items()))

    editions = add_total_countries(editions)

    editions = format_countries(editions, add_flags=not args.no_flag)

    editions_list = dict_to_list(editions)

    editions_list = pad_editions_list(editions_list)

    editions_list = add_total_index(editions_list)

    # Rotate list of lists
    editions_list = list(map(list, zip(*editions_list)))

    table = PrettyTable()
    table.set_style(TableStyle.MARKDOWN)
    table.field_names = editions_list[0]
    table.add_rows(editions_list[1:])

    update_readme(table.get_string())


if __name__ == "__main__":
    main()

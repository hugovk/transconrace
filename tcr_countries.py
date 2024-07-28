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

from prettytable import MARKDOWN, PrettyTable

# from pprint import pprint


COUNTRIES = {
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
        "LU",
        "BA",
        "ME",
        "SI",
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


FLAG = "![](https://hugovk.github.io/flag-icon/png/16/country-4x3/{}.png)"


def timestamp() -> str:
    """Create a timestamp and the filename with path"""
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%A, %d %B %Y, %H:%M UTC")
    return f"Last updated {stamp} by {os.path.basename(__file__)}"


def add_total_countries(dict_of_lists):
    """Append a list that contains all year's countries, no repeats"""
    all = []
    for _, countries in dict_of_lists.items():
        for country in countries:
            if country not in all:
                all.append(country)
    dict_of_lists["All"] = all

    return dict_of_lists


def format_countries(dict_of_lists, *, add_flags=False):
    """Add flag images to countries and italics to very first seen"""
    seen = set()
    for _, countries in dict_of_lists.items():
        for i, country in enumerate(countries):
            flag = FLAG.format(country.lower()) + " " if add_flags else ""

            if country not in seen:
                # Italicise
                seen.add(country)
                country = f"*{country}*"

            countries[i] = f"{flag}{country}"

    return dict_of_lists


def dict_of_lists_to_list_of_lists(dict_of_lists):
    """Convert:
    {"1. 2013": ["GB", "FR"], "6. 2018": ["BE", "FR"]}
    into:
    [["1. 2013", "GB, FR"], ["6. 2018", "BE", "FR"]]
    """
    list_of_lists = []

    for year, countries in dict_of_lists.items():
        row = [year] + countries
        list_of_lists.append(row)

    return list_of_lists


def pad_list_of_lists(list_of_lists):
    """Given lists of different lengths:
    [["GB", "FR", "TR"], ["BE", "SI"]]
    pad the shorter ones:
    [["GB", "FR", "TR"], ["BE", "SI", "  "]]
    """
    length = 0
    # Find longest list length
    for list_ in list_of_lists:
        length = max(len(list_), length)

    new = []
    for list_ in list_of_lists:
        # https://stackoverflow.com/a/3438818/724176
        new.append(list_ + ["  "] * (length - len(list_)))

    return new


def add_total_index(list_of_lists):
    """Prepend a list like ["", 1, 2, 3, 4]"""
    numbers = [""] + list(range(1, len(list_of_lists[0]) + 1))
    list_of_lists.insert(0, numbers)
    return list_of_lists


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

    countries = dict(reversed(COUNTRIES.items()))

    countries = add_total_countries(countries)

    countries = format_countries(countries, add_flags=not args.no_flag)

    list_of_lists = dict_of_lists_to_list_of_lists(countries)

    list_of_lists = pad_list_of_lists(list_of_lists)

    list_of_lists = add_total_index(list_of_lists)

    # Rotate list of lists
    list_of_lists = list(map(list, zip(*list_of_lists)))

    table = PrettyTable()
    table.set_style(MARKDOWN)
    table.field_names = list_of_lists[0]
    table.add_rows(list_of_lists[1:])

    update_readme(table.get_string())


if __name__ == "__main__":
    main()

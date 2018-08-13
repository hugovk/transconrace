#!/usr/bin/python

"""
Create a Markdown table of countries visited by the Transcontinental Race.

python tcr_countries.py --flag > README.md
"""
import argparse
import datetime

import pytablewriter  # pip install pytablewriter

# from pprint import pprint


COUNTRIES = {
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
        "RS",
        "XK",
        "MK",
    ],
}


FLAG = "![](https://hugovk.github.io/flag-icon/png/16/country-4x3/{}.png)"


def timestamp():
    """Print a timestamp and the filename with path"""
    stamp = datetime.datetime.utcnow().strftime("%A, %d %B %Y, %H:%M UTC")
    print("Last updated {} by {}".format(stamp, __file__))


def add_total_countries(dict_of_lists):
    """Append a list that contains all year's countries, no repeats"""
    all = []
    for _, countries in dict_of_lists.items():
        for country in countries:
            if country not in all:
                all.append(country)
    dict_of_lists["All"] = all

    return dict_of_lists


def add_flags(dict_of_lists):
    """Add flag images to countries"""
    for _, countries in dict_of_lists.items():
        for i, country in enumerate(countries):
            flag = FLAG.format(country.lower())
            countries[i] = "{} {}".format(flag, country)

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
    for l in list_of_lists:
        length = max(len(l), length)

    new = []
    for l in list_of_lists:
        # https://stackoverflow.com/a/3438818/724176
        new.append(l + ["  "] * (length - len(l)))

    return new


def add_total_index(list_of_lists):
    """Prepend a list like ["", 1, 2, 3, 4]"""
    numbers = [""] + list(range(1, len(list_of_lists[0]) + 1))
    list_of_lists.insert(0, numbers)
    return list_of_lists


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-f", "--flag", action="store_true", help="Add a flag image")
    args = parser.parse_args()

    countries = add_total_countries(COUNTRIES)

    if args.flag:
        countries = add_flags(countries)

    list_of_lists = dict_of_lists_to_list_of_lists(countries)

    list_of_lists = pad_list_of_lists(list_of_lists)
    # pprint(list_of_lists)

    list_of_lists = add_total_index(list_of_lists)

    # Rotate list of lists
    list_of_lists = list(map(list, zip(*list_of_lists)))

    print("# Transcontinental Race")
    print()
    print(
        "Countries the [Transcontinental Race](https://www.transcontinental.cc/)"
        " has collectively visited, roughly in order of first entry.\n"
    )

    writer = pytablewriter.MarkdownTableWriter()
    writer.header_list = list_of_lists[0]
    writer.value_matrix = list_of_lists[1:]
    writer.margin = 1
    writer.write_table()

    timestamp()

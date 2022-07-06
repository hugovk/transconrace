#!/usr/bin/python

"""
List all the countries visited by a GPX track.

python gpx_countries.py route.gpx
"""
import argparse
import glob
import json
import sys

import gpxpy  # # pip install gpxy lxml
import gpxpy.gpx
from shapely.geometry import Point, shape  # pip install shapely
from shapely.prepared import prep

all_results = {}


# https://stackoverflow.com/a/46589405/724176
def get_country(lon, lat):
    point = Point(lon, lat)
    for country, geom in countries.items():
        if geom.contains(point):
            return country

    return "unknown"


def borders_total_unique(visited):
    total = len(visited)
    borders = total - 1
    unique = len(set(visited))
    return borders, total, unique


def process_gpx(filename):
    print(f"Loading GPX: {filename}")
    with open(filename) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    print("Finding countries in GPX")
    visited = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                country = get_country(point.longitude, point.latitude)
                if country == "unknown":
                    continue
                if len(visited) == 0 or country != visited[-1]:
                    new = country not in visited
                    marker = "*" if new else ""
                    visited.append(country)
                    if args.unique:
                        if new:

                            print(f"{len(set(visited)):2d}. {point.time} {country}")
                    else:
                        print(
                            f"{len(visited):2d}. {len(set(visited)):2d}. "
                            f"{point.time} {country}{marker}"
                        )
    borders, total, unique = borders_total_unique(visited)
    print(f"Unique country visits:\t{unique}")
    print(f"Total country visits:\t{total}")
    print(f"Borders crossed:\t{borders}")
    return visited


def is_smaller(new, min, new_name, min_names):
    if new < min:
        min = new
        min_names = [new_name]
    elif new == min:
        min_names.append(new_name)
    return min, min_names


def is_bigger(new, max, new_name, max_names):
    if new > max:
        max = new
        max_names = [new_name]
    elif new == max:
        max_names.append(new_name)
    return max, max_names


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("gpx", help="Input GPX files")
    parser.add_argument(
        "-u", "--unique", action="store_true", help="Only show unique countries"
    )
    args = parser.parse_args()

    filenames = glob.glob(args.gpx)
    print(f"GPX files found:\t{len(filenames)}")
    if not filenames:
        sys.exit(f"No files match {args.gpx}")

    print("Loading countries")
    # https://github.com/datasets/geo-countries
    # All data is licensed under the Open Data Commons Public Domain Dedication and
    # License. Thanks to Natural Earth, Lexman and the Open Knowledge Foundation.
    with open("countries.geojson") as geojson_file:
        data = json.load(geojson_file)

    countries = {}
    for feature in data["features"]:
        geom = feature["geometry"]
        country = feature["properties"]["ADMIN"]
        countries[country] = prep(shape(geom))

    print(f"Countries loaded:\t{len(countries)}")

    for filename in filenames:
        visited = process_gpx(filename)
        all_results[filename] = visited

    if len(all_results) > 1:
        min_borders = sys.maxsize
        min_borders_filenames = []
        min_total_countries = sys.maxsize
        min_total_countries_filenames = []
        min_unique_countries = sys.maxsize
        min_unique_countries_filenames = []
        max_borders = 0
        max_borders_filenames = []
        max_total_countries = 0
        max_total_countries_filenames = []
        max_unique_countries = 0
        max_unique_countries_filenames = []

        for filename, visited in all_results.items():
            borders, total, unique = borders_total_unique(visited)

            max_borders, max_borders_filenames = is_bigger(
                borders, max_borders, filename, max_borders_filenames
            )
            max_total_countries, max_total_countries_filenames = is_bigger(
                total, max_total_countries, filename, max_total_countries_filenames
            )
            max_unique_countries, max_unique_countries_filenames = is_bigger(
                unique, max_unique_countries, filename, max_unique_countries_filenames
            )

            # Some tracks start late or end early
            if "Belgium" not in visited or "Greece" not in visited:
                continue
            min_borders, min_borders_filenames = is_smaller(
                borders, min_borders, filename, min_borders_filenames
            )
            min_total_countries, min_total_countries_filenames = is_smaller(
                total, min_total_countries, filename, min_total_countries_filenames
            )
            min_unique_countries, min_unique_countries_filenames = is_smaller(
                unique, min_unique_countries, filename, min_unique_countries_filenames
            )

        print()
        print(
            f"Most unique country visits:\t"
            f"{max_unique_countries}\t{max_unique_countries_filenames}"
        )
        print(
            f"Most total country visits:\t"
            f"{max_total_countries}\t{max_total_countries_filenames}"
        )
        print(f"Most borders crossed:\t\t{max_borders}\t{max_borders_filenames}")

        print()
        print(
            f"Least unique country visits:\t"
            f"{min_unique_countries}\t{min_unique_countries_filenames}"
        )
        print(
            f"Least total country visits:\t"
            f"{min_total_countries}\t{min_total_countries_filenames}"
        )
        print(f"Least borders crossed:\t\t{min_borders}\t{min_borders_filenames}")

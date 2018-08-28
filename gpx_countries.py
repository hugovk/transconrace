#!/usr/bin/python

"""
List all the countries visited by a GPX track.

python gpx_countries.py route.gpx
"""
import argparse
import glob
import json

import gpxpy  # # pip install gpxy lxml
import gpxpy.gpx
from shapely.geometry import Point, shape  # pip install shapely
from shapely.prepared import prep


# https://stackoverflow.com/a/46589405/724176
def get_country(lon, lat):
    point = Point(lon, lat)
    for country, geom in countries.items():
        if geom.contains(point):
            return country

    return "unknown"


def process_gpx(filename):
    print("Loading GPX: {}".format(filename))
    with open(filename) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    print("Finding countries in GPX")
    visited = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                country = get_country(point.longitude, point.latitude)
                if len(visited) == 0 or country != visited[-1]:
                    new = country not in visited
                    marker = "*" if new else ""
                    visited.append(country)
                    if args.unique:
                        if new:

                            print(
                                "{:2d}. {} {}".format(
                                    len(set(visited)), point.time, country
                                )
                            )
                    else:
                        print(
                            "{:2d}. {:2d}. {} {}{}".format(
                                len(visited),
                                len(set(visited)),
                                point.time,
                                country,
                                marker,
                            )
                        )
    print("Unique country visits:\t{}".format(len(set(visited))))
    print("Total country visits:\t{}".format(len(visited)))
    print("Borders crossed:\t{}".format(len(visited) - 1))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("gpx", help="Input GPX files")
    parser.add_argument(
        "-u", "--unique", action="store_true", help="Only show unique countries"
    )
    args = parser.parse_args()

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

    print("Countries loaded:\t{}".format(len(countries)))

    filenames = glob.glob(args.gpx)
    print("GPX files found:\t{}".format(len(filenames)))

    for filename in filenames:
        process_gpx(filename)

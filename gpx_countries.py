#!/usr/bin/python

"""
List all the countries visited by a GPX track.

python gpx_countries.py route.gpx
"""
import argparse
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("gpx", help="Input GPX file")
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

    print("{} countries loaded".format(len(countries)))

    print("Loading GPX")
    with open(args.gpx) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    print("Finding countries in GPX")
    visited = set()
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                country = get_country(point.longitude, point.latitude)
                if country not in visited:
                    visited.add(country)
                    print("{}. {}".format(len(visited), country))

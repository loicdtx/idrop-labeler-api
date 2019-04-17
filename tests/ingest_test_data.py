#!/usr/bin/env python3

import csv

import fiona

from idb.db import session_scope, init_db
from idb import add_inventories
from idb.models import Tile, Studyarea, Species
from idb.utils import get_or_create


csv_file = 'data/species.csv'
gpkg_file = 'data/test_data.gpkg'


# Create database tables
init_db()

# Ingest species
with open(csv_file) as src:
    reader = csv.reader(src)
    with session_scope() as session:
        for row in reader:
            get_or_create(session=session, model=Species,
                          code=row[0], name=row[1])

# Add tiles
with fiona.open(gpkg_file, layer='tiles') as src:
    tile_list = [Tile.from_geojson(feature) for feature in src]
with session_scope() as session:
    session.add_all(tile_list)

# Add inventory samples
with fiona.open(gpkg_file, layer='inventory') as src:
    with session_scope() as session:
        add_inventories(session, list(src))

# Add study area
with fiona.open(gpkg_file, layer='studyarea') as src:
    studyarea_list = [Studyarea.from_geojson(feature) for feature in src]
with session_scope() as session:
    session.add_all(studyarea_list)


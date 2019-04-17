#!/usr/bin/env bash

dropdb idrop_tests
createdb idrop_tests
psql idrop_tests -c "CREATE EXTENSION postgis;"
psql idrop_tests -c "CREATE EXTENSION postgis_topology;"

./ingest_test_data.py
py.test

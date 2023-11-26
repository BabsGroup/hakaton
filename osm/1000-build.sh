#!/bin/sh

psql -U postgres -d moscow -c "CREATE EXTENSION postgis";

osm2pgsql -U postgres -d moscow -l moscow.osm.pbf
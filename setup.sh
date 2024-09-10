#! /usr/bin/env bash

basedir=$(dirname "$0")
datadir=$basedir/data
sudo cp $datadir/* /var/lib/postgres/data/
psql -d unb-db-2024-1 -f $basedir/generate_database.sql

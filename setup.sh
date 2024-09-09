#! /usr/bin/env bash

basedir=$(dirname "$0")
datadir=$basedir/data
sudo cp $datadir/* /var/lib/postgres/data/

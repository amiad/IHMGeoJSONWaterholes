#!/bin/bash
url="https://docs.google.com/spreadsheets/d/1BbT762qaYilLnwGD7sJDo8sfs_Y5ExjvixS_Tl3rSas/gviz/tq?tqx=out:csv&sheet=IHM"
csv='floods.csv'

pushd $(dirname "$0") > /dev/null
git checkout main
git pull
wget  $url -O $csv
./node_modules/csv2geojson/csv2geojson --lat Latitude --lon Longitude $csv > source.geojson
git add .
git commit source.geojson $csv -m "update source.geojson $(date +%Y-%m-%d-%R)"
git push
popd > /dev/null

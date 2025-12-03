#!/bin/bash

url="https://docs.google.com/spreadsheets/d/1BbT762qaYilLnwGD7sJDo8sfs_Y5ExjvixS_Tl3rSas/export?format=tsv&gid=0&range=A4:M100&headers=0"

tsv="floods.tsv"
csv="floods.csv"
geojson="source.geojson"

# הורדת TSV
wget -O "$tsv" "$url"

# המרה ל‑CSV עם כותרת ומרכאות מסביב לכל השדות
python3 - <<'EOF'
import csv

header = ["stream","flood_date","flood_source","name","status","date","source","source2","notes","Latitude","Longitude"]

if reader:
    reader[0] = header

with open("floods.tsv", newline="", encoding="utf-8") as tsvfile, \
     open("floods.csv", "w", newline="", encoding="utf-8") as csvfile:
    
    reader = csv.reader(tsvfile, delimiter="\t")
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    
    # כותבים את כל השורות
    for row in reader:
        writer.writerow(row)
EOF

# המרה ל‑GeoJSON
./node_modules/csv2geojson/csv2geojson --lat Latitude --lon Longitude "$csv" > "$geojson"

# אופציונלי: git
git add "$csv" "$geojson"
git commit -m "update source.geojson $(date +%Y-%m-%d-%R)"
git push

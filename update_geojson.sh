#!/bin/bash
set -euo pipefail

url="https://docs.google.com/spreadsheets/d/1BbT762qaYilLnwGD7sJDo8sfs_Y5ExjvixS_Tl3rSas/export?format=csv&gid=0&range=A4:M100&headers=0"
csv="floods.csv"
head="stream,flood_date,flood_source,name,status,date,source,source2,notes,Latitude,Longitude"

pushd "$(dirname "$0")" > /dev/null
git checkout main
git pull

wget -q "$url" -O "$csv"

# 1. החלפת שורת כותרת
sed -i "1s|.*|$head|" "$csv"

# 2. תיקון CSV שבור (שורות מפוצלות, מרכאות בעייתיות)
python3 fix_csv.py "$csv"

# 3. מילוי אוטומטי (forward-fill) בעמודות מידע שהיה ממוזג
#    כאן: stream (עמודה 1), flood_date (2), flood_source (3)
awk -F, '
BEGIN { OFS="," }
NR==1 { print; next }

{
    for (i=1; i<=3; i++) {
        if ($i == "") $i = last[i]
        else last[i] = $i
    }
    print
}
' "$csv" > tmp && mv tmp "$csv"

# 4. סינון שורות ללא קואורדינטות תקינות
awk -F, 'NR==1 || ($10 != "" && $11 != "")' "$csv" > filtered.csv
mv filtered.csv "$csv"

# 5. יצירת GeoJSON
./node_modules/csv2geojson/csv2geojson \
    --lat Latitude --lon Longitude "$csv" > source.geojson

git add source.geojson "$csv"
git commit -m "update source.geojson $(date +%Y-%m-%d-%R)"
git push
popd > /dev/null

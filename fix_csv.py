#!/usr/bin/env python3
import csv
import re
import sys

if len(sys.argv) != 2:
    print("Usage: fix_csv_latlon.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
NUM_COLUMNS = 11  # מספר העמודות הסופי

fixed_rows = []

latlon_re = re.compile(r'(\d+\.\d+),(\d+\.\d+)$')

with open(csv_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        m = latlon_re.search(line)
        if m:
            lat, lon = m.groups()
            rest = line[:m.start()].rstrip(",")
        else:
            # שורה ללא קואורדינטות
            lat = lon = ""
            rest = line

        # עכשיו נפרק את השאר לפי פסיקים
        # נשמור מרכאות שמכילות פסיקים
        row = next(csv.reader([rest]))
        # נוסיף Lat/Lon
        row += [lat, lon]

        # ריפוד לשורת NUM_COLUMNS
        while len(row) < NUM_COLUMNS:
            row.append("")

        fixed_rows.append(row)

# forward-fill עבור שלוש העמודות הראשונות: stream, flood_date, flood_source
last = ["", "", ""]
for r in fixed_rows[1:]:
    for i in range(3):
        if r[i].strip():
            last[i] = r[i]
        else:
            r[i] = last[i]

# סינון שורות ללא קואורדינטות
final_rows = [fixed_rows[0]]
for r in fixed_rows[1:]:
    if r[9] and r[10]:
        final_rows.append(r)

# כתיבה על אותו קובץ
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_rows)

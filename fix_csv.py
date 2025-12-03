#!/usr/bin/env python3
import csv
import sys

if len(sys.argv) != 2:
    print("Usage: fix_csv_complete.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]
NUM_COLUMNS = 11  # מספר העמודות הצפוי

fixed_rows = []

with open(csv_file, 'r', encoding='utf-8') as f:
    buffer = ""
    for line in f:
        line = line.rstrip("\n")
        if buffer:
            buffer += " " + line
        else:
            buffer = line
        try:
            reader = csv.reader([buffer])
            row = next(reader)
            if len(row) == NUM_COLUMNS:
                fixed_rows.append(row)
                buffer = ""
        except Exception:
            continue

# Forward-fill בעמודת stream (שם הנחל)
last_stream = ""
for r in fixed_rows[1:]:  # דילוג על כותרת
    if r[0].strip():
        last_stream = r[0]
    else:
        r[0] = last_stream

# סינון שורות ללא קואורדינטות
final_rows = [fixed_rows[0]]
for r in fixed_rows[1:]:
    if r[9].strip() and r[10].strip():
        final_rows.append(r)

# כתיבה על אותו קובץ
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final_rows)

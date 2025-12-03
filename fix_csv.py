#!/usr/bin/env python3
import csv
import sys

'''
תקון CSV שבור ע"י קריאה עם csv.reader שמצליח לפרש פסיקים וריבוי שורות
כותב קבצי CSV תקניים לחלוטין.
'''

inp = sys.argv[1]
out = sys.argv[2]

rows = []
with open(inp, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        # סינון שורות ריקות
        if not any(col.strip() for col in row):
            continue
        rows.append(row)

# מציאת מספר העמודות הגדול ביותר
width = max(len(r) for r in rows)

# ריפוד שורות קצרות
for r in rows:
    if len(r) < width:
        r.extend([""] * (width - len(r)))

with open(out, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

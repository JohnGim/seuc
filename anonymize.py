"""
Reads seuc26.csv and writes records.json containing only the 5 fields
the website needs: country, role, gender, age, travel method.
No names, emails, phones, medical data, or any other PII.

Run: python3 anonymize.py
"""
import csv, json

ROLE_MAP = {
    'Student/Young Adult':                              'S',
    'Serving young adults/students at the conference':  'O',
}

GENDER_MAP = {
    'Female': 'F',
    'Male':   'M',
}

# Coaches/9-seaters are grouped with car/vehicle
TRAVEL_MAP = {
    'Plane':             'plane',
    'Train':             'train',
    'Vehicle':           'car',
    'Bus/Coach':         'car',
    '9-seater (Edmund)': 'car',
    '9-seater (Bartek)': 'car',
    '9-seater (Matthew)':'car',
}

records = []
with open('seuc26.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        country = row['Country'].strip()
        if not country:
            continue

        raw_age = row['What is your age?'].strip()
        age = int(raw_age) if raw_age.isdigit() else None

        role   = ROLE_MAP.get(row['What is your registrant status for this conference?'].strip(), 'S')
        gender = GENDER_MAP.get(row['Gender'].strip(), 'F')
        travel = TRAVEL_MAP.get(row['What is your method of travel TO the conference?'].strip())

        records.append({
            'c': country,
            'r': role,
            'g': gender,
            'a': age,
            't': travel,
        })

with open('records.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, separators=(',', ':'))

print(f"Done — {len(records)} records → records.json")
print(f"  Roles:   { {v: sum(1 for r in records if r['r']==v) for v in ('S','O')} }")
print(f"  Travel:  { {k: sum(1 for r in records if r['t']==k) for k in ('plane','train','car',None)} }")

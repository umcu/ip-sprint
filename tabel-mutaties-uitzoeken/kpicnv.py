#!/usr/bin/env python3

from csv import DictReader, DictWriter
from datetime import datetime, timedelta

fieldnames = [
    'opnamemoment', 'ontslagdatum', 'ontslagmoment', 'ontslagspecialisme_specialisme_id',
    'ontslagspecialisme_specialisme_identifier_system', 'ontslagspecialisme_specialisme_identifier_value',
    'opnametype_id', 'opnametype_identifier_system', 'opnametype_identifier_value', 'organisatie-eenheid_id',
    'organisatie-eenheid_identifier_system', 'organisatie-eenheid_identifier_value', 'ontslagafdeling_afdeling_id',
    'ontslagafdeling_afdeling_identifier_system', 'ontslagafdeling_afdeling_identifier_value', 'leeftijd_bij_ontslag',
    'ontslagbrief_aanwezig', 'ontslagbericht_aanwezig', 'brief_binnen_14_dagen', 'brief_of_bericht_op_tijd',
    'moment_brief_aangemaakt', 'moment_brief_akkoord', 'moment_brief_gewijzigd', 'moment_brief_verstuurd',
    'moment_bericht_verstuurd', 'duur_aanmaken_brief', 'duur_akkoord_brief', 'duur_doorloop_brief',
    'duur_versturen_brief', 'duur_versturen_bericht', 'kpi_klinisch_ontslag_bericht'
]
infilename = 'kpidata_2021.csv'
outfilename = 'cnvdata_2021.csv'
infile = open(infilename, 'r', encoding='utf-8-sig')
outfile = open(outfilename, 'w')

def dt(s):
    try:
        return datetime.fromisoformat(s)
    except:
        return None

def hours(td: timedelta):
    return int(td.total_seconds()/3600)

def convert(f, row, origin):
    moment = dt(row[f])
    if moment:
        row[f] = hours(moment-origin)

reader = DictReader(infile)
writer = DictWriter(outfile, fieldnames=fieldnames)
writer.writeheader()
for row in reader:
    if row['ontslagmoment'] == 'NULL': continue
    om = dt(row['ontslagmoment'])
    convert('moment_brief_aangemaakt', row, om)
    convert('moment_brief_akkoord', row, om)
    convert('moment_brief_gewijzigd', row, om)
    convert('moment_brief_verstuurd', row, om)
    convert('moment_bericht_verstuurd', row, om)
    try:
      writer.writerow(row)
    except ValueError:
        print(list(row.keys()))
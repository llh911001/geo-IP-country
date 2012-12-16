#!/usr/bin/env python
# coding: utf-8

import csv
import sqlite3
from collections import namedtuple

#CSV_FILE = 'geo_IP_other.csv'
CSV_FILE = 'CN_geo_cmcc_inserted.csv'
GeoIP = namedtuple("GeoIP", ['StartIP', 'EndIP', 'StartNum', 'EndNum', 'CountryCode', 'CountryName', 'Organization'])

def unicode_csv_reader(encoded_data, encoding='utf-8', *args, **kwargs):
    csv_reader = csv.reader(encoded_data, *args, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, encoding) for cell in row]

conn = sqlite3.connect('GeoIP.db')
reader = unicode_csv_reader(open(CSV_FILE))
with conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS GeoIP(
                StartIP TEXT,
                EndIP TEXT,
                StartNum INT,
                EndNum INT,
                CountryCode TEXT,
                CountryName TEXT,
                Organization TEXT)""")
    for rec in reader:
        cur.execute("INSERT OR IGNORE INTO GeoIP VALUES(?,?,?,?,?,?,?)", rec)

#!/usr/bin/env python
#coding: utf-8

import sys
import sqlite3
import argparse
from collections import namedtuple
from helper.ipcalc import IP, Network

_db = 'GeoIP.db'
lookup_sql = "SELECT CountryCode, CountryName, Organization FROM GeoIP WHERE StartNum<? AND EndNum>?"

GeoIP = namedtuple("GeoIP", ['CountryCode', 'CountryName', 'Organization'])

def valid_IP(dq):
    try:
        ip = IP(dq)
    except ValueError, e:
        raise argparse.ArgumentTypeError(e)
    return ip

def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=valid_IP, help="dotquad IP address")
    return parser.parse_args(argv)

def lookup(ip):
    """ip is an instance of IP object"""
    ip_num = int(ip)
    conn = sqlite3.connect(_db)
    with conn:
        cur = conn.cursor()
        cur.execute(lookup_sql,(ip_num, ip_num))
        rows = cur.fetchall()
    return rows

def ip_lookup(args):
    res = lookup(args.ip)
    if len(res) == 1:
        geo_ip = GeoIP._make([u.encode('utf-8') for u in res[0]])
        print '{:<16}:\t{:<}'.format('IP', str(args.ip))
        print '{:<16}:\t{:<}'.format('Country', geo_ip.CountryName)
        print '{:<16}:\t{:<}'.format('Country Code', geo_ip.CountryCode)
        print '{:<16}:\t{:<}'.format('ISP', geo_ip.Organization)
    elif len(res) > 1:
        raise ValueError, "Fatal Error: One IP can not belong to more than TWO country! Something went wrong with our database."
    else:
        print "we are sorry, but there are NO results about this IP: %s" % str(args.ip)

if __name__ == '__main__':
    args = parse_command_line(sys.argv[1:])
    ip_lookup(args)

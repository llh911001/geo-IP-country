#!/usr/bin/env python
# coding: utf-8

import csv
from ipcalc import Network

def dq_to_ip(dq):
    """Convert dotquad to int."""
    bits = dq.split('.')
    if len(bits) != 4:
        raise ValueError, "%r: IPv4 address invalid: should be 4 bytes" % dq
    for q in bits:
        if int(q) < 0 or int(q) > 255:
            raise ValueError, "%r: IPv4 address invalid: bytes should be between 0 and 255" % dq
    return int(bits[0])<<24 | int(bits[1])<<16 | int(bits[2])<<8 | int(bits[3])

def ip_to_dq(ip):
    """Convert int ip to dotquad."""
    return '.'.join(map(str, [(ip>>24) & 0xff, (ip>>16) & 0xff, (ip>>8) & 0xff, ip & 0xff]))


def new_isp_ip():
    with open('new_isp_ip.txt', 'w') as f:
        for line in open('isp_ip.txt'):
            line = line.strip()
            if line:
                elems = [e.strip() for e in line.split('/')]
                try:
                    mask = int(elems[1])
                except ValueError:
                    f.write(','.join(elems) + '\n')
                    continue
                network = Network(elems[0], mask=mask)
                elems[0] = network.network().dq
                elems[1] = network.broadcast().dq
                f.write(','.join(elems) + '\n')

def geo_IP_cn():
    with open('cmcc_ip2.txt', 'w') as f:
        for line in open('cmcc_ip.txt'):
            elems = line.split(',')
            network = dq_to_ip(elems[0])
            broadcast = dq_to_ip(elems[1])
            res = elems[:2] + [str(network), str(broadcast)] + elems[2:]
            f.write(','.join(res))

def country_name_dict():
    d = {}
    for line in open('countries.txt'):
        elems = line.split()
        d[elems[1]] = elems[0]
    return d

def translate_country_name():
    cd = country_name_dict()
    writer = csv.writer(open('geo_IP_country_whois.csv' ,'w'))
    reader = csv.reader(open('GeoIPCountryWhois.csv'))
    for line in reader:
        line[-1] = cd.get(line[-1], line[-1])
        writer.writerow(line)


if __name__ == '__main__':
    writer = csv.writer(open('cmcc_ip_merged_final.csv', 'w'))
    reader = csv.reader(open('cmcc_ip_merged.csv'))
    for elems in reader:
        res = elems[:4] + ['CN', '中国'] + elems[-1:]
        writer.writerow(res)

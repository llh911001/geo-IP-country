#!/usr/bin/env python
#coding: utf-8

import csv
from utils import dq_to_ip, ip_to_dq

MERGE_IN_FILE = 'cmcc_ip_cmcc.txt'
MERGE_OUT_FILE = 'c_i_c_merge_test.csv'
INSERT_IN_FILE = 'CN_geo_cmcc.csv'
INSERT_OUT_FILE = 'CN_geo_cmcc_inserted.csv'

def merge_consecutive(numberlist):
    """Convert consecutive numbers into `a-b' format.

    Example:
    >>>merge_consecutive([1,2,3,4,5,6,8,9,10,11,15,16,19])
    1-6,8-11,15-16,19
    >>>
    """
    numberlist.sort()
    prev_number = numberlist[0]
    continuous = []
    for number in numberlist:
        if number != prev_number+1:
            continuous.append([number])
        elif len(continuous[-1]) > 1:
            continuous[-1][-1] = number
        else:
            continuous[-1].append(number)
        prev_number = number
    #print continuous
    return ','.join(['-'.join(map(str,page)) for page in continuous])


def merge(elems):
    """
    elems is a list of list, merge the consecutive IP segments of same orgnisation to one.

    for example:
    >>>elems = [['221.130.208.0','221.130.211.255','3716337664','3716338687','中国移动(集团公司)'],
    ...         ['221.130.212.0','221.130.223.255','3716338688','3716341759','中国移动(集团公司)'],
    ...         ['221.130.224.0','221.130.255.255','3716341760','3716349951','中国移动(集团公司)']
    ...         ['218.206.190.0','218.206.191.255','3670982144','3670982655','中国移动(集团公司)']]
    ...
    >>>merge(elems)
    [['221.130.208.0','221.130.255.255','3716337664','3716349951','中国移动(集团公司)'],
    ['218.206.190.0','218.206.191.255','3670982144','3670982655','中国移动(集团公司)']]
    """
    elems.sort(key=lambda x: int(x[2]))
    prev = elems[0]
    merged = []
    for e in elems:
        if (int(e[2]) != int(prev[3]) + 1) or (e[-1] != prev[-1]):
            merged.append([e])
        elif len(merged[-1]) > 1:
            merged[-1][-1] = e
        else:
            merged[-1].append(e)
        prev = e
    # merged = [[start,end], [single] ... ]
    merge_two = lambda x, y: [x[0] + y[1] + x[2] + y[3]] + x[4:]
    return [reduce(merge_two, x) for x in merged]

def test_merge():
    reader = csv.reader(open(MERGE_IN_FILE))
    writer = csv.writer(open(MERGE_OUT_FILE, 'w'), lineterminator='\n')
    elems = list(reader)
    result = merge(elems)
    for row in result:
        writer.writerow(row)


def insert(elems):
    """
    elems is a list of list, insert the subnet IP segments into 

    for example:
    >>>elems = [['111.16.0.0','111.63.255.255','1863319552','1866465279','CN','中国'],
    ...         ['112.0.0.0','112.67.255.255','1879048192','1883504639','CN','中国'],
    ...         ['112.0.0.0','112.4.255.255','1879048192','1879375871','CN', '中国','中国移动(江苏)'],
    ...         ['112.5.0.0','112.5.255.255','1879375872','1879441407','CN','中国','中国移动(福建)']]
    ...
    >>>insert(elems)
    [[['111.16.0.0','111.63.255.255','1863319552','1866465279','CN','中国']],
     [['112.0.0.0','112.67.255.255','1879048192','1883504639','CN','中国'],
      ['112.0.0.0','112.4.255.255','1879048192','1879375871','CN', '中国','中国移动(江苏)'],
      ['112.5.0.0','112.5.255.255','1879375872','1879441407','CN','中国','中国移动(福建)']]]
    >>>
    """
    elems.sort(key=lambda x: int(x[2]))
    prev = elems[0]
    res = []
    for e in elems:
        if e == prev:
            res.append([e])
        elif int(e[2]) < int(prev[3]):
            res[-1].append(e)
        else:
            res.append([e])
            prev = e
    return res

def do_insert(lsts):
    """
    take what was returned fron function insert.

    for example:
    >>>lsts = [[['111.16.0.0','111.63.255.255','1863319552','1866465279','CN','中国']],
    ...        [['112.0.0.0','112.67.255.255','1879048192','1883504639','CN','中国'],
    ...        ['112.0.0.0','112.4.255.255','1879048192','1879375871','CN', '中国','中国移动(江苏)'],
    ...        ['112.5.0.0','112.5.255.255','1879375872','1879441407','CN','中国','中国移动(福建)']]]
    ...
    >>>do_insert(lsts)
    [['111.16.0.0','111.63.255.255','1863319552','1866465279','CN','中国'],
     ['112.0.0.0','112.4.255.255','1879048192','1879375871','CN', '中国','中国移动(江苏)'],
     ['112.5.0.0','112.5.255.255','1879375872','1879441407','CN','中国','中国移动(福建)'],
     ['112.6.0.0','112.67.255.255','1879441408','1883504639','CN','中国']]
    >>>
    """
    result = []
    for lst in lsts:
        if len(lst) > 1:
            max_dq, max_ip, misc = lst[0][1], lst[0][3], lst[0][4:]
            lst[0][1] = ip_to_dq(int(lst[1][2])-1)
            lst[0][3] = str(int(lst[1][2])-1)
            if int(lst[0][2]) > int(lst[0][3]):
                lst = lst[1:]
            rest_start = int(lst[-1][3]) + 1
            if rest_start < int(max_ip):
                rest = [ip_to_dq(rest_start),max_dq,str(rest_start),max_ip] + misc
                lst.append(rest)
        result.extend(lst)
    return result

def test_insert():
    reader = csv.reader(open(INSERT_IN_FILE))
    elems = list(reader)
    lst = insert(elems)
    result = do_insert(lst)
    print result
    writer = csv.writer(open(INSERT_OUT_FILE, 'w'), lineterminator='\n')
    for row in result:
        writer.writerow(row)

if __name__ == '__main__':
    test_insert()

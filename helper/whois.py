#!/usr/bin/env python

import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('whois.apnic.net', 43))
s.send(sys.argv[1] + '\r\n')

response = ''
while True:
    d = s.recv(4096)
    response += d
    if not d:
        break

s.close()
print
print response

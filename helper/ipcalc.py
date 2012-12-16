#!/usr/bin/env python
#coding: utf-8

class IP(object):
    """IP class."""
    def __init__(self, ip, mask=None):
        self.mask = mask
        if isinstance(ip, IP):
            self.ip = ip.ip
            self.dq = ip.dq
            self.mask = ip.mask
        elif isinstance(ip, (int, long)):
            self.ip = ip
            if self.ip > 0xffffffff:
                raise ValueError, "%r: IPv4 address invalid: must be less than 0xffffffff" % ip
            self.dq = self._to_dq(ip)
        else:
            if '/' in ip:
                ip, mask = ip.split('/', 1)
                self.mask = int(mask)
            self.dq = ip
            self.ip = self._to_ip(ip)

        if self.mask is None:
            b = self.binary()
            if b.startswith('0'):    # Class A
                self.mask = 8
            elif b.startswith('10'): # Class B
                self.mask = 16
            else:
                self.mask = 24       # Class C
        if self.mask < 0 or self.mask > 32:
            raise ValueError, "%r: IPv4 address invalid: mask must be between 0 and 32" % ip

    def binary(self):
        """binary representation of the ip."""
        b = bin(self.ip)[2:]
        return ''.join('0' for x in range(32-len(b))) + b

    def _to_ip(self, dq):
        """Convert dotquad to int."""
        bits = dq.split('.')
        if len(bits) != 4:
            raise ValueError, "%r: IPv4 address invalid: should be 4 bytes" % dq
        for q in bits:
            if int(q) < 0 or int(q) > 255:
                raise ValueError, "%r: IPv4 address invalid: bytes should be between 0 and 255" % dq
        return int(bits[0])<<24 | int(bits[1])<<16 | int(bits[2])<<8 | int(bits[3])

    def _to_dq(self, ip):
        """Convert int ip to dotquad."""
        return '.'.join(map(str, [(ip>>24) & 0xff, (ip>>16) & 0xff, (ip>>8) & 0xff, ip & 0xff]))

    def size(self):
        return 1

    def __str__(self):
        return self.dq

    def __int__(self):
        return int(self.ip)

class Network(IP):
    """ Network calculations."""
    def netmask(self):
        """Network netmask of IP instance."""
        return IP((0xffffffff >> (32-self.mask)) << (32-self.mask))

    def network(self):
        """Network address."""
        return IP(self.ip & int(self.netmask()))

    def broadcast(self):
        """Broadcast address."""
        return IP(int(self.network()) | (0xffffffff-int(self.netmask())))

    def first_host(self):
        return IP(int(self.nerwork()) + 1)

    def last_host(self):
        return IP(int(self.broadcast()) - 1)

    def size(self):
        return 2 ** (32 - self.mask)

    def __repr__(self):
        return 'Network(%s/%s)' % (self.dq, self.mask)

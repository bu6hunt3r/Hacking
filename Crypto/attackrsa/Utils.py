#!/usr/bin/env python

import gmpy

def egcd(a,b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    g, g1 = a, b
    while g1:
            q = g // g1
            u, u1 = u1, u - q * u1
            v, v1 = v1, v - q * v1
            g, g1 = g1, g - q * g1
    return u, v    

def modInv(a,m):
    '''
    Return r such that a*r mod m = 1
    '''
    return gmpy.invert(a,m)

def CRT(ds, rs):
    pass
    
def main():
    print egcd(5,3)
    print modInv(17,3)
if __name__ == '__main__':
    main()
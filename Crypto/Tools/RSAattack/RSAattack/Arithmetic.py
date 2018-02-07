#!/usr/bin/env python

from __future__ import print_function

def gcd(a,b):
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def egcd(a,b):
    u, u1 = 1, 0
    v, v1 = 0, 1

    while b:
        q=a//b
        u, u1 = u1, u-q*u1
        v, v1 = v1, v-q*v1
        a,b = b, a-q*b
    return (u, v, a)

def modInverse(e,n):
    '''
    d such that de = 1 (mod n)
    e must be coprime to n
    '''
    return egcd(e,n)[0]%n

def bitlength(x):
    '''
    Calculates bitlength of n
    '''
    assert x>=0
    n=0
    while x > 0:
        n=n+1
        x = x>>1
    return n

def isqrt(n):
    if n < 0:
        raise ValueError("square root not defined for negative numbers")

    if n==0:
        return 0
    a,b=divmod(bitlength(n),2)
    x=2**(a+b)
    while True:
        y = (x+n//x)//2
        if y >= x:
            return x
        x=y

def is_perfect_square(n):
    h = n & 0xF

    if h > 9:
        return -1

    if (h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8):
        t=isqrt(n)
        if t*t == n:
            return t
        else:
            return -1

    return -1

def test_is_perfect_square():
    print("Testing is_perfect_square")
    testsuit = [4, 0, 15, 25, 18, 901, 1000, 1024]

    for n in testsuit:
        print("Is ", n, " a perfect square?")
        if is_perfect_square(n)!= -1:
            print("Yes!")
        else:
            print("Nope")

def fermat(n):
    a = isqrt(n) 
    b2 = a*a - n
    b = isqrt(n) 
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2) 
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    return p, q

if __name__=="__main__":
    test_is_perfect_square()

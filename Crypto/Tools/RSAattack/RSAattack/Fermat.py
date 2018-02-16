from __future__ import print_function
from RSAattack.Arithmetic import isqrt

def fermat(n,verbose=True):
    a=isrt(n)
    b2=a*a-n
    b=isqrt(n)
    count=0
    while b*b != b2:
        if verbose:
            print("Trying a=%s b2=%s b=%s" % (a,b2,b))
        a=a+1
        b2=a*a-n
        b=isqrt(b2)
        count+=1
    p=a+b
    q=a-b
    assert n==p*q
    print('a=',a)
    print('b=',b)
    print('p=',p)
    print('q=',q)
    print('p*q=',p*q)
    return p,q

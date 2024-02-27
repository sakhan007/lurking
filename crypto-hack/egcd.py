#! /usr/bin/python3

import sys

# From the book Understanding Cryptography. This code solves a Cryptohack challenge modular arithmetic
# We are required to find u and v such that 26513*u+32321*v=gcd(32321,26513) using extended gcd algorithim.


def gcd(r0,r1):
    if r1 == 0:
        return r0
    else:
        return gcd(r1,r0%r1)

#print(gcd(973,301)) # should be 7


def egcd(r0,r1):

    # initialization
    s0 = 1
    t0 = 0
    s1 = 0
    t1 = 1

    r = 1
    while (r != 0):
        r = r0 % r1
        q = (r0 - r)/r1
        s = s0 - q*s1
        t = t0 - q*t1
        
        # updation
        r0 = r1
        r1 = r
        s0 = s1
        s1 = s
        t0 = t1
        t1 = t

    return r0, s0, t0 # We had to use r0, s0,t0; since we are printing after updation of values

#print(egcd(973,301)) # should return 7,13,-42 


if len(sys.argv) != 3:
    print("\n")
    print("   Usage: python3 egcd.py num1 num2...  ")
    sys.exit()
else:
    a,b,c = egcd(int(sys.argv[1]), int(sys.argv[2]) )
    print("\n")
    print(f"   The numbers you are looking for are: {b}, {c}")
    print(f"   The GCD of the numbers you supplied is {a} ")
    print(f"   Hence the equation is {b}x{sys.argv[1]} + {c}x{sys.argv[2]} = gcd({sys.argv[1]}, {sys.argv[2]})")

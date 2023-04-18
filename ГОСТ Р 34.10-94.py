from random import getrandbits, randint
from sympy import isprime
from Crypto.Util import number

def gen_keys():
    # left=getrandbits(254)
    # right=getrandbits(256)
    q=number.getPrime(256)

    # l,r=getrandbits(250),getrandbits(256)
    r=getrandbits(256)

    while True:
        p=q*r
        if isprime(p+1):
            break
        else: r+=1
    p+=1
    print('p:\n',p)
    print('q:\n',q)


    # print(len(str(bin(p)[2:])))
    # print(len(str(bin(q)[2:])))
    # print(isprime(q))
    # print(isprime(p))

    print((p-1)%q==0)

    a = pow(number.getRandomRange(2, p-1), q, p)
    print('a:\n',a)

    x=number.getRandomRange(2, q-1)
    print('x:\n',x)

    y=pow(a,x,p)
    print('y:\n',y)


import random
from sympy import isprime
from math import gcd 

# создаем список простых чисел до 1000
primes = [i for i in range(1,1000) if isprime(i)]

def get_prime():
    # выбираем два случайных простых числа
    while True:
        p = random.choice(primes)
        q = random.choice(primes)
        # проверяем, что их произведение состоит из 4 цифр и они не равны друг другу
        if len(str(p*q)) == 4 and p!=q:
            return p,q     

def EXP(fn):
    # выбираем случайное простое число e, такое что 1 < e < Ф(n) и gcd(e, Ф(n)) = 1
    e = next((e for e in primes if gcd(fn, e) == 1 and 1 < e < fn),None)
    return e

def NOD(e, fn):
    # вычисляем наибольший общий делитель двух чисел и их коэффициенты Безу
    if e == 0 :
        return fn,0,1
    gcd,x1,y1 = NOD(fn%e, e)
    x = y1 - (fn//e) * x1
    y = x1
    return gcd,x,y

def inverse(fn,e):
    # находим мультипликативно обратный элемент e по модулю Ф(n)
    gcd, x, y = NOD(e, fn)
    if gcd == 1:
        return((x % fn + fn) % fn)

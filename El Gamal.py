import random
from sympy import isprime,primitive_root
import time

def is_primitive_root(a, p):
    """
    Функция, которая проверяет, является ли a первообразным корнем по модулю p.
    """
    if pow(a, p - 1, p) != 1:
        return False
    for i in range(2, p - 1):
        if pow(a, i, p) == 1:
            return False
    return True


def find_primitive_root(p):
    """
    Функция, которая находит первообразный корень по модулю p.
    """
    for a in range(2, p):
        if is_primitive_root(a, p):
            return a
    return None


def Elgamal(m):
    print("m: ",m)
    while True:
        p=random.randrange(100_000, 1_000_000)
        if isprime(p):
            break

    print("p: ",p)

    # g = find_primitive_root(p)
    g=primitive_root(p)
    print("g: ",g)
    x=random.randint(2,p-2)
    print("x: ",x)
    y=pow(g,x,p)
    print("y: ",y)
    k=random.randint(2,p-2)
    print("k: ",k)

    a=pow(g,k,p)
    b=((y**k)*m)%p
    print("a: ",a) #a и b это ШТ
    print("b: ",b)

    M=(b*(a**(p-1-x)))%p
    print("M: ",M)
    print("__________________")

    return a,b,M

Ot=input("Введите текст: ")
start_time = time.time()
text=list(Ot)
num_text=[int(ord(i)) for i in text]
print(num_text)

pom=[Elgamal(i) for i in num_text]

enc_text = [(pom[i][j]) for i in range(len(pom)) for j in range(2)]
dec_text = [(pom[i][2]) for i in range(len(pom))]

print("Числа в Ш.Т:\n",enc_text)

dec_text1=[chr(dec_text[i]) for i in range(len(dec_text))]

print("Результат дешифрования:\n","".join(dec_text1))
print(time.time() - start_time)
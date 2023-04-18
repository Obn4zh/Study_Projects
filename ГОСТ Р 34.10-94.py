from random import getrandbits, randint
from sympy import isprime
from Crypto.Util import number
import hashlib
import gostcrypto as gost

def gen_keys():
    print("___ГЕНЕРАЦИЯ КЛЮЧЕЙ___")
    while True:
        q=randint(2**254,2**256)
        # q=number.getPrime(256)

        r=randint(2**244,2**256)
        # r=number.getPrime(256)

        while True:
            p=q*r
            if isprime(p+1):
                break
            else: r+=1
        p+=1
        if (512>=len(str(bin(p)[2:]))>=509) and (256>=len(str(bin(q)[2:]))>=254) and isprime(p) and isprime(q):
            break
    print('p:\n',p)
    print('q:\n',q)


    print(len(str(bin(p)[2:])))
    print(len(str(bin(q)[2:])))
    print(isprime(q))
    print(isprime(p))

    print((p-1)%q==0)

    while True:
        g = randint(2, p - 1)
        a = pow(g, (p-1)//q, p)
        if a != 1:
            break

    print('a:\n',a)
    x=number.getRandomRange(2, q-1)
    print('x:\n',x)

    y=pow(a,x,p)
    print('y:\n',y)

    with open("private.pem", "w") as file:
        file.write(str(x))
        print('Закрытый ключ записан')
    with open("public.pem", "w") as file:
        file.write(str(y))
        print('Открытый ключ записан')
    with open("open_a.txt", "w") as file:
        file.write(str(a))
        print('Открытый параметр a записан')
    with open("open_p.txt", "w") as file:
        file.write(str(p))
        print('Открытый параметр p записан')
    with open("open_q.txt", "w") as file:
        file.write(str(q))
        print('Открытый параметр q записан')

    
def read_doc(way):
    with open(way, "rb") as file:
                # Создаем объект хэш-функции SHA-256 или ГОСТ Р 34.11-94
            hash = gost.gosthash.new('streebog256')
            # hash = hashlib.sha256()
            while chunk := file.read(256):
                hash.update(chunk)
                # Получаем хэш-значение в виде строки
            hash_value = hash.hexdigest()

    hash_int=int(hash_value,16)
    print(f"Хэш:\n{hash_int}\n")
    # print(len(str(bin(hash_int)[2:])))
    return(hash_int)

def send(hash):
    print("___ПОДПИСЬ ДОКУМЕНТА___")

    with open("open_q.txt") as file:
        q = file.read()
    with open("open_p.txt") as file:
        p = file.read()
    with open("private.pem") as file:
        x = file.read()
    with open("open_a.txt") as file:
        a = file.read()

    q,p,x,a=int(q),int(p),int(x),int(a)

    while True:
        k=number.getRandomRange(1, q-1)
        r=(pow(a,k,p))%q
        if r!=0:
            break
    if hash%q==0:
        hash=1    
    s=(x*r+k*(hash))%q

    with open("r.txt", "w") as file:
        file.write(str(r))
    with open("s.txt", "w") as file:
        file.write(str(s))
    print('k:\n',k)
    print('r:\n',r)
    print('s:\n',s)


def recive(way):
    print("___ПРОВЕРКА ПОДПИСИ___")

    with open("open_q.txt") as file:
        q = file.read()
    with open("open_p.txt") as file:
        p = file.read()
    with open("public.pem") as file:
        y = file.read()
    with open("open_a.txt") as file:
        a = file.read()

    with open("r.txt") as file:
        r = file.read()
    with open("s.txt") as file:
        s = file.read()
    
    q,p,y,r,s,a=int(q),int(p),int(y),int(r),int(s),int(a)
    hash=read_doc(way)

    v=pow(hash,q-2,q)
    print("v:\n",v)
    one_z=(s*v)%q
    print("1z:\n",one_z)
    two_z=((q-r)*v)%q
    print("2z:\n",two_z)

    u=(((pow(a,one_z,p))*(pow(y,two_z,p)))%p)%q
    print("u:\n",u)
    if u==r:
        print("\nПодпись верна!")
    else:
        print("\nПодпись неверна!")
    

way="dok.docx"
hash=read_doc(way)

while True:
    action=input('\n\nГенерация ключей - 1\nПодписать - 2\nПроверить подпись - 3\nЛюбая другая клавиша - выйти\n')
    if action=='1':
        gen_keys()
    elif action=='2':
        send(hash)
    elif action=='3':
        recive(way)
    else: quit()

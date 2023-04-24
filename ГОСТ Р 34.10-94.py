from random import randint
from sympy import isprime
from Crypto.Util import number
import gostcrypto as gost

def gen_keys():
    print("___KEY GENERATION___")
    while True:
        q=randint(2**254,2**256)
        # q=number.getPrime(256)

        generator=randint(2**244,2**256)
        # r=number.getPrime(256)
        while True:
            p=q*generator
            if isprime(p+1):
                break
            else: generator+=1
        p+=1
        if (512>=p.bit_length()>=509) and (256>=q.bit_length()>=254) and isprime(p) and isprime(q):
            break
    print('p:\n',p)
    print('q:\n',q)


    print(p.bit_length())
    print(q.bit_length())
    print(isprime(q))
    print(isprime(p))

    print((p-1)%q==0)
#проверка того, что g является корнем порядка q в p
#это элемент g, который генерирует подгруппу порядка q в мультипликативной группе вычетов по модулю p

    while True:
        g = randint(2, p - 1) 
        a = pow(g, (p-1)//q, p)
        if a != 1:
            break

    print('a:\n',a)
    print(pow(a,q,p)==1)
    x=number.getRandomRange(2, q-1)
    print('x:\n',x)

    y=pow(a,x,p)
    print('y:\n',y)

    with open("private.pem", "w") as file:
        file.write(str(x))
        print('Private key writen')
    with open("public.pem", "w") as file:
        file.write(str(y))
        print('Public key writen')
    with open("open_a.txt", "w") as file:
        file.write(str(a))
        print('Public parameter (a) writen')
    with open("open_p.txt", "w") as file:
        file.write(str(p))
        print('Public parameter (p) writen')
    with open("open_q.txt", "w") as file:
        file.write(str(q))
        print('Public parameter (q) writen')


def read_doc(way):
    with open(way, "rb") as file:
                # Создаем объект хэш-функции ГОСТ Р 34.11-94
            hash = gost.gosthash.new('streebog256')
            while chunk := file.read(256):
                hash.update(chunk)
                # Получаем хэш-значение в виде строки
            hash_value = hash.hexdigest()

    hash_int=int(hash_value,16)
    print(f"Hash:\n{hash_int}\n")
    # print(len(str(bin(hash_int)[2:])))
    return(hash_int)

def send(way):
    hash=read_doc(way)
    print("___DOCUMENT SIGNING___")

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
    print('\nThe document was signed')


def recive(way):
    print("___SIGNATURE VERIFICATION___")

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
        print("\nThe signature is correct!")
    else:
        print("\nThe signature is wrong!")


way="D:\\4 курс\\2 семестр\\КМЗИ\\lab_6(ГОСТ ЭЦП)\\dok.docx"

while True:
    try:
        action=input('\n\nKey generation - 1\nSign a document - 2\nSignature check - 3\nAny other button - quit\n')
        if action=='1':
            gen_keys()
        elif action=='2':
            send(way)
        elif action=='3':
            recive(way)
    except: print("\nWrong input!")
    
    if action!='1' and action!='2' and action!='3': quit()
    

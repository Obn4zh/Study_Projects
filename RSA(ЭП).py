import hashlib
import random
from sympy import isprime

def get_prime(bit_length):
        while True:
            candidate = random.getrandbits(bit_length)
            if isprime(candidate):
                return candidate

def get_private_exponent(e, phi):
    return pow(e, -1, phi)

def EXP(key_size):
        while True:
            e = random.randint(2**(key_size-1), 2**key_size - 1)
            if isprime(e):
                break
        return e

def gen_keys():
    key_size = 2048
    p = get_prime(key_size // 2)
    q = get_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = EXP(key_size)
    d = get_private_exponent(e, phi)
    private_key = (d, n)
    public_key = (e, n)
    return (public_key,private_key)

def check_sign(hash_int,sign,pub):
    un=pow(sign,pub[0],pub[1])

    # if un==hash_int%pub[0]: #Модуль нужен если длина ключа маленькая
    if un==hash_int:
        print("Подпись верна!")
    else:
        print("Подпись неверна!!")

def sign_a_document(way):
    pub,priv=gen_keys()
    print(f"Публичный ключ:\n{pub}\n")
    print(f"Приватный ключ:\n{priv}\n")
    with open(way, "rb") as file:
            # Создаем объект хэш-функции SHA-256 или md5
        hash = hashlib.sha256()
        # hash = hashlib.md5()
        while chunk := file.read(2048):
            hash.update(chunk)
            # Получаем хэш-значение в виде строки
        hash_value = hash.hexdigest()

    hash_int=int(hash_value,16)
    print(f"Хэш:\n{hash_int}\n")
    return hash_int,pub,priv

def sign_doc_save(hash_int,priv,way_sign):
    sign=pow(hash_int,priv[0],priv[1])
    print(f"Подпись:\n{sign}\n")
    with open(way_sign, "w") as file:
        sign=file.write(str(sign))
    return sign

if __name__ == "__main__":
    way="Путь к документу"
    way_pub="Путь к первой части публичного ключа(e)"
    way_pub1="Путь ко второй части публичного ключа(N)"
    way_sign="Путь к ЭП"
    
    hash,pubkey,priv=sign_a_document(way)
    k=input("Есть подпись - 1, нет - 0: ")
    if k=="0":
        with open(way_pub, "w") as file:
            file.write(str(pubkey[0]))

        with open(way_pub1, "w") as file:
            file.write(str(pubkey[1]))
        x=sign_doc_save(hash,priv,way_sign)
    
    elif k=="1":
        with open(way_sign) as file:
            x = file.read()
        x=int(x)

        with open(way_pub) as file:
            public = file.read()
        public=int(public)

        with open(way_pub1) as file:
            public1 = file.read()

        public1=int(public1)
        pub_klych=(public,public1)
        check_sign(hash,x,pub_klych)

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

    sign=pow(hash_int,priv[0],priv[1])
    print(f"Подпись:\n{sign}\n")
    return hash_int,sign,pub

if __name__ == "__main__":
    way="D:\\4 курс\\2 семестр\\КМЗИ\\Lab_5(ЭЦП)\\test.docx"
    hash,sign,pubkey=sign_a_document(way)
    check_sign(hash,sign,pubkey)
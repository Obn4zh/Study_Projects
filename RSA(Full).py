import random
import time
from sympy import isprime


class RSAEncryptor:
    def __init__(self, key_size):
        p = self.get_prime(key_size // 2)
        q = self.get_prime(key_size // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = self.EXP(key_size)
        d = self.get_private_exponent(e, phi)
        self.key = (n, d)
        self.public_key = (n, e)
    
    def EXP(self, key_size):
        while True:
            e = random.randint(2**(key_size-1), 2**key_size - 1)
            if isprime(e):
                break
        return e

    def encrypt(self, message):
        message_bytes = message.encode('utf-8')
        message_int = int.from_bytes(message_bytes, byteorder='big')
        encrypted_int = pow(message_int, self.public_key[1], self.public_key[0])
        encrypted_bytes = encrypted_int.to_bytes((encrypted_int.bit_length() + 7) // 8, byteorder='big')
        return encrypted_bytes.hex()

    def decrypt(self, ciphertext):
        ciphertext_bytes = bytes.fromhex(ciphertext)
        ciphertext_int = int.from_bytes(ciphertext_bytes, byteorder='big')
        decrypted_int = pow(ciphertext_int, self.key[1], self.key[0])
        decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')
        return decrypted_bytes.decode('utf-8')

    def pub_key(self):
        return self.public_key

    def priv_key(self):
        return self.key

    def get_prime(self, bit_length):
        while True:
            candidate = random.getrandbits(bit_length)
            if isprime(candidate):
                return candidate

    def EXP(self, key_size):
        while True:
            e = random.randint(2**(key_size-1), 2**key_size - 1)
            if isprime(e):
                break
        return e

    def get_private_exponent(self, e, phi):
        return pow(e, -1, phi)
    


if __name__ == '__main__':
    start_time = time.time()
    rsa = RSAEncryptor(2048)
    # message = input("Введите текст: ")
    message="Текст сообщения"
    ciphertext = rsa.encrypt(message)
    plaintext = rsa.decrypt(ciphertext)
    pub = rsa.pub_key()
    priv = rsa.priv_key()

    print(f"Сообщение: {message}\n")
    print(f"Зашифрованное сообщение: {ciphertext}\n")
    print(f"pub_key: {pub}\n")
    print(f"priv_key: {priv}\n")
    print(f"Дешифрованное сообщение: {plaintext}\n")
    print(f"Время выполнения: {time.time() - start_time}")
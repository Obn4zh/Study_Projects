"""Учебная реализация RSA с акцентом на чистоту кода."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from .number_theory import generate_prime, mod_inverse


@dataclass(frozen=True)
class RSAPublicKey:
    """Публичный ключ RSA."""

    modulus: int
    exponent: int


@dataclass(frozen=True)
class RSAPrivateKey:
    """Закрытый ключ RSA."""

    modulus: int
    exponent: int


@dataclass(frozen=True)
class RSAKeyPair:
    """Пара ключей RSA."""

    public: RSAPublicKey
    private: RSAPrivateKey


def generate_rsa_keypair(bit_size: int = 2048, *, public_exponent: int = 65537) -> RSAKeyPair:
    """Генерирует пару RSA-ключей заданной длины."""

    if bit_size < 16:
        raise ValueError("Размер ключа должен быть не меньше 16 бит")

    half = bit_size // 2
    while True:
        p = generate_prime(half)
        q = generate_prime(bit_size - half)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if math.gcd(public_exponent, phi) == 1:
            break

    n = p * q
    d = mod_inverse(public_exponent, phi)
    return RSAKeyPair(
        public=RSAPublicKey(modulus=n, exponent=public_exponent),
        private=RSAPrivateKey(modulus=n, exponent=d),
    )


def _int_to_bytes(value: int) -> bytes:
    if value == 0:
        return b"\x00"
    length = (value.bit_length() + 7) // 8
    return value.to_bytes(length, "big")


def _bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, "big")


def encrypt(message: bytes, key: RSAPublicKey) -> bytes:
    """Шифрует сообщение (сырые байты)."""

    message_int = _bytes_to_int(message)
    if message_int >= key.modulus:
        raise ValueError("Размер сообщения превышает модуль ключа")
    cipher_int = pow(message_int, key.exponent, key.modulus)
    return _int_to_bytes(cipher_int)


def decrypt(ciphertext: bytes, key: RSAPrivateKey) -> bytes:
    """Дешифрует сообщение, полученное с помощью :func:`encrypt`."""

    cipher_int = _bytes_to_int(ciphertext)
    message_int = pow(cipher_int, key.exponent, key.modulus)
    return _int_to_bytes(message_int)


def encrypt_text(message: str, key: RSAPublicKey, *, encoding: str = "utf-8") -> bytes:
    """Удобная обёртка для текстовых сообщений."""

    return encrypt(message.encode(encoding), key)


def decrypt_text(ciphertext: bytes, key: RSAPrivateKey, *, encoding: str = "utf-8") -> str:
    """Декодирует байтовое представление в строку."""

    return decrypt(ciphertext, key).decode(encoding)


def demo(bits: int, message: str | None) -> None:
    key_pair = generate_rsa_keypair(bits)
    print(f"Сгенерирован ключ длиной {bits} бит\n")
    print("Публичный ключ:")
    print(f"  n = {key_pair.public.modulus}")
    print(f"  e = {key_pair.public.exponent}\n")
    print("Приватный ключ:")
    print(f"  n = {key_pair.private.modulus}")
    print(f"  d = {key_pair.private.exponent}\n")

    if message is None:
        return

    ciphertext = encrypt_text(message, key_pair.public)
    decrypted = decrypt_text(ciphertext, key_pair.private)

    print("Сообщение:", message)
    print("Шифротекст (hex):", ciphertext.hex())
    print("Расшифровка:", decrypted)


def main() -> None:
    parser = argparse.ArgumentParser(description="Учебный демо-скрипт RSA")
    parser.add_argument(
        "--bits", type=int, default=512, help="Размер генерируемого ключа"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Текст для шифрования и обратного расшифрования",
    )
    args = parser.parse_args()
    demo(args.bits, args.message)


if __name__ == "__main__":
    main()

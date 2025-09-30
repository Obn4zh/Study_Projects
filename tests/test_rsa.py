import pytest

from study_crypto import (
    decrypt,
    decrypt_text,
    encrypt,
    encrypt_text,
    generate_rsa_keypair,
)


def test_encrypt_decrypt_roundtrip():
    pair = generate_rsa_keypair(256)
    message = b"test message"

    ciphertext = encrypt(message, pair.public)
    assert decrypt(ciphertext, pair.private) == message


def test_encrypt_text_roundtrip():
    pair = generate_rsa_keypair(256)
    message = "привет"

    ciphertext = encrypt_text(message, pair.public)
    assert decrypt_text(ciphertext, pair.private) == message


def test_message_too_long_raises():
    pair = generate_rsa_keypair(256)
    byte_length = (pair.public.modulus.bit_length() + 7) // 8
    message = pair.public.modulus.to_bytes(byte_length, "big")

    with pytest.raises(ValueError):
        encrypt(message, pair.public)

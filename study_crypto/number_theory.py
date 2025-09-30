"""Вспомогательные функции теории чисел для криптографии."""

from __future__ import annotations

from secrets import randbelow, randbits
from typing import Tuple

_SMALL_PRIMES = (
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
)


def _decompose(n: int) -> Tuple[int, int]:
    """Возвращает (s, d) такое, что n = 2**s * d и d нечётное."""
    s = 0
    d = n
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d


def is_probable_prime(n: int, *, rounds: int = 16) -> bool:
    """Проверяет число на простоту тестом Миллера–Рабина.

    Для целей учебного проекта используем вероятностную проверку с 16 раундами,
    что даёт астрономически малую вероятность ошибки для 512+ бит.
    """

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for prime in _SMALL_PRIMES:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    s, d = _decompose(n - 1)
    for _ in range(rounds):
        a = randbelow(n - 3) + 2  # [2, n-2]
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(num_bits: int) -> int:
    """Генерирует вероятно простое число заданной битовой длины."""

    if num_bits < 2:
        raise ValueError("Размер простого числа должен быть >= 2 бит")

    while True:
        candidate = randbits(num_bits)
        # гарантируем нужную битовую длину и нечётность
        candidate |= 1
        candidate |= 1 << (num_bits - 1)
        if is_probable_prime(candidate):
            return candidate


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Расширенный алгоритм Евклида: gcd, x, y такие, что ax + by = gcd."""

    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(value: int, modulo: int) -> int:
    """Обратный элемент по модулю."""

    gcd, x, _ = egcd(value, modulo)
    if gcd != 1:
        raise ValueError("Обратного элемента не существует")
    return x % modulo


__all__ = ["generate_prime", "is_probable_prime", "mod_inverse"]

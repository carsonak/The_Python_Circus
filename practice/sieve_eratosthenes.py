#!/usr/bin/python3
"""Module for sieve_eratosthenes."""
from math import isqrt


def primes_less_than(n: int) -> list[int]:
    """Find prime numbers less than a given int.

    Warning!
        Memory intesive for high values of n
    """

    if n <= 2:
        return []
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, isqrt(n)+1):
        if is_prime[i]:
            for x in range(i*i, n, i):
                is_prime[x] = False

    return [i for i in range(n) if is_prime[i]]


if __name__ == '__main__':
    print(primes_less_than(100))

"""Defines functions to generate prime numbers"""


from collections.abc import Generator


def prime_gen() -> Generator[int, None, None]:
    """Prime number generator"""

    prime_list = []

    n = 2

    while True:

        yield n

        prime_list.append(n)
        n += 1
        while any(n % prime == 0 for prime in prime_list):
            n += 1


_cache = {2: [], 3: [2]}


def primes_to_n(n: int) -> list[int]:
    """Return all primes less than or equal to n using cache"""

    if n in _cache:
        return _cache[n]

    primes = []

    for i in range(2, n):
        max_factor = int(pow(i, 0.5) + 1)
        factors = primes_to_n(max_factor)
        if all(i % factor for factor in factors):
            primes.append(i)

    _cache[n] = primes

    return primes


def primes_to_n_2(n: int) -> list[int]:
    """Return all primes less than or equal to n by keeping track
    of smaller primes
    """

    primes: list[int] = []

    for i in range(2, n):

        max_factor = int(pow(i, 0.5) + 1)
        is_prime = True

        for p in primes:
            if p > max_factor:
                break
            if i % p == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(i)

    return primes


if __name__ == '__main__':
    print(primes_to_n(100))
    print(primes_to_n_2(100))

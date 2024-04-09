import itertools
from config import command_args

def sieve(ints):
    prime = next(ints)
    yield prime
    not_divisible = filter(lambda x: x % prime, ints)
    for p in sieve(not_divisible):
        yield p

primes = sieve(itertools.count(2))


def prime_gen():
    prime_list = []
    n = 2
    while True:
        yield n
        prime_list.append(n)
        n += 1
        while any([n % prime == 0 for prime in prime_list]):
            n += 1

#pg = prime_gen()
#for i in range(10): print pg.next()
        
_cache = {2: [], 3: [2]}
        
def primes_to_n(n):

    if command_args.debug:
        print(f'calling primes_to_n({n})')

    if n in _cache:
        return _cache[n]

    if command_args.debug:
        print(f'{n} not yet cached for primes_to_n')

    primes = list()

    for i in range(2, n):
        max_factor = int(pow(i, 0.5) + 1)
        factors = primes_to_n(max_factor)
        if all(i % factor for factor in factors):
            primes.append(i)

    _cache[n] = primes

    return primes

def primes_to_n_2(n):

    primes = list()

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

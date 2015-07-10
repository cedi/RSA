from collections import namedtuple
from fractions import gcd
from random import randrange

PrimesPair = namedtuple('PrimesPair', 'p q')
KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'RSA exponent')


def is_prime(number):
    if number is 0 or number is 1:
        return False

    # http://de.wikipedia.org/wiki/Sieb_des_Eratosthenes

    primes = []

    # Array initalisieren
    for i in range(number + 1):
        primes.append(True)

    # 0 und 1 von vorne herein ausschließen
    primes[0] = False
    primes[1] = False

    # Alle vielfachen von number sind können ausgeschlossen werden

    for i in range(number + 1):
        if primes[i] is True:
            j = 2 * i
            while j <= number:
                primes[j] = False
                j += i

    return primes[number] is True

    for i in range(len(primes)):
        print("{0}: {1}".format(i, primes[i]))


def multinv(modulus, value):
    # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x

    result = (1 - lastx * modulus) // value

    if result < 0:
        result += modulus

    assert 0 <= result < modulus and value * result % modulus == 1

    return result


def possible_prime_generator(rsa):
    for i in range(rsa):
        if is_prime(i) is False:
            continue

        if rsa % i is not 0:
            continue

        possible_p = i
        possible_q = int(rsa / i)

        yield PrimesPair(p=possible_p, q=possible_q)

    raise StopIteration


def generate_keys(p, q, publicE):
    RSAModule = p * q
    phi = (p - 1) * (q - 1)

    private = int()
    public = int()

    while True:
        while True:
            private = randrange(phi)
            if gcd(private, phi) == 1:
                break

        public = multinv(phi, private)
        if public != publicE:
            continue

        privateKey = Key(RSA=RSAModule, exponent=private)
        publicKey = Key(RSA=RSAModule, exponent=public)

        return KeyPair(public=publicKey, private=privateKey)

# ----------- Main -----------

RSA = input("RSA Module N: ")
publicE = input("Öffentlicher Exponent e: ")

try:
    RSA = int(RSA)
    publicE = int(publicE)
except TypeError:
    exit(1)

possible_primes = []
possible_keys = []

for prime_pair in possible_prime_generator(RSA):
    append = True
    for pair in possible_primes:
        if pair.p == prime_pair.q or pair.q == prime_pair.p:
            append = False

    if append is True:
        possible_primes.append(prime_pair)
        print(prime_pair)

for prime_pair in possible_primes:
    p = prime_pair.p
    q = prime_pair.q

    keyPair = generate_keys(p, q, publicE)
    print(keyPair)

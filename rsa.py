import random


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)
    d = pow(e, -1, phi)
    return (n, e), (n, d)


def encrypt(message, public_key):
    n, e = public_key
    ciphertext = [chr(pow(ord(char), e, n)) for char in message]
    return ''.join(ciphertext)


def decrypt(ciphertext, private_key):
    n, d = private_key
    plaintext = [chr(pow(ord(char), d, n)) for char in ciphertext]
    return ''.join(plaintext)

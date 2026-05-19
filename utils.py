import random
import json

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_random_prime(lower: int, upper:int) -> int:
    while True:
        p = random.randint(lower, upper)
        if is_prime(p):
            return p

def mod_inverse(e: int, phi: int) -> int:
    def extended_gcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = extended_gcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("No modular inverse exists")
    return x % phi

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def generate_keys(p: int = None, q: int = None):
    while True:
        p = get_random_prime(1, 20) if p is  None else p
        q = get_random_prime(1, 20) if q is None else q

        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537
        if gcd(e, phi) != 1:
            continue

        d = mod_inverse(e, phi)
        return RSAKeyPair(public_key=(e, n), private_key=(d, n)), n, phi


class RSAKeyPair:
    def __init__(self, public_key: tuple[int, int], private_key: tuple[int, int]):
        self.public = public_key
        self.private = private_key

    def encrypt(self, message: str):
        e, n = self.public

        ciphertext = []
        steps = []

        for char in message:
            m = ord(char)
            c = pow(m, e, n)

            ciphertext.append(c)
            steps.append({
                "char": char,
                "m": m,
                "operation": f"{m}^{e} mod {n}",
                "cipher": c
            })

        return ciphertext, steps

    def decrypt(self, ciphertext: list[str]):
        d, n = self.private

        plaintext = ""
        steps = []

        for c in ciphertext:
            m = pow(c, d, n)
            char = chr(m)

            plaintext += char
            steps.append({
                "cipher": c,
                "operation": f"{c}^{d} mod {n}",
                "m": m,
                "char": char
            })

        return plaintext, steps


    
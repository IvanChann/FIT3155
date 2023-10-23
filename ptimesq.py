import random

def miller_rabin_test(n, k=5):
    if n < 2:
        return False
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def karatsuba_multiply(x, y):
    if x < 10 or y < 10:
        return x * y
    
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    a, b = divmod(x, 10**m)
    c, d = divmod(y, 10**m)

    ac = karatsuba_multiply(a, c)
    bd = karatsuba_multiply(b, d)
    ad_plus_bc = karatsuba_multiply(a+b, c+d) - ac - bd

    return ac * 10**(2*m) + ad_plus_bc * 10**m + bd

def generate_n_bit_random_number(n):
    return random.randint(2**(n-1), 2**n - 1)

def generate_n_bit_prime(n):
    while True:
        candidate = generate_n_bit_random_number(n)
        if miller_rabin_test(candidate):
            return candidate

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ptimesq.py <n>")
        sys.exit(1)

    n = int(sys.argv[1])

    if not (32 <= n <= 2046):
        print("n should be between 32 and 2046.")
        sys.exit(1)

    p, q = generate_n_bit_prime(n), generate_n_bit_prime(n)
    while p == q:
        q = generate_n_bit_prime(n)

    product = karatsuba_multiply(p, q)

    with open('output_ptimesq.txt', 'w') as f:
        f.write(f"{p}\n")
        f.write(f"{q}\n")
        f.write(f"{product}\n")

    print(f"Results written to output_ptimesq.txt")

import random
import sys

def gen_n_bit_random_number(n):
    # OR (1 << (n-1)) ensures MSB is 1 so size is guaranteed n bits
    # OR 1 guarantees it odd (LSB = 1)
    return random.getrandbits(n) | (1 << (n-1)) | 1

def gen_n_bit_prime(n):
    while True:
        candidate = gen_n_bit_random_number(n)
        if miller_rabin_test(candidate):
            return candidate

def modular_exponentiation(a, b, n):
    binary_rep = bin(b)[2:] # convert b to its binary representation
    
    # Base case
    current = a % n
    if binary_rep[-1] == "1" :  # last element is LSB
        result = current
    else:
        result = 1

    # Iterating through remaining bits in the binary representation in reverse
    for current_bit in reversed(binary_rep[:-1]):
        # Compute the next term in the sequence
        current = (current * current) % n
        if current_bit == "1":
            # update result
            result = (result * current) % n

    return result


# function for miller rabin test
# returns true for probably prime, false for composite
def miller_rabin_test(n, k=5):
    # special cases
    if n == 2 or n == 3:
        return True
    # only testing odd integers (can technically skip as gen_n_bit_random_number only generates odd numbers)
    if n % 2 == 0:
        return False
    # Factor n-1 as (2^s)*t, where t is odd
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    # running k random tests
    for _ in range(k):
        # selecting random witness
        a = random.randint(2, n - 2)

        # Compute the sequence [x_0, x_1, ... , x_s] with modular exponentiation by repeated squaring
        x_values = [modular_exponentiation(a, t, n)] # modular expontentiation to calculate a ^ t mod n
        for _ in range(s):
            x_values.append((x_values[-1] * x_values[-1]) % n)

        # Check if n satisfies Fermat’s little theorem for this witness
        if x_values[-1] != 1:
            return False

        # Run the sequence test
        for j in range(1, s + 1):
            if x_values[j] == 1 and (x_values[j - 1] != 1 and x_values[j - 1] != n - 1):
                return False

    # n has passed all tests so probably prime
    return True


# recursive implementation of karatsuba multiplication in base 10
def karatsuba_multiply(u, v):
    # base case
    if u < 10 or v < 10:
        return u * v
    
    n = max(len(str(u)), len(str(v))) # getting max digits
    m = n // 2

    # splitting u and v, divmod returns quotient and remainder
    u_1, u_0 = divmod(u, 10**m) 
    v_1, v_0 = divmod(v, 10**m)

    return (10**(2*m) + 10**m) * karatsuba_multiply(u_1, v_1) - 10**m * karatsuba_multiply(u_1 - u_0, v_1 - v_0) + (10**m + 1) * karatsuba_multiply(u_0, v_0)

        

if __name__ == "__main__":   
    n = int(sys.argv[1])
    
    if not (32 <= n <= 2046):
        print("n should be between 32 and 2046")
        sys.exit(1)

    p, q = gen_n_bit_prime(n), gen_n_bit_prime(n)
    while p == q:
        q = gen_n_bit_prime(n)

    product = karatsuba_multiply(p, q)  

    with open('output_ptimesq.txt', 'w') as file:
        file.write(f"#p (in base 10)]\n{p}\n\n")
        file.write(f"#q (in base 10)\n{q}\n\n")
        file.write(f"p*q (in base 10)\n{product}\n")

    print(f"Results written to output_ptimesq.txt")

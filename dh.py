import random

def calculate_public_key(p, g, private_key):
    return pow(g, private_key, p)

def calculate_shared_secret(p, public_key, private_key):
    return pow(public_key, private_key, p)

def record_calculation(p, g, private_key, public_key, shared_secret):
    print("p =", p)
    print("g =", g)
    print("Private Key:", private_key)
    print("Public Key:", public_key)
    print("Shared Secret:", shared_secret)
    print("------------------------")

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_primitive_root(p):
    primitive_roots = []
    for g in range(2, p):
        is_primitive_root = True
        for i in range(1, p - 1):
            if pow(g, i, p) == 1:
                is_primitive_root = False
                break
        if is_primitive_root:
            primitive_roots.append(g)
    return primitive_roots

# 表格中的p和g值
values = [
    (101, 2),
    (103, 5),
    (107, 2),
    (109, 6),
    (113, 3),
    (127, 3),
    (131, 2),
    (137, 3),
    (139, 2),
    (149, 2),
    (151, 6),
    (157, 5),
    (163, 2),
    (167, 5),
    (173, 2),
    (179, 2),
    (181, 2),
    (191, 19),
    (193, 5),
    (197, 2),
    (199, 3),
    (211, 2),
    (223, 3),
    (227, 2),
    (229, 6),
    (233, 3),
    (239, 7),
    (241, 7),
    (251, 6)
]

for p, g in values:
    # A和B生成各自的私钥
    private_key_A = random.randint(2, p - 2)
    private_key_B = random.randint(2, p - 2)

    # A和B计算各自的公钥
    public_key_A = calculate_public_key(p, g, private_key_A)
    public_key_B = calculate_public_key(p, g, private_key_B)

    # A和B交换各自的公钥，并计算共享密钥
    shared_secret_A = calculate_shared_secret(p, public_key_B, private_key_A)
    shared_secret_B = calculate_shared_secret(p, public_key_A, private_key_B)

    # 记录计算过程
    record_calculation(p, g, private_key_A, public_key_A, shared_secret_A)
    record_calculation(p, g, private_key_B, public_key_B, shared_secret_B)



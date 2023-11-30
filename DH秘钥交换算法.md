# D-H秘钥交换算法

##### 1、概述

​	在对称加密算法中,加密和解密使用的都是同一把秘钥,把加密后的密文放在网络上传输是可以的,如果密文泄露了,没有秘钥是得不到原始内容的。但如果秘钥也通过网络传输,一旦秘钥泄露,就可能会通过秘钥对密文进行解密,使得原始内容泄露。为了安全地将秘钥和密文传输到解密方进行解密,可以采用D-H秘钥交换算法。

##### 2、D-H秘钥交换算法

​	D-H秘钥交换算法并没有将真正的秘钥放在网络中传输,而是双方通过一种协商和数学推导的方式来得到共同的秘钥。

![image-20231126220220310](C:\Users\liangyuxin\AppData\Roaming\Typora\typora-user-images\image-20231126220220310.png)

​	如上图所示, 加密和解密双方都会拥有自己的私钥和公钥,公钥是公开的,私钥是只有自己知道的,Alice将自己的私钥与g,p两个参数进行计算得到自己的公钥,然后将自己的公钥和g,p两个参数通过网络发送给Bob,Bob根据Alice发送的g,p参数与自己的私钥进行相同计算得到他的公钥,再将他的公钥发送给Alice,最后,双方根据各自的私钥与对方发送来的公钥进行相同的数学计算得到共享秘钥(真正进行加密和解密的秘钥)。

​	例如:Alice的私钥是a=123,取p=509,g=5通过5^123mod 509进行与运算和求余得到公钥A=215,然后Alice将A=215,p=509,g=5发送给Bob，假设Bob的私钥b=456,Bob进行相同的运算5^456 mod 509得到自己的公钥B=181并发送给Alice,Alice根据自己的私钥a与Bob的公钥B进行B^a mod p进行计算得到结果121,Bob根据自己的私钥b与Alice的公钥A进行A^b mod p得到相同的结果121;

​	从上面的推导过程中看到,在网络传输中并没有传输关于真正秘钥的内容,而是双方将各自的公钥发送给对方,通过类似于协商的方式得到共同的秘钥。

##### 3、实现DH交换算法

```
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
```

运行结果记录如下: 

 从运行结果中看到,虽然Alice和Bob的私钥,公钥都不相同,但通过协商计算出了相同的秘钥,在后来的加密算法中,Alice和Bob就可以使用计算出的秘钥进行相应的加密和解密操作了。DH算法就是一种秘钥交换算法,双方在不安全的环境中协商出一个秘钥,防止秘钥在传输过程泄露。 

| P    | g    | A-private key | A-public key | B-private key | B-public key | shared secret |
| ---- | ---- | ------------- | ------------ | ------------- | ------------ | ------------- |
| 101  | 2    | 99            | 51           | 5             | 32           | 60            |
| 103  | 5    | 101           | 62           | 100           | 33           | 25            |
| 107  | 2    | 74            | 48           | 100           | 102          | 49            |
| 109  | 6    | 22            | 104          | 60            | 105          | 38            |
| 113  | 3    | 110           | 88           | 108           | 60           | 7             |
| 127  | 3    | 75            | 54           | 13            | 92           | 89            |
| 131  | 2    | 116           | 102          | 118           | 15           | 21            |
| 137  | 3    | 107           | 86           | 119           | 41           | 10            |
| 139  | 2    | 13            | 130          | 48            | 106          | 131           |
| 149  | 2    | 33            | 109          | 10            | 130          | 69            |
| 151  | 6    | 34            | 58           | 113           | 30           | 80            |
| 157  | 5    | 15            | 79           | 118           | 140          | 143           |
| 163  | 2    | 158           | 51           | 45            | 125          | 53            |
| 167  | 5    | 147           | 51           | 119           | 35           | 90            |
| 173  | 2    | 142           | 137          | 162           | 37           | 133           |
| 179  | 2    | 171           | 7            | 93            | 163          | 105           |
| 181  | 2    | 138           | 152          | 34            | 60           | 114           |
| 191  | 19   | 162           | 65           | 2             | 170          | 23            |
| 193  | 5    | 54            | 69           | 190           | 139          | 3             |
| 197  | 2    | 50            | 169          | 153           | 108          | 64            |
| 199  | 3    | 28            | 16           | 34            | 122          | 79            |
| 211  | 2    | 96            | 143          | 56            | 100          | 188           |
| 223  | 3    | 200           | 218          | 101           | 160          | 124           |
| 227  | 2    | 81            | 138          | 71            | 146          | 68            |
| 229  | 6    | 32            | 55           | 65            | 59           | 196           |
| 233  | 3    | 100           | 225          | 182           | 31           | 51            |
| 239  | 7    | 111           | 79           | 193           | 236          | 104           |
| 241  | 7    | 39            | 140          | 26            | 77           | 116           |
| 251  | 6    | 171           | 62           | 90            | 51           | 125           |


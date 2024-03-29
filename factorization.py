# pylint: disable = C0103, W0105
import typing

import gmpy2
import tqdm
from Crypto.Util.number import GCD, isPrime


def fermat(n: int) -> tuple[int, int]:
    a = gmpy2.isqrt(n) + 1
    b = a ** 2 - n
    while not gmpy2.iroot(b, 2)[1]:
        a += 1
        b = a ** 2 - n
    b = gmpy2.iroot(b, 2)[0]
    return (a + b, a - b)


def pollard(n: int) -> int:
    a, b = 2, 2
    while True:
        a = pow(a, b, n)
        p = GCD(a - 1, n)
        if 1 < p < n:
            return p
        b += 1


def williams(n: int, *, B: int | None = None) -> int:
    """B is the largest prime of the factors of p + 1 or p - 1"""
    def gen_prime() -> typing.Generator[int, None, None]:
        yield 3
        i = 5
        while True:
            if isPrime(i):
                yield i
            if isPrime(i + 2):
                yield i + 2
            i += 6

    def mlucas(b: int, k: int) -> int:
        """It returns k-th V(b, 1)"""
        v1, v2 = b % n, (b ** 2 - 2) % n
        for bit in bin(k)[3:]:
            if int(bit):
                v1, v2 = (v1 * v2 - b) % n, (v2 ** 2 - 2) % n
            else:
                v1, v2 = (v1 ** 2 - 2) % n, (v1 * v2 - b) % n
        return v1

    B = B or int(gmpy2.isqrt(n))
    for A in tqdm.tqdm(gen_prime(), disable=True):
        v = A
        for i in tqdm.trange(1, B + 1, desc=f"A={A}"):
            v = mlucas(v, i)
            g = GCD(v - 2, n)
            if g > 1:
                return g

"""
Williams Example:
    # wiki
    n = 112729
    print(williams(n, B=29))

    # p-1 smooth
    n = 89440560733164708153845415331446945959245098008966030018929526224499627757561588031620648168516773823431871418356339994635745869093527493722219078655396271734959826773338477957209319942403927521493751796095337134761865520104013849636230344195374484615442639465418351367038754528133862123415585916462336887316272609032894837016897778296130831547243876103719134564487881368375292269727492130954469891687595162077285957074426084146076230091131943856427238665819605762639
    print(williams(n, B=1<<12))

    # p+1 smooth
    n = 51996076692048722302761900056642680476540015543011479312413059393488457763604721208727469678078786799742029838329267567796783526516547183269392673162252396292776337638007225267519370228310303179305074137400073891412356919163377467538074363929453978888588967493488244070876029795039400793907625514218173531182370548791155690999213414133504593716651097967429440004150821114887337079235761030322095935699448009093502038952349191429234699268848426170302694760098881388267364694899579002895901602821456241740399012210807870408183763369948426609487
    print(williams(n, B=1<<16))
"""

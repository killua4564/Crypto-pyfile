import functools
import itertools
import typing

import gmpy2
from Crypto.Util.number import inverse


@functools.cache
def chinese_remainder(n: tuple[int], r: tuple[int]) -> int:
    result = 0
    prod = functools.reduce(lambda a, b: a * b, n)
    for ni, ri in zip(n, r):
        Ni = prod // ni  # pylint: disable=C0103
        result += ri * inverse(Ni, ni) * Ni
    return result % prod


@functools.cache
def legendre_symbol(a: int, p: int) -> int:
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


@functools.cache
def tonelli_shanks(a: int, p: int) -> int | None:
    a = a % p
    if a in (0, 1):
        return a

    if p == 2 or legendre_symbol(a, p) != 1:
        return None

    if p % 4 == 3:  # p + 1 mod 4 = 0
        # a ** (p - 1) / 2 = 1
        # ==> a ** (p + 1) / 2 = a
        # ==> (a ** (p + 1) / 4) ** 2 = a
        return pow(a, (p + 1) // 4, p)

    # find quadratic nonresidue
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1

    # factor p - 1 into Q * 2 ** S
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    c = pow(z, q, p)
    m = s

    while True:
        # find R ** 2 = nt and t = 1
        if t == 1:
            return r

        # find least i to try
        i = 0
        while pow(t, 2 ** i, p) != 1:
            i += 1

        b = pow(c, 2 ** (m - i - 1), p)

        # because of R ** 2 = n * t * b ** 2, so t = t * b ** 2
        r = r * b % p
        t = t * pow(b, 2, p) % p

        # c = pow(c, 2 ** (m - i), p), and keep power inside p-1
        c = pow(b, 2, p)
        m = i


def power2roots(a: int, modulars: typing.Iterable[int], k: int) -> typing.Generator[int, None, None]:
    if k == 0: 
        yield a
        return

    for i in power2roots(a, modulars, k - 1):
        remainders: tuple[int | None] = tuple(tonelli_shanks(i, p) for p in modulars)
        if not all(remainders):
            return

        for remainder in itertools.product(*[
            (r, m - r) for m, r in zip(modulars, remainders)
        ]):
            yield chinese_remainder(modulars, remainder)


def main():
    e = 8
    n = 36698059413399807859498533311
    c = 29390284442190568750119061394  # pow(m, e, n)
    modulars: tuple[int] = (2620668341, 3528051199, 3969137629)
    for m in power2roots(c, modulars, int(gmpy2.log2(e))):
        assert pow(m, e, n) == c
        print(m)


if __name__ == "__main__":
    main()

import functools

import gmpy2
import tqdm
from Crypto.Util.number import GCD, inverse


def chinese_remainder(n: tuple[int], r: tuple[int]) -> int:
    result = 0
    prod = functools.reduce(lambda a, b: a * b, n)
    for ni, ri in zip(n, r):
        Ni = prod // ni
        result += ri * inverse(Ni, ni) * Ni
    return result % prod


def pohlig_hellman(g: int, h: int, p: int, factors: tuple[tuple[int, int]]) -> int:
    """baby-step giant-step
    1. restore pow(g, k * sqrt(n), p)
    2. match i with h * pow(g, i, p) % p
    3. return x = (k * sqrt(n) - i) % n
    """
    def baby_giant(g: int, h: int, n: int) -> int:
        giant: dict[int, int] = {}
        sqrt = int(gmpy2.isqrt(n)) + 1

        gs, gks = pow(g, sqrt, p), 1
        for k in tqdm.trange(sqrt, leave=False):
            giant[gks] = k
            gks = gks * gs % p

        for i in tqdm.trange(sqrt, leave=False):
            try:
                k = giant[h]
                return (k * sqrt - i) % n
            except KeyError:
                h = h * g % p

        raise ValueError(f"Can't find ord in subgroup {n}")

    """pollard's rho
    1. check g == h to avoid b1 == b2
    2. calculate until x_i == x_2i
    """
    def pollard_rho(g: int, h: int, n: int) -> int:
        def new(x: int, a: int, b: int) -> tuple[int]:
            if x % 3 == 1:
                return (g * x % p, (a + 1) % n, b)
            if x % 3 == 2:
                return (h * x % p, a, (b + 1) % n)
            return (x * x % p, 2 * a % n, 2 * b % n)

        if g == h:
            return 1

        x1, a1, b1 = 1, 0, 0
        x2, a2, b2 = 1, 0, 0
        for _ in tqdm.trange(n, leave=False):
            x1, a1, b1 = new(x1, a1, b1)
            x2, a2, b2 = new(x2, a2, b2)
            x2, a2, b2 = new(x2, a2, b2)
            if x1 == x2:
                r = inverse(b2 - b1, n) // GCD(b2 - b1, n)
                return (a1 - a2) * r % n

        raise ValueError(f"Can't find ord in subgroup {n}")

    ords = []

    """if all factors are one power
    for pi, _ in factors:
        gi = pow(g, (p - 1) // pi, p)
        hi = pow(h, (p - 1) // pi, p)
        ords.append(baby_giant(gi, hi, pi))
    """

    g_inv = inverse(g, p)
    for pi, power in factors:
        gi, xi = pow(g, (p - 1) // pi, p), 0
        for j in range(power):
            hi = h * pow(g_inv, xi, p) % p
            hj = pow(hi, (p - 1) // pi ** (j + 1), p)
            xi += baby_giant(gi, hj, pi) * pi ** j
        ords.append(xi)

    return chinese_remainder(
        tuple(i ** j for i, j in factors), tuple(ords),
    )


def main():
    p = 0xfffffed83c17
    g = 5
    h = 103547092903557

    factors: tuple[tuple[int, int]] = (
        (2, 1), (3, 2), (7, 1), (13, 4),
        (47, 1), (103, 1), (107, 1), (151, 1),
    )

    x = pohlig_hellman(g, h, p, factors)
    assert pow(g, x, p) == h
    print(x)


if __name__ == "__main__":
    main()

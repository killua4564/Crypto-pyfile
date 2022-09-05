import functools
import typing


class LFSR:
    SIZE: int = 16

    register: int
    taps: typing.Tuple[int]

    def __init__(
        self,
        register: int,
        taps: typing.Iterable[int],
    ):
        self.register = register
        if not 0 < self.register < (1 << self.SIZE):
            raise ValueError(f"0 < register <= {1 << self.SIZE}")

        self.taps = tuple(set(taps))
        if not all(0 < tap <= self.SIZE for tap in self.taps):
            raise ValueError(f"0 < tag <= {self.SIZE}")

    def next(self):
        raise NotImplementedError


class FibonacciLFSR(LFSR):
    def next(self) -> int:
        bit: int = functools.reduce(lambda x, y: x ^ y, (
            (self.register >> (self.SIZE - tap)) & 1
            for tap in self.taps
        ))
        ret: int = self.register & 1
        self.register = (bit << (self.SIZE - 1)) | (self.register >> 1)
        return ret


class GaloisLFSR(LFSR):
    mask: int

    def __init__(
        self,
        register: int,
        taps: typing.Iterable[int],
    ):
        super().__init__(register, taps)
        self.mask = 0
        for tap in self.taps:
            self.mask |= (1 << (self.SIZE - tap))

    def next(self) -> int:
        ret: int = self.register & 1
        self.register >>= 1
        self.register ^= ret * self.mask
        return ret


if __name__ == "__main__":
    print("FibonacciLFSR")
    lfsr = FibonacciLFSR(0xACE1, [1, 4, 13, 15, 16])
    for _ in range(16):
        print("{:016b}".format(lfsr.register))
        lfsr.next()

    print("GaloisLFSR")
    lfsr = GaloisLFSR(0xACE1, [1, 4, 13, 15, 16])
    for _ in range(16):
        print("{:016b}".format(lfsr.register))
        lfsr.next()

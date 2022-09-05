class DES:
    ROUNDS: int = 16

    IP: list[int] = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17,  9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
    ]

    FP: list[int] = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41,  9, 49, 17, 57, 25,
    ]

    E: list[int] = [
        32,  1,  2,  3,  4,  5,
         4,  5,  6,  7,  8,  9,
         8,  9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32,  1,
    ]

    P: list[int] = [
        16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25,
    ]

    PC1: list[int] = [
        57, 49, 41, 33, 25, 17,  9,
         1, 58, 50, 42, 34, 26, 18,
        10,  2, 59, 51, 43, 35, 27,
        19, 11,  3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,
        21, 13,  5, 28, 20, 12,  4,
    ]

    PC2: list[int] = [
        14, 17, 11, 24,  1,  5,
         3, 28, 15,  6, 21, 10,
        23, 19, 12,  4, 26,  8,
        16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32,
    ]

    PC_shift: list[int] = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1,
    ]

    S_BOX: list[list[list[int]]] = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ],
    ]

    def __init__(self, key: bytes):
        self.round_keys: list[bytes] = self.generate_round_keys(key)

    @classmethod
    def _box(cls, state: bytes, box: list[int]) -> bytes:
        result: int = 0
        bits: int = len(state) * 8
        state: int = int.from_bytes(state, byteorder="big")
        for elem in box:
            result <<= 1
            result += (state >> (bits - elem)) & 1
        return result.to_bytes(len(box) // 8, byteorder="big")

    @classmethod
    def _ceil(cls, x: float) -> int:
        if int(x) == x:
            return int(x)
        return int(x) + 1

    @classmethod
    def _join(cls, left: bytes, right: bytes, ignore: int = 0) -> bytes:
        bits: int = (len(left) + len(right)) * 8 // 2 - ignore
        left: int = int.from_bytes(left, byteorder="big")
        right: int = int.from_bytes(right, byteorder="big")
        return ((left << bits) + right).to_bytes(bits * 2 // 8, byteorder="big")

    @classmethod
    def _mask(cls, bits: int) -> int:
        return (1 << bits) - 1

    @classmethod
    def _s_box(cls, state: bytes, length: int = 4) -> bytes:
        result: int = 0
        bits: int = len(state) * 8 // len(cls.S_BOX)
        boxes: int = len(cls.S_BOX)
        state: int = int.from_bytes(state, byteorder="big")
        for idx in range(boxes):
            result <<= length
            _state: int = (state >> ((boxes - idx - 1) * bits)) & cls._mask(bits)
            _row: int = (((_state >> 5) & 1) << 1) + (_state & 1)
            _column: int = (_state >> 1) & cls._mask(length)
            result += cls.S_BOX[idx][_row][_column]
        return result.to_bytes(length, byteorder="big")

    @classmethod
    def _shift(cls, state: bytes, shift: int, ignore: int = 0) -> bytes:
        bits: int = len(state) * 8 - ignore
        state: int = int.from_bytes(state, byteorder="big")
        state = ((state << shift) | (state >> (bits - shift))) & cls._mask(bits)
        return state.to_bytes((bits + ignore) // 8, byteorder="big")

    @classmethod
    def _split(cls, state: bytes) -> (bytes, bytes):
        bits: int = len(state) * 8 // 2
        state: int = int.from_bytes(state, byteorder="big")
        left, right = (state >> bits) & cls._mask(bits), state & cls._mask(bits)
        return (
            left.to_bytes(cls._ceil(bits / 8), byteorder="big"),
            right.to_bytes(cls._ceil(bits / 8), byteorder="big"),
        )

    @classmethod
    def _xor(cls, x: bytes, y: bytes) -> bytes:
        return bytes(i ^ j for i, j in zip(x, y))

    @classmethod
    def generate_round_keys(cls, state: bytes) -> list[bytes]:
        round_keys: list[bytes] = []
        left, right = cls._split(cls._box(state, cls.PC1))
        for idx in range(cls.ROUNDS):
            left = cls._shift(left, cls.PC_shift[idx], ignore=4)
            right = cls._shift(right, cls.PC_shift[idx], ignore=4)
            round_keys.append(cls._box(cls._join(left, right, ignore=4), cls.PC2))
        return round_keys

    @classmethod
    def F(cls, state: bytes, key: bytes) -> bytes:
        state = cls._xor(cls._box(state, cls.E), key)
        state = cls._s_box(state)
        state = cls._box(state, cls.P)
        return state

    def encrypt(self, plaintext: bytes) -> bytes:
        left, right = self._split(self._box(plaintext, self.IP))
        for idx in range(self.ROUNDS):
            key: bytes = self.round_keys[idx]
            left, right = right, self._xor(left, self.F(right, key))
        return self._box(self._join(right, left), self.FP)


if __name__ == "__main__":
    k = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6])
    p = bytes([0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d])
    c = bytes([0x61, 0xcb, 0x4a, 0x69, 0xbf, 0xcc, 0x9b, 0xc4])
    assert DES(k).encrypt(p) == c

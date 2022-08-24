import copy
import typing


class RC4:
    def __init__(self, key: bytes):
        self.s_box: list[int] = self._KSA(list(key))

    @staticmethod
    def _KSA(key: list[int]) -> list[int]:
        s_box, j = list(range(256)), 0
        for i in range(256):
            j = (j + s_box[i] + key[i % len(key)]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
        return s_box

    @staticmethod
    def _PRGA(s_box: list[int]) -> typing.Generator[int, None, None]:
        i, j = 0, 0
        s_box = copy.copy(s_box)
        while True:
            i = (i + 1) % 256
            j = (j + s_box[i]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
            yield s_box[(s_box[i] + s_box[j]) % 256]

    def encrypt(self, plaintext: bytes) -> bytes:
        return bytes(i ^ j for i, j in zip(plaintext, self._PRGA(self.s_box)))

if __name__ == "__main__":
    p = b"the brown fox jumped over the lazy dog"
    k = b"\xd3\xd3a\x15Y\x9dS\xee\xb0A<:\x81\x8e\x12\x0b"

    cipher = RC4(k)
    c = cipher.encrypt(p)
    print(f"cipher text: {c}")

    p = cipher.encrypt(c)
    print(f"plain text: {p}")

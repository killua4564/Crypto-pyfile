import abc
import struct


class Cipher(abc.ABC):
    @staticmethod
    def pad(text: bytes) -> bytes:
        padding = 16 - (len(text) % 16)
        return text + bytes([padding]) * padding

    @staticmethod
    def unpad(text: bytes) -> bytes:
        padding = text[-1]
        assert 0 < padding <= 16
        assert text.endswith(bytes([padding]) * padding)
        return text[:-padding]

    @abc.abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        raise NotImplementedError


class XTEA(Cipher):
    def __init__(self, key: int, rounds: int):
        assert len(key) == 16
        assert int(rounds) > 0

        self.key = struct.unpack("<4L", key)
        self.rounds = int(rounds)

    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = b""
        plaintext = self.pad(plaintext)
        for i in range(0, len(plaintext), 8):
            v0, v1 = struct.unpack("<2L", bytes(plaintext[i:i+8]))
            _sum, delta, mask = 0, 0x9E3779B9, 0xFFFFFFFF
            for _ in range(self.rounds):
                v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (_sum + self.key[_sum & 3]))) & mask
                _sum = (_sum + delta) & mask
                v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (_sum + self.key[_sum >> 11 & 3]))) & mask
            ciphertext += struct.pack("<2L", v0, v1)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = b""
        for i in range(0, len(ciphertext), 8):
            v0, v1 = struct.unpack("<2L", bytes(ciphertext[i:i+8]))
            _sum, delta, mask = (0x9E3779B9 * self.rounds) & 0xFFFFFFFF, 0x9E3779B9, 0xFFFFFFFF
            for _ in range(self.rounds):
                v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (_sum + self.key[_sum >> 11 & 3]))) & mask
                _sum = (_sum - delta) & mask
                v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (_sum + self.key[_sum & 3]))) & mask
            plaintext += struct.pack("<2L", v0, v1)
        return self.unpad(plaintext)


if __name__ == "__main__":
    p = b"the brown fox jumped over the lazy dog"
    k = b"\xd3\xd3a\x15Y\x9dS\xee\xb0A<:\x81\x8e\x12\x0b"

    xtea = XTEA(k, 32)
    c = xtea.encrypt(p)
    print(f"cipher text: {c}")

    p = xtea.decrypt(c)
    print(f"plain text: {p}")

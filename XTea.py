
import struct

class Cipher:

    @staticmethod
    def pad(text):
        padding = 16 - (len(text) % 16)
        return text + bytes([padding] * padding)

    @staticmethod
    def unpad(text):
        padding = text[-1]
        assert padding <= 16
        for char in text[-padding:]:
            assert char == padding
        return text[:-padding]


class XTea(Cipher):

    def __init__(self, key, rounds):
        assert len(key) == 16
        assert int(rounds) > 0

        self.key = struct.unpack('<4L', key)
        self.rounds = int(rounds)

    def encrypt(self, plaintext):
        ciphertext = b''
        plaintext = self.pad(plaintext)
        for i in range(0, len(plaintext), 8):
            pt_block = bytes(plaintext[i:i+8])
            vector0, vector1 = struct.unpack('<2L', pt_block)
            sum_delta, delta, mask = 0, 0x9E3779B9, 0xFFFFFFFF
            for _ in range(self.rounds):
                vector0 = (vector0 + (((vector1 << 4 ^ vector1 >> 5) + vector1) ^ (sum_delta + self.key[sum_delta & 3]))) & mask
                sum_delta = (sum_delta + delta) & mask
                vector1 = (vector1 + (((vector0 << 4 ^ vector0 >> 5) + vector0) ^ (sum_delta + self.key[sum_delta >> 11 & 3]))) & mask
            ciphertext += struct.pack("<2L", vector0, vector1)
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        for i in range(0, len(ciphertext), 8):
            ct_block = bytes(ciphertext[i:i+8])
            vector0, vector1 = struct.unpack('<2L', ct_block)
            sum_delta, delta, mask = (0x9E3779B9 * self.rounds) & 0xFFFFFFFF, 0x9E3779B9, 0xFFFFFFFF
            for _ in range(self.rounds):
                vector1 = (vector1 - (((vector0 << 4 ^ vector0 >> 5) + vector0) ^ (sum_delta + self.key[sum_delta >> 11 & 3]))) & mask
                sum_delta = (sum_delta - delta) & mask
                vector0 = (vector0 - (((vector1 << 4 ^ vector1 >> 5) + vector1) ^ (sum_delta + self.key[sum_delta & 3]))) & mask
            plaintext += struct.pack('<2L', vector0, vector1)
        return self.unpad(plaintext)

if __name__ == '__main__':
    p = b'the brown fox jumped over the lazy dog'
    k = b'\xd3\xd3a\x15Y\x9dS\xee\xb0A<:\x81\x8e\x12\x0b'

    xtea = XTea(k, 32)
    c = xtea.encrypt(p)
    print('cipher text:', c)

    p = xtea.decrypt(c)
    print('plain text:', p)

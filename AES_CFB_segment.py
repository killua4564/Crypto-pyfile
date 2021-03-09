
import os
from Crypto.Cipher import AES

iv = os.urandom(16)
key = os.urandom(32)

xor = lambda x, y: bytes([i ^ j for i, j in zip(x, y)])
block = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]

def CFB(segment_size, plaintext):
    assert segment_size % 8 == 0
    assert len(plaintext) % (segment_size // 8) == 0
    aes = AES.new(key, AES.MODE_CFB, iv, segment_size=segment_size)
    return aes.encrypt(plaintext)

def ECB(segment_size, plaintext):
    assert segment_size % 8 == 0
    assert len(plaintext) % (segment_size // 8) == 0
    segment_size //= 8

    segment = iv
    ciphertext = b''
    aes = AES.new(key, AES.MODE_ECB)
    for plaintext_segment in block(plaintext, segment_size):
        enc_segment = xor(aes.encrypt(segment), plaintext_segment)
        ciphertext += enc_segment
        segment = segment[segment_size:] + enc_segment
    return ciphertext

if __name__ == '__main__':
    for segment_size in range(8, 128+8, 8):
        plaintext = os.urandom(segment_size // 4)
        cfb = CFB(segment_size, plaintext)
        ecb = ECB(segment_size, plaintext)
        if cfb != ecb:
            print(f'Wrong, {segment_size}')
        print(cfb.hex())
        print(ecb.hex())

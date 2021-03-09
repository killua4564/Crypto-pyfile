
import os
from Crypto.Cipher import AES

iv = os.urandom(16)
key = os.urandom(16)
aes = AES.new(key, AES.MODE_CBC, iv)

xor = lambda x, y, z: bytes([i ^ j ^ k for i, j, k in zip(x, y, z)])
substitute = lambda x, y, n: x[:n] + y + x[n+16:]

def attack(ciphertext):
    # target: b'these are secret' change to b'hacked by killua'
    # b'these are secret' = AES(ciphertext[32:48], key) ^ ciphertext[16:32]
    # ==> b'hacked by killua' = AES(ciphertext[32:48], key) ^ ciphertext[16:32] ^ b'these are secret' ^ b'hacked by killua'
    # fixed AES(ciphertext[32:48], key)
    # change ciphertext[16:32] to ciphertext[16:32] ^ b'these are secret' ^ b'hacked by killua'
    changetext = xor(ciphertext[16:32], b'these are secret', b'hacked by killua')
    ciphertext = substitute(ciphertext, changetext, 16)
    return ciphertext

if __name__ == '__main__':
    pt = b'A' * 16 + b'B' * 16 + b'these are secret' + b'C' * 16 + b'D' * 16
    print(f'plaintext: {pt}')

    ct = aes.encrypt(pt)
    print(f'Before attack ciphertext: {ct}')

    pt = aes.decrypt(iv + ct)[16:]
    print(f'Before attack plaintext: {pt}')

    chg_ct = attack(ct)
    print(f'After attack ciphertext: {chg_ct}')

    pt = aes.decrypt(iv + chg_ct)[16:]
    print(f'After attack plaintext: {pt}')

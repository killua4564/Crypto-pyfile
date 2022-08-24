import os
from Crypto.Cipher import AES

iv: bytes = os.urandom(16)
key: bytes = os.urandom(16)
xor: callable = lambda x, y, z: bytes(i ^ j ^ k for i, j, k in zip(x, y, z))


def pad(string: bytes) -> bytes:
    k = 16 - (len(string) % 16)
    return string + bytes([k]) * k

def unpad(string: bytes) -> bytes:
    k = string[-1]
    assert k <= 16
    assert string.endswith(bytes([k]) * k)
    return string[:-k]

def leak_iv(cipher, plaintext: bytes, ciphertext: bytes) -> bytes:
    # target: leak iv
    # D(ciphertext, key) = plaintext ^ iv
    # Let block one is iv and block two is ciphertext
    # Because of CBC block mode, block two iv = block one cipher = block one iv
    # brute force iv in block one cipher byte-by-byte
    iv = b""
    for idx in range(15, -1, -1):
        for i in range(256):
            test_ciphertext = b"\x00" * idx + bytes([i]) + iv + ciphertext
            test_plaintext = cipher.decrypt(test_ciphertext)
            if test_plaintext[16+idx] == plaintext[idx]:
                iv = bytes([i]) + iv
                break
    return iv

def attack(ciphertext: bytes, iv: bytes) -> bytes:
    # target: b"test12345_guest" change to b"test12345_admin"
    # D(ciphertext, key) = b"test12345_guest" ^ iv
    # change block one to b"test12345_guest" ^ iv ^ b"test12345_admin"
    # append ciphertext to block two
    block_one = xor(pad(b"test12345_guest"), iv, pad(b"test12345_admin"))
    ciphertext = block_one + ciphertext
    return ciphertext

if __name__ == "__main__":
    pt = b"test12345_guest"
    print(f"plaintext: {pt}")

    ct = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(pt))
    print(f"Before attack ciphertext: {ct}")

    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(iv + ct)[16:]
    print(f"Before attack plaintext: {unpad(pt)}")

    iv = leak_iv(AES.new(key, AES.MODE_CBC, iv), pad(pt), ct)
    chg_ct = attack(ct, iv)
    print(f"After attack ciphertext: {chg_ct}")

    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(iv + chg_ct)[16:]
    print(f"After attack plaintext: {unpad(pt[16:])}")

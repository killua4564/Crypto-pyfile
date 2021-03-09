
class RC4:

    def __init__(self, key, plaintext):
        self.s_box = self.__ksa(list(key))
        self.key = self.__prga(self.s_box, len(plaintext))
        self.plaintext = plaintext

    @staticmethod
    def __ksa(key):
        s_box, j = list(range(256)), 0
        for i in range(256):
            j = (j + s_box[i] + key[i % len(key)]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
        return s_box

    @staticmethod
    def __prga(s_box, size):
        i, j, key = 0, 0, []
        for _ in range(size):
            i = (i + 1) % 256
            j = (j + s_box[i]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
            key.append(s_box[(s_box[i] + s_box[j]) % 256])
        return bytes(key)

    def cipher(self):
        ciphertext = []
        for i, j in zip(self.key, self.plaintext):
            ciphertext.append(i ^ j)
        return bytes(ciphertext)

if __name__ == '__main__':
    k = b'keykeykey'
    p = b'plaintext'
    print(RC4(k, p).cipher().hex())

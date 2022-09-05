class MT19937:
    MASK: int = (1 << 32) - 1

    MT: list[int]
    index: int

    def __init__(self, seed: int):
        self.MT = [0] * 624
        self.MT[0] = seed
        self.index = 0
        for idx in range(1, 624):
            self.MT[idx] = (0x6C078965 * (self.MT[idx-1] ^ self.MT[idx-1] >> 30) + idx) & self.MASK

    def generate_numbers(self):
        for idx in range(624):
            y = ((self.MT[idx] & 0x80000000) + (self.MT[(idx + 1) % 624] & 0x7FFFFFFF)) & self.MASK
            self.MT[idx] = (y >> 1) ^ self.MT[(idx + 397) % 624] ^ (0x9908B0DF * (y % 2))

    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()
        y = self.MT[self.index]
        y ^= y >> 11
        y ^= y << 7 & 0x9D2C5680
        y ^= y << 15 & 0xEFC60000
        y ^= y >> 18
        self.index = (self.index + 1) % 624
        return y & self.MASK

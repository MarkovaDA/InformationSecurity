from math import *

class RSA(object):

    # initial data
    def __init__(self, e, n, cipher_text):
        self.e = e
        self.n = n
        self.cipher_text = str(cipher_text)
        # self.generate_blocks()
        self.data = self.decipher()

    # returns array of basic multipliers
    # multipliers[0] = p, multipliers[1] = q
    def factor(self, number):
        # number = self.n
        multipliers = []
        divider = 2
        while divider * divider <= number:
            if number % divider == 0:
                multipliers.append(divider)
                number //= divider
            else:
                divider += 1
        if number > 1:
            multipliers.append(number)
        return multipliers

    # Both functions take positive integers a, b as input, and return a triple (g, x, y),
    # such that ax + by = g = gcd(a, b).
    def egcd(self, a, b):  # e, n in our task
        x, y,  u, v = 0, 1,  1, 0
        while a != 0:
            q, r = b//a, b % a
            m, n = x - u * q, y - v * q
            b, a,  x, y,  u, v = a, r,  u, v,  m, n
        gcd = b
        return gcd, x, y

    # An application of extended GCD algorithm to finding modular inverses
    def modinv(self, a, m):  # e, n in our tsk
        gcd, x, y = self.egcd(a, m)
        if gcd != 1:
            return None  # modular inverse does not exist
        else:
            return x % m

    def dectobin(self, x):
        bin = []
        while x != 0:
            bin.append(x % 2)
            x = floor(x / 2)
        return bin

    def bigmod(self, base, exponent, mod):
        a = self.dectobin(exponent)
        # b = len(a)
        btemp = 1
        f = []
        i = 0
        j = 0
        f.append((base**(2**0)) % mod)
        while i < len(a) - 1:
            f.append((f[i]**2) % mod)
            i += 1
        while j < len(a):
            if a[j] == 1.0:
                btemp = (btemp*f[j]) % mod
            j += 1

        modp = btemp % mod
        return modp

    # returns value of d
    def set_d(self):
        multipliers = self.factor(self.n)
        # print "multipliers: ", multipliers
        fi = (multipliers[0] - 1) * (multipliers[1] - 1)    # Euler's function
        d = self.modinv(self.e, fi)

        return d # self.e ** (fi_fi - 1)

    # returns numbers of chars
    def generate_blocks(self):
        # code of space = 32, of A = 65
        self.d = self.set_d()
        len_n = len(str(self.n))
        print "e = ", self.e, ", n = ", self.n, "text = ", self.cipher_text, ""
        print "d = ", self.d

        blocks = []
        i = 0
        while i < len(self.cipher_text):
            string = self.cipher_text[i:i+len_n]
            if int(string) > self.n:
                string = self.cipher_text[i:i+len_n-1]
                i += (len_n - 1)
            else:
                i += len_n
            blocks.append(int(string))

        return blocks

    # returns deciphered data
    # (block ** d) mod n
    def decipher(self):
        numbers = self.generate_blocks()
        data_numbers = []
        for block in numbers:
            data_numbers.append(self.bigmod(block, self.d, self.n))

        data = ""
        for number in data_numbers:
            data += str(number)

        result = ""
        i = 0
        while i < len(data):
            result += chr(int(data[i:i+2]))
            i += 2

        return result


#  6 variant
n = 517758144238469
e = 15931
cipher_text = 419529693641281414842251130008422950947927526

rsa_data = RSA(e, n, cipher_text)
print "Data: ", rsa_data.data


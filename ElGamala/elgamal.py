import binascii
import random
import sys


def gcd(x, y):
    if y != 0:
        return gcd(y, x % y)
    return x


def hex(message):
    return int(binascii.hexlify(str.encode(message)), 16)


def decoder(number):
    message = hex(number)
    return binascii.unhexlify(message[2:]).decode("utf-8")

def inv(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


def encode(plainText, numberOfBits):
    byteArray = bytearray(plainText, 'utf-16')
    a = []
    b = numberOfBits // 8
    c = -1 * b
    for i in range(len(byteArray)):
        if i % b == 0:
            c += b
            a.append(0)
        a[c//b] += byteArray[i]*(2**(8*(i % b)))
    return a


def encrypt(publicKP, publicKG, publicKR, numberOfBits, plainText):
    encodeText = encode(plainText, numberOfBits)
    magic = lambda encodeText: int(''.join(str(y) for y in encodeText))
    encodeTextNum = magic(encodeText)
    if encodeTextNum > publicKP:
        print("M jest większe od P")
    else:
        cipher = []
        for i in encodeText:
            x = random.randint(0, publicKP)
            y = pow(publicKG, x, publicKP)
            z = (i * pow(publicKR, x, publicKP)) % publicKP
            cipher.append([y, z])
            encryptedText = ""
            for pair in cipher:
                encryptedText += str(pair[0]) + " " + str(pair[1]) + " "
            return encryptedText


def decode(aiPlaintext, iNumBits):
    bytes_array = []
    k = iNumBits//8
    for num in aiPlaintext:
        for i in range(k):
            temp = num
            for j in range(i+1, k):
                temp = temp % (2**(8*j))
            letter = temp // (2**(8*i))
            bytes_array.append(letter)
            num = num - (letter*(2**(8*i)))
    decodedText = bytearray(b for b in bytes_array).decode("utf-8", "ignore")
    return decodedText


def decrypt(keyp, keyx, cipher):
    plaintext = []
    cipherArray = cipher.split()
    if not len(cipherArray) % 2 == 0:
        return "Zniekształcony tekst zaszyfrowany"
    for i in range(0, len(cipherArray), 2):
        c = int(cipherArray[i])
        d = int(cipherArray[i+1])
        s = pow(c, keyx, keyp)
        plain = (d*pow(s, keyp-2, keyp)) % keyp
        plaintext.append(plain)
    decryptedText = decode(plaintext, 256)
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
    return decryptedText


def siggen(p, g, x, m):
    m = hex(m)
    k = random.randint(0, p -1)
    while gcd(k, p - 1) != 1:
        k = random.randint(1, p - 1)
    r = pow(g, k, p)
    x = (m % (p - 1) - ((x * r) % (p - 1))) % (p - 1)
    x = x * inv(k, p - 1) % (p - 1)
    return r, int(x)


def sigver(p, g, pub_key, signFirst, signSecond, message):
    m = hex(message)
    r = int(signFirst)
    x = int(signSecond)
    first = pow(g, m, p)
    second = (pow(r, x, p) * pow(pub_key, r, p)) % p
    if first == second:
        return "Tak"
    else:
        return "Nie"


def main():
    if sys.argv[1] == "-k":
        idx = 0
        elgamal = open("elgamal.txt", "r")
        for line in elgamal:
            if idx == 0:
                p = int(line)
            elif idx == 1:
                g = int(line)
            idx += 1
        rnd = random.randint(0, p)
        exp = pow(g, rnd, p)
        private = open("private.txt", "w")
        private.write("%s\n%s\n%s" % (str(p), str(g), str(rnd)))
        print("Plik z kluczem prywatnym został stworzony")
        public = open("public.txt", "w")
        public.write("%s\n%s\n%s" % (str(p), str(g), str(exp)))
        print("Plik z kluczem publicznym został stworzony")

    if sys.argv[1] == "-e":
        idx = 0
        public = open("public.txt", "r")
        plain = open("plain.txt", "r")
        for line in public:
            if idx == 0: publicKP = int(line)
            if idx == 1: publicKG = int(line)
            if idx == 2: publicKR = int(line)
            idx += 1
        numberOfBits = 256
        for line in plain:
            msg = str(line)
        cipher = encrypt(publicKP, publicKG, publicKR, numberOfBits, msg)
        encryptF = open("crypto.txt", "w")
        encryptF.write("%s" % (str(cipher)))
        print("Szyfrowanie zawierszone.")
        print("Zaszyfrowane dane zostały zapisane w pliku crypto.txt")

    if sys.argv[1] == "-d":
        index = 0
        epriv = open("private.txt", "r")
        for line in epriv:
            if index == 0: privkp = int(line)
            if index == 2: privkx = int(line)
            index = index + 1
        ecrypt = open("crypto.txt", "r")
        for line in ecrypt:
            cipher = str(line)
        decrypted = ''.join((decrypt(privkp, privkx, cipher))).encode('utf-8').strip()
        edecrypt = open("decrypt.txt", "w")
        decrypted = ("%s" % decrypted)
        decrypted = decrypted.replace("'", "")
        decrypted = decrypted.replace("b", "")
        edecrypt.write(decrypted)
        print("Odszyfrowanie zawierszone")
        print("Odszyfrowane dane zostały zapisane w pliku decrypt.txt")

    if sys.argv[1] == "-s":
        index = 0
        epriv = open("private.txt", "r")
        for line in epriv:
            if index == 0: privkp = int(line)
            if index == 1: privkg = int(line)
            if index == 2: privkx = int(line)
            index = index + 1
        message = open("message.txt", "r")
        for line in message:
            content = line
        rr, ss = siggen(privkp, privkg, privkx, content)
        signature = open("signature.txt", "w")
        signature.write('%s\n%s' % (str(rr), str(ss)))
        print("Podpis został zapisany w pliku signature.txt")

    if sys.argv[1] == "-v":
        index = 0
        signature = open("signature.txt", "r")
        for line in signature:
            if index == 0: sigr = line
            if index == 1: sigs = line
            index = index + 1
        message = open("message.txt", "r")
        for line in message:
            content = line
        index = 0
        epub = open("public.txt", "r")
        for line in epub:
            if index == 0: pubkp = int(line)
            if index == 1: pubkg = int(line)
            if index == 2: pubky = int(line)
            index = index + 1
        isvalid = sigver(pubkp, pubkg, pubky, sigr, sigs, content)
        verify = open("verify.txt", "w")
        verify.write('Weryfikacja: %s' % isvalid)
        print("Weryfikacja: %s" % isvalid)

main()

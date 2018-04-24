#from BitVector import *

class RC4:

    def __init__(self, key):
        self.S = self.gen_S(key)

    def gen_S(self, key):
        s = [i for i in range(256)]
        t = []
        #k = [0] * len(key)
        #for i in range(len(key)):
        #    k[i] = int(BitVector(textstring=key[i]))
        #while (len(t) < 256):
        #    t.extend(k)
        for i in range(256):
            t.append(ord(key[i % (len(key))]))
        j = 0
        for i in range(256):
            j = (j + s[i] + t[i]) % 256
            s[i], s[j] = s[j], s[i]
        return s

    def encrypt(self, image):
        i = 0
        j = 0
        output = ""
        S = self.S
        for b in image:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = (S[i] + S[j]) % 256
            output += chr(ord(b) ^ S[k])
        return output

    def decrypt(self, image):
        return self.encrypt(image)

if __name__ == "__main__":
    rc4 = RC4("key string")
    header = []
    originalImage = []
    with open("winterTown.ppm") as input:
        for i in range(3):
            header.append(input.readline())
        originalImage = input.read()

    encryptedImage = rc4.encrypt(originalImage)
    f = open('outputImage.ppm', 'w')
    f.write(header[0] + header[1] + header[2] + encryptedImage)
    f.close()
    decryptedImage = rc4.decrypt(encryptedImage)
    if originalImage == decryptedImage:
        print('RC4 is awesome')
    else:
        print('Hmm, something seems fishy!')
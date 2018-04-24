#python2.7
#Homework Number: 05
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 2/15/2018

import io
import copy

class RC4(object):
    def __init__(self, key):
        if(len(key) != 16):
            print("key must be 16 character")
        self.key = [ord(x) for x in list(key)]
        self.S = self.gen_S(self.key)
        self.header = "P6\n1181 784\n255\n"

    def load(self, file):
        with open(file, 'rb') as f:
            #self.header = f.read(16)      # if use no header file, comments this line out
            image = f.read()

        return image

    @staticmethod
    def gen_S(key):
        S = list(range(256))
        T = [key[i % len(key)] for i in range(256)]
        # Key Scheduling
        j = 0
        for i in range(256):
            j = (j + S[i] + T[i]) % 256
            temp = S[i]
            S[i] = S[j]
            S[j] = temp
        return S

    def encrypt(self, image):
        f = io.BytesIO()
        S = copy.deepcopy(self.S)
        i = 0
        j = 0
        for c in image:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = (S[i] + S[j]) % 256
            encrypted = chr(S[k] ^ ord(c))
            f.write(encrypted)

        with open("encryptedImage.ppm", 'wb') as output:
            output.write(self.header)
            output.write(f.getvalue())
        return f


    def decrypt(self, filepointer):
        f = io.BytesIO()
        S = copy.deepcopy(self.S)
        i = 0
        j = 0
        string = filepointer.getvalue()
        for c in string:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = (S[i] + S[j]) % 256
            decrypted = chr(S[k] ^ ord(c))
            f.write(decrypted)
        with open("decryptedImage.ppm", 'wb') as output:
            output.write(self.header)
            output.write(f.getvalue())
        return f.getvalue()

if __name__ == '__main__':
    rc4Cipher = RC4('1234567890ABCDEF')
    originalImage = rc4Cipher.load("winterTownNoHeader.ppm")
    encryptedImage = rc4Cipher.encrypt(originalImage)
    decryptedImage = rc4Cipher.decrypt(encryptedImage)

    if  decryptedImage == originalImage:
        print('RC4 is awesome')
    else:
        print('Hmm, something seems fishy!')
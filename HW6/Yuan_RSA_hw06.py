#Homework Number: 6
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 2/27/2017

#my read_bits_from_file(256) function couldn't work correctly, it gets different bit with my input file

from PrimeGenerator import *
from BitVector import *
import os

def gcd(a,b):
    while b:
        a, b = b, a%b
    return a

def gen_key(e):
    while(True):
        prime = PrimeGenerator(bits = 128)
        p = prime.findPrime()
        q = prime.findPrime()
        if p != q:
            if (bin(p)[2] and bin(p)[3] and bin(q)[2] and bin(q)[3]):
                #print(bin(p),bin(q))
                if gcd((p-1),e) == 1 and gcd((q-1),e) == 1:
                    break
    n = p * q
    tn = (p - 1) * (q - 1)
    e_bv = BitVector(intVal=e)
    tn_bv = BitVector(intVal=tn)
    d_bv = e_bv.multiplicative_inverse(tn_bv)
    d = int(d_bv)
    pub = [e,n]
    prv = [d,n]
    return (prv,pub,p,q)

def crt(block, d, n, p, q):
    #print("b")
    V_p = pow(block, d, p)
    V_q = pow(block, d, q)
    p_bv = BitVector(intVal=p)
    q_bv = BitVector(intVal=q)
    X_p = q * int(q_bv.multiplicative_inverse(p_bv))
    X_q = p * int(p_bv.multiplicative_inverse(q_bv))
    output = ((V_p * X_p) + (V_q * X_q)) % n
    #print(len(str(output)))
    return output

def readFile(f, ed):
    data = []
    #my_f = open(f,'r').read()
    #print(''.join(format(ord(x), 'b') for x in my_f))
    bv = BitVector(filename=f)
    if (ed == 'e'):
        while bv.more_to_read:
            data.append(bv.read_bits_from_file(128))
        n = BitVector(textstring='\n')
        while(len(data[-1]) < 128):
            data[-1] += n
        for i in data:
            i.pad_from_left(128)
            print("message3",pow(int(i),3))
        return data
    else:
        #need original output
        if os.path.isfile("real_output.txt"):
            print("with real output")
            test = open("real_output.txt",'r').read().split()
            for i in test:
                data.append(BitVector(intVal=int(i),size=256))
        else:
            #this won't work since it gets different bits with my encrypted output
            while bv.more_to_read:
                data.append(bv.read_bits_from_file(256))
    return data

def encrypt(data,key):
    output = []
    for i in data:
        output.append(pow(int(i),key[0],key[1]))
    return output

def decrypt(data,key,p,q):
    output = []
    for i in data:
        #print(int(i))
        #print("len",len(i))
        output.append(crt(int(i),key[0],key[1],p,q))
    return output

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print("usage: Yuan_RSA_hw06.py -e | -p input.txt output.txt")
    e = 65537 #replace this number 65537 with 3 for breakRSA
    private_key = [0,0]
    f = open(sys.argv[3], 'w')
    if (sys.argv[1] == '-e'):
        private_key, public_key, p, q = gen_key(e)
        if os.path.isfile("key.txt"):
            os.remove("key.txt")
        k = open("key.txt", 'w')
        k.write(str(p)+" ")
        k.write(str(q)+" ")
        k.write(str(private_key[0])+" ")
        k.write(str(private_key[1])+" ")
        k.write(str(public_key[0]))
        data = readFile(sys.argv[2],'e')
        output = encrypt(data,public_key)
        fhex = open("encrypt_hex.txt", 'w')
        temp = open("real_output.txt",'w')
        #print("output",len(output))
        for i in output:
            bv = BitVector(intVal=i, size = 256)
            f.write(bv.get_bitvector_in_ascii())
        for i in output:
            #print(i)
            #print(len(str(i)))
            bv = BitVector(intVal=i, size = 256)
            #print(len(bv))
            temp.write(str(int(bv))+" ")
            #f.write(bv.get_bitvector_in_ascii())
        for i in output:
            bv = BitVector(intVal=i, size = 256)
            fhex.write(bv.get_bitvector_in_hex())
        #need original output
        #test = open("output.txt",'r').read().split()
        #print("test",test)
        #sb = []
        #for i in test:
        #    sb.append(BitVector(intVal=int(i),size=256))
        #for n in sb:
        #    print(int(n)
        temp.close()
    elif (sys.argv[1] == '-d'):
        data = readFile(sys.argv[2],'d')
        k = open("key.txt", 'r')
        key = k.readlines()[0].split()
        p = long(key[0])
        q = long(key[1])
        private_key[0] = long(key[2])
        private_key[1] = long(key[3])
        output = decrypt(data,private_key,p,q)
        fhex = open("decrypt_hex.txt", 'w')
        for i in output:
            bv = BitVector(intVal=i, size=256)
            print(bv)
            bv = bv[128:]
            f.write(bv.get_bitvector_in_ascii())
        for i in output:
            bv = BitVector(intVal=i, size=256)
            bv = bv[128:]
            fhex.write(bv.get_bitvector_in_hex())
        if(os.path.isfile("real_output.txt")):
            os.remove("real_output.txt")
    fhex.close()
    f.close()

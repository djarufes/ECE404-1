#Homework Number: 6
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 2/27/2017

from Yuan_RSA_hw06 import *
from BitVector import *
from solve_pRoot import *
from copyfile import *

def save_key(private_key, public_key, p, q, num):
    file = open("key"+num+".txt",'w')
    file.write("private key " + str(private_key[0])+" "+str(private_key[1]) + "\n")
    file.write("public key " + str(public_key[0])+" "+str(public_key[1]) + "\n")
    file.write("p " + str(p) + "\n")
    file.write("q " + str(q) + "\n")
    return

if __name__ == "__main__":
    e=3
    private_key1, public_key1, p1, q1 = gen_key(e)
    save_key(private_key1,public_key1,p1,q1,'1')
    n1 = public_key1[1]
    data1 = readFile(sys.argv[1], 'e')
    en1 = encrypt(data1, public_key1)
    f = open("encrypt1.txt",'w')
    fhex = open("encrypt_hex1.txt",'w')
    for i in en1:
        bv = BitVector(intVal=i, size=256)
        f.write(bv.get_bitvector_in_ascii())
    for i in en1:
        bv = BitVector(intVal=i, size=256)
        fhex.write(bv.get_bitvector_in_hex())


    private_key2, public_key2, p2, q2 = gen_key(e)
    save_key(private_key2, public_key2, p2, q2, '2')
    n2 = public_key2[1]
    data2 = readFile(sys.argv[1], 'e')
    en2 = encrypt(data2, public_key2)
    f = open("encrypt2.txt",'w')
    fhex = open("encrypt_hex2.txt",'w')
    for i in en2:
        bv = BitVector(intVal=i, size=256)
        f.write(bv.get_bitvector_in_ascii())
    for i in en2:
        bv = BitVector(intVal=i, size=256)
        fhex.write(bv.get_bitvector_in_hex())


    private_key3, public_key3, p3, q3 = gen_key(e)
    save_key(private_key3, public_key3, p3, q3, '3')
    n3 = public_key3[1]
    data3 = readFile(sys.argv[1], 'e')
    en3 = encrypt(data3, public_key3)
    f = open("encrypt3.txt",'w')
    fhex = open("encrypt_hex3.txt",'w')
    for i in en3:
        bv = BitVector(intVal=i, size=256)
        f.write(bv.get_bitvector_in_ascii())
    for i in en3:
        bv = BitVector(intVal=i, size=256)
        fhex.write(bv.get_bitvector_in_hex())



    print "p",p1,"q",q1,"e",public_key1,"n",n1,"d",private_key1
    print p2,q2,public_key2,n2,private_key2
    print p3,q3,public_key3,n3,private_key3


    N = n1*n2*n3
    print("n",N)

    N1 = N/n1
    bv1 = BitVector(intVal= n1)
    bvN1 = BitVector(intVal= N1)
    d1 = int(bvN1.multiplicative_inverse(bv1))

    N2 = N/n2
    bv2 = BitVector(intVal= n2)
    bvN2 = BitVector(intVal= N2)
    d2 = int(bvN2.multiplicative_inverse(bv2))

    N3 = N/n3
    bv3 = BitVector(intVal= n3)
    bvN3 = BitVector(intVal= N3)
    d3 = int(bvN3.multiplicative_inverse(bv3))

    #en1 = BitVector(filename="encrypt1.txt")
    #print(en1.read_bits_from_file(256))
    #en2 = BitVector(filename="encrypt2.txt")
    #en3 = BitVector(filename="encrypt3.txt")

    M = []
    print(solve_pRoot(3,64))
    for i in range(len(en1)):
        #bven1 = int(en1.read_bits_from_file(256))
        #bven2 = int(en2.read_bits_from_file(256))
        #bven3 = int(en3.read_bits_from_file(256))
        temp = ((en1[i] * N1 * d1) + (en2[i] * N2 * d2) + (en3[i] * N3 * d3)) % N
        print('running',temp)
        M.append(solve_pRoot(3,temp))
        print('sb')

    print(M)
    fout = open(sys.argv[2], 'w')
    for i in M:
        bv = BitVector(intVal=i, size = 128)
        fout.write(bv.get_bitvector_in_ascii())
    fout = open("cracked_hex.txt",'w')
    for i in M:
        bv = BitVector(intVal=i, size = 128)
        fout.write(bv.get_bitvector_in_hex())
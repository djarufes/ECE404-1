#python2.7
#Homework Number: 02
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 1/24/2018

import random
import os
import copy
from DES_yuan import *


def file_as_bits(inputfile):
    read_bits = os.path.getsize(inputfile) * 8
    bv = BitVector(filename=inputfile)
    bitvec = bv.read_bits_from_file(read_bits)
    return bitvec


def bit_changes(f1, f2):
    b1 = file_as_bits(f1)
    b2 = file_as_bits(f2)
    changes = b1 ^ b2
    return changes.count_bits(), b1.length()/64


def gen_sboxes():
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    s_boxes = {i: None for i in range(8)}

    for i in range(8):
        random.shuffle(x)
        r1 = copy.deepcopy(x)
        random.shuffle(x)
        r2 = copy.deepcopy(x)
        random.shuffle(x)
        r3 = copy.deepcopy(x)
        random.shuffle(x)
        r4 = copy.deepcopy(x)
        s_boxes[i] = [r1, r2, r3, r4]
    return s_boxes



def substitute( expanded_half_block ,sb):
    output = BitVector (size = 32)
    s_boxes = sb
    segments = [expanded_half_block[x*6:x*6+6] for x in range(8)]
    for sindex in range(len(segments)):
        row = 2*segments[sindex][0] + segments[sindex][-1]
        column = int(segments[sindex][1:-1])
        output[sindex*4:sindex*4+4] = BitVector(intVal = s_boxes[sindex][row][column], size = 4)
    return output


def encrypt_with_sb(input, output, sb, decrypt = False):
    key = get_encryption_key()
    round_key = generate_round_keys( key )
    if decrypt:
        round_key.reverse()
    bv = BitVector( filename=input )
    output_file = open(output,'ab')
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )
        if bitvec.length() > 0:
            if len(bitvec) != 64:
                bitvec.pad_from_right(64 - len(bitvec))
            [LE, RE] = bitvec.divide_into_two()
            for rkey in round_key:
                newRE = RE.permute( expansion_permutation )
                out_xor = newRE ^ rkey
                out_sub = substitute(out_xor, sb)
                p_out = out_sub.permute(p_box_permutation)
                temp = RE
                RE = p_out ^ LE
                LE = temp
            output = RE + LE
            output.write_to_file(output_file)
    output_file.close()
    return

def diffusion(inputfile, sbox=None):
    plaintext_bits = file_as_bits(inputfile)
    bit_to_change = random.randrange(plaintext_bits.length())
    plaintext_bits[bit_to_change] ^= 1

    FILEOUT = open("new_plaintext.txt", 'wb')
    plaintext_bits.write_to_file(FILEOUT)
    FILEOUT.close()
    if sbox:
        encrypt_with_sb(inputfile, "ciphertext.txt", sbox)
        encrypt_with_sb("new_plaintext.txt", "ciphertext_new.txt", sbox)
    else:
        encrypt(inputfile, "ciphertext.txt")
        encrypt("new_plaintext.txt", "ciphertext_new.txt")

    changed_bits, _ = bit_changes("ciphertext.txt", "ciphertext_new.txt")

    os.remove("ciphertext.txt")
    os.remove("new_plaintext.txt")
    os.remove("ciphertext_new.txt")

    return changed_bits


def confusion(inputfile):
    encrypt(inputfile, "ciphertext.txt")
    key_bits = file_as_bits("key.txt")
    bit_to_change = random.randrange(key_bits.length())
    key_bits[bit_to_change] ^= 1
    os.remove("key.txt")

    FILEOUT = open("key.txt", 'wb')
    key_bits.write_to_file(FILEOUT)
    FILEOUT.close()

    encrypt(inputfile, "ciphertext_new.txt")

    changed_bits, blocks = bit_changes("ciphertext.txt", "ciphertext_new.txt")

    os.remove("ciphertext.txt")
    os.remove("ciphertext_new.txt")

    return changed_bits / blocks


if __name__ == '__main__':

    #1
    avg_bits_changed = []
    for _ in range(20):
        bits_changed = diffusion("message.txt")
        avg_bits_changed.append(bits_changed)
    print(sum(avg_bits_changed) / len(avg_bits_changed))

    #2
    sbox1 = gen_sboxes()
    sbox2 = gen_sboxes()
    avg_bits_changed = []
    results = []
    for sbox in [sbox1, sbox2]:
        for _ in range(20):
            bits_changed = diffusion("message.txt", sbox)
            avg_bits_changed.append(bits_changed)
        avg = sum(avg_bits_changed) / len(avg_bits_changed)
        results.append(avg)
    print(results[0], results[1])

    #3
    total = 0
    for key in ["eepurdue", "iamjacky", 'whatssup', 'iplaylol']:
        os.remove("key.txt")
        with open("key.txt", 'w') as f:
            f.write(key)

        bits_changed = confusion("message.txt")
        total += bits_changed
    print (total / 4)

    '''
        Problem 1:
            Average bits changed: 32
        Problem 2:
            For Random Sbox 1:
                Average bits changed: 31
            For Random Sbox 2:
                Average bits changed: 31
        Problem 3:
        	Average bits changed: 31
    '''
#Homework Number: 1
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 1/19/2017

input_file = open('input.txt', 'r')
output_file = open('output.txt', 'w')
key_file = open('key.txt', 'r')

f = input_file.read()
key = key_file.read()


output_txt = ""
i = 0
for c in f:
    if c.isupper():
        if (key[i].isupper()):
            output_txt += chr((ord(c) - 65 + ord(key[i]) - 65) % 26 + 65)
        else :
            output_txt += chr((ord(c) - 65 + ord(key[i]) - 97) % 26 + 65)
    else:
        if (key[i].isupper()):
            output_txt += chr((ord(c) - 97 + ord(key[i]) - 65) % 26 + 97)
        else:
            output_txt += chr((ord(c) - 97 + ord(key[i]) - 97) % 26 + 97)
    i += 1
    if i == len(key):
        i = 0
output_file.write(output_txt)
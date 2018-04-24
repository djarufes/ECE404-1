#python2.7
#Homework Number: 03
#Name: Jiacheng Yuan
#ECN Login: yuan105
#Due Date: 1/31/2018


def isPrime(num):
    if num == 1:
        return False
    for n in range(2, num):
        if num % n == 0 and n!= num:
            return False
    return True

if __name__ == "__main__":
    num = 0
    while (1 > num or num >= 50):
        num = input("Please input a small integer (1<n<50): ")
    if isPrime(num):
        print("field")
    else:
        print("ring")
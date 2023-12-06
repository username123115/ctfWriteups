import random

key1 = random.choices(range(256), k=20)
key2 = list(range(256))
random.shuffle(key2)
flag = open('flag.txt', 'rb').read()    

def enc(n):
    q = key2[n]
    w = key1[q % 20]
    n ^= q
    return n, w

x = 0
l = len(flag) * 2 * 8
def display(n, op = 0):
    bytesDisplayed = l // 8
    opBytes = (op * 2 + 1)
    for i in range(bytesDisplayed):
        if (bytesDisplayed - i - 1) == opBytes:
            msg = "V" * 8
        else:
            msg = str(bytesDisplayed - i - 1) * 8
        print(msg, end=' ')
    print('')
    s = bin(n)
    n = (s[2:])
    nl = l - len(n)
    zeros = '0' * nl
    msg = (zeros + n)
    for i in range(bytesDisplayed):
        print(msg[8 * i: 8 * (i + 1)], end=' ')

    print('')
    print('')

display(x)
print("start")
for i, c in enumerate(flag):
    x <<= 8
    display(x, i)
    n, w = enc(c)
    if i % 2:
        n, w = w, n
    
    #n placed at beginning (normal order)
    x |= n
    display(x, i)
    #w placed at end (normal order)
    x |= w << ((2 * i + 1) * 8)
    display(x, i)
    print("new")
display(x)


#! /bin/python
with open('output.txt') as f:
    output = [int(x) for x in f.readlines()]

blockCounts = 264
seeds = []
randoms = []
original = []
scrambled = []

for i in range(blockCounts):
    j = i + 1
    seeds.append((j * 127) % 500)

for i in range(blockCounts):
    j = i + 1
    y = (((j * 327) % 681) + 344) % 313
    randoms.append(y)

r = 0
for i in range(blockCounts):
    if (i != 0):
        r = output[i - 1]
    original.append((output[i] ^ randoms[i]) ^ r)


#This took an ungodly amount of time (mostly due to not reading code correctly)
######################### Test
out = []
r = 0
for i in range(blockCounts):
    fun = original[i]
    r = (fun ^ r) ^ randoms[i]
    out.append(r)

print(out == output)
#########################

# confirm all are same length (also fit scramble output due to only having groups of "11"'s and "00"'s
binStrings = []
for x in original:
    y = bin(x)
    binStrings.append(y)
    print(y)

length = len(bin(original[0])) - 2
print(length)
rawLength = length // 2

#length = 60
#=>raw string will be 30 chars => 30 / 6 = 5 groups/block => 5 lines

def unScramble(binString, seed):
    order = ["x" for i in range(rawLength)]

    for i in range(rawLength):
        #print(order)
        y = (i * seed) % rawLength
        while order[y] != "x":
            y = (y + 1) % rawLength
        order[y] = i

    scrambled = []
    #get rid of the "0b"
    binString = binString[2:]
    for i in range(rawLength):
        c = binString[i * 2:i*2+2]
        if c == "00":
            scrambled.append('0')
        elif c == "11":
            scrambled.append('1')
        else:
            print(f"Invalid string: {c}")

    result = ["_" for i in range(rawLength)]
    for index, charOrder in enumerate(order):
        #indexth element of scrambled was originally charOrderth
        result[charOrder] = scrambled[index]
    blocks = []
    for block in range(rawLength // 6):
        b = result[6 * block: 6 * block + 6]
        b = "".join(b)
        blocks.append(b)

    return blocks

print(unScramble(binStrings[0], seeds[0]))
final = ["" for i in range(5)]
for i in range(blockCounts):
    good = unScramble(binStrings[i], seeds[i])
    for j in range(len(good)):
        if len(good[j]) != 6:
            print("bad")
        final[j] += good[j] + " "

"""
for s in final:
    print(s)
"""
print(len(final[0]))




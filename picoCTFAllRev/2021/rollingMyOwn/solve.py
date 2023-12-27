#! /bin/python
import hashlib
import string
from tqdm import tqdm

"""
  for (i = 0; i < 4; i = i + 1) {
    for (j = 0; j < 4; j = j + 1) {
      local_d8[j * 4 + i] = hashed[offsets[j] + j * 0x10 + i];
    }
  }
"""
offsets = [8, 2, 7, 1]
codeIndexes = [0] * 16
for i in range(4):
    for j in range(4):
        codeIndexes[j * 4 + i] = offsets[j] + j * 0x10 + i


salts = ["GpLaMjEW", "pVOjnnmk", "RGiledp6", "Mvcezxls"]
key = "D1v1~~~~~~~~~~~~"
desirables = [0x4889fe48, 0xbff126dc, 0xb3070000, 0x00ffd6]
lb = 8
ub = 11

"""
We need
mov rsi, rdi
mov rdi, 0x7b3dc26f1
call rsi

=====

48 89 fe
48 bf f1 26 dc b3 07 00 00 00
ff d6 ??

48 89 fe 48
bf f1 26 dc
b3 07 00 00
00 ff d6 ??
"""

def determineElegibility(key, offset):
    global salts, desirables, offsets
    toHash = (key + salts[offset]).encode()
    #print(toHash)
    #print(len(toHash))
    result = hashlib.md5(toHash)
    hashed = result.digest()
    #print(hashed)
    length = 4
    if offset == 3:
        length = 3
    run = hashed[offsets[offset]: offsets[offset] + length]
    #print(run)
    #print(int.from_bytes(run) == desirables[offset])
    return int.from_bytes(run) == desirables[offset]



print(codeIndexes)
print(len(key))

flagChars = string.printable
charLen = len(flagChars)

# we already know what the offset for 1 is from the hint ("D1v1")
for i in range(1, 4):
    print(i)
    for j in tqdm(range(charLen ** 4)):
        candidate = ""
        temp = j
        for k in range(4):
            a = temp % charLen
            temp -= a
            temp = temp // charLen
            candidate += flagChars[a]
        candidate = candidate[::-1]
        if determineElegibility(candidate, i):
            print(candidate)
            break

# this finds the key as D1v1d3AndC0nqu3r

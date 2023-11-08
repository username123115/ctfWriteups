#! /bin/python
from binary import *

def scramble(inp, offset):
    substitutionTable = substitutions[offset]
    swapTable = swaps[offset]
    transformed = []
    modified = [0] * 32

    for value in inp:
        transformed.append(substitutionTable[value])
    for i in range(32):
        modified[i] = transformed[swapTable[i]]
    return modified

def unScramble(inp, offset):
    substitutionTable = substitutions[offset]
    swapTable = swaps[offset]

    unSub = [0] * 256
    unSwap = [0] * 32

    for i in range(256):
        unSub[substitutionTable[i]] = i
    for i in range(32):
        #the ith element is in swapTable[i]
        #so the swapTable[i]th element should go to i
        unSwap[swapTable[i]] = i

    unSwapped = [0] * 32
    for i in range(32):
        unSwapped[i] = inp[unSwap[i]]

    unScrambled = []
    for value in unSwapped:
        unScrambled.append(unSub[value])
    return unScrambled
    

l = [x for x in range(32)]

good = (unScramble(unScramble(unScramble(unScramble(final, 3), 2), 1), 0))
solution = ""
for x in good:
    solution += (chr(x))

print(solution)



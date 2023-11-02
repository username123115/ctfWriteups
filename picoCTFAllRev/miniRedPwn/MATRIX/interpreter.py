#! /bin/python

PROGRAM="./prog"
with open(PROGRAM, "r") as f:
    lines = f.readlines()

prog = []

counter = 0
a = []
b = []

resWin = 0
resCount = 0

for l in lines:
    l = l.replace("\n", "")
    for n in l.split(" "):
        h = int(n, 16)
        prog.append(h)

def interpret():
    global prog, counter, a, b, resWin, resCount
    eip = int(counter)
    ins = prog[eip]
    counter += 1
    #NOP
    if (ins == 0x00):
        return 1
    #Set win, pop from `a` into counter, end
    elif (ins == 0x01):
        resWin = 0
        resCounter = a[-1]
        return 0
    # Take value at top of `a` and push onto `a`
    elif (ins == 0x10):
        a.append(a[-1])
        return 1
    # Decrement a
    elif (ins == 0x11):
        a = a[:-1]
        return 1
    # Sum first with second highest element of `a` into second highest and pop from `a`
    elif (ins == 0x12):
        a[-2] = a[-2] + a[-1]
        a = a[:-1]
        return 1
    # Subtract first from second element of `a` into second and pop from `a`
    elif (ins == 0x13):
        a[-2] = a[-2] - a[-1]
        a = a[:-1]
        return 1
    # Swap second and first elements of `a`
    elif (ins == 0x14):
        t = a[-2]
        a[-2] = a[-1]
        a[-1] = t
        return 1
    # Pop from `a`, push to `b`
    elif (ins == 0x20):
        t = a[-1]
        a = a[:-1]
        b.append(t)
        return 1
    # Pop from `b`, push to `a`
    elif (ins == 0x21):
        t = b[-1]
        b = b[:-1]
        a.append(t)
        return 1
    # Pop from `a` into counter
    elif (ins == 0x30):
        t = a[-1]
        a = a[:-1]
        counter = t
        return 1
    # Pop second and first elements from `a`, if second element is zero, jump to first element
    elif (ins == 0x31):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        if (s == 0):
            counter = f
        return 1
    # Pop second and first elements from `a`, if second element is NOT zero, jump to first element
    elif (ins == 0x32):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        if (s != 0):
            counter = f
        return 1
    # Pop second and first elements from `a`, if second element is LESS than zero, jump to first element
    elif (ins == 0x33):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        if (s < 0):
            counter = f
        return 1
    # Pop second and first elements from `a`, if second element is LESS than ONE, jump to first element
    elif (ins == 0x34):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        if (s < 1):
            counter = f
        return 1
    else:
        if (ins == 0xc0):
            a.append(ord(input()[0]))
            return 1

        if (ins < 0xc1):
            if (ins == 0x80):
                a.append(prog[eip + 1])
                counter = eip + 2
            # Push next word into `a`, jump over word
            elif (ins == 0x81):
                p1 = prog[eip + 2]
                p2 = prog[eip + 1]
                v = 256 * p1 + p2
                # Account for sign of V
                v - ((v >> 15) * (1 << 15))
                a.append(256 * p1 + p2)
                counter = eip + 3
            #Invalid instruction, lets fail!
            else:
                resWin = 1
                print(f"Invalid instruction {hex(ins)}")
                print(ins)
                return 0
            return 1
        if (ins == 0xc1):
            t = a[-1]
            a = a[:-1]
            print(chr(t), end="")
            return 1
        # just in case?
        return 1

cont = 1
while (cont != 0):
    cont = interpret()

#! /bin/python
import sys


PROGRAM="./prog"
HELP = """
    Debugging program instructions:
    d: Dissasemble until next branch
    b: Set breakpoint
    c: Continue until end/breakpoint
    pa:Print contents of stack a
    pb:Print contents of stack b
    t: Toggle print mode
    q: Exit program
    s: Step one instruction (Inputting nothing and pressing enter works too)
    h: Print this help message
    """

STOP = 0x0
STEPS = 1
HIT = False

PRINT = True

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

def moveInstruction():
    global prog, counter, a, b, resWin, resCount, HIT, STOP, STEPS
    eip = int(counter)
    ins = prog[eip]
    counter += 1
    return eip, ins

def debug():
    global prog, counter, a, b, resWin, resCount, HIT, STOP, STEPS, PRINT
    eip, ins = moveInstruction()

    if (not HIT) and (eip == STOP):
        print("*", end="")
        HIT = True
    if HIT:
        STEPS -= 1
    while (STEPS == 0):
        HIT = False
        command = input("> ").lower()
        #Step through commands is default
        if (command == "d"):
            saveState = (int(counter), list(a), list(b), int(resWin), int(resCount), int(eip), int(ins))
            savePrint = bool(PRINT)
            PRINT = True
            #Disassemble
            while (not (0x30 <= ins <= 0x34)):
                interpret(eip, ins)
                eip, ins = moveInstruction()
            print("hit branch")
            interpret(eip, ins)
            counter, a, b, resWin, resCount, eip, ins = saveState
            PRINT = savePrint

        if (command == "b"):
            addr = int(input("Enter address, 0 to set HIT: "), 16)
            STOP = addr
            if (addr <= 0):
                HIT = True
            steps = int(input("Enter instructions to go forward: "))
            STEPS = steps
        if (command == "c"):
            STEPS = 1
        if (command == "pa"):
            print(a)
        if (command == "pb"):
            print(b)
        if (command == "t"):
            PRINT = not PRINT
        if (command == "q"):
            exit()
        if (command == "s" or command == ""):
            HIT = True
            STEPS += 1
        if (command == "h" or command == "help"):
            print(HELP)
    return interpret(eip, ins)

def interpret(eip, ins):
    global counter, a, b, resWin, resCount
    if PRINT:
        print(f"{hex(eip)}: {hex(ins)} ", end = "")
    message = ""
    ret = 1
    #NOP
    if (ins == 0x00):
        message = ("NOP")
        ret = 1
    #Set win, pop from `a` into counter, end
    elif (ins == 0x01):
        message = ("WIN A")
        resWin = 0
        resCounter = a[-1]
        ret = 0
    # Take value at top of `a` and push onto `a`
    elif (ins == 0x10):
        message = (f"pushAA {hex(a[-1])}")
        a.append(a[-1])
        ret = 1
    # Decrement a
    elif (ins == 0x11):
        message = (f"A-- {hex(a[-1])} -> {hex(a[-2])}")
        a = a[:-1]
        ret = 1
    # Sum first with second highest element of `a` into second highest and pop from `a`
    elif (ins == 0x12):
        message = (f"ASUM {hex(a[-2])} + {hex(a[-1])}")
        a[-2] = a[-2] + a[-1]
        a = a[:-1]
        ret = 1
    # Subtract first from second element of `a` into second and pop from `a`
    elif (ins == 0x13):
        message = (f"ADIF {hex(a[-2])} - {hex(a[-1])} -> {hex(a[-2] - a[-1])}")
        a[-2] = a[-2] - a[-1]
        a = a[:-1]
        ret = 1
    # Swap second and first elements of `a`
    elif (ins == 0x14):
        message = (f"ASWAP {hex(a[-2])} <-> {hex(a[-1])}")
        t = a[-2]
        a[-2] = a[-1]
        a[-1] = t
        ret = 1
    # Pop from `a`, push to `b`
    elif (ins == 0x20):
        message = (f"APUSHB {hex(a[-1])}")
        t = a[-1]
        a = a[:-1]
        b.append(t)
        ret = 1
    # Pop from `b`, push to `a`
    elif (ins == 0x21):
        message = (f"BPUSHA {hex(b[-1])}")
        t = b[-1]
        b = b[:-1]
        a.append(t)
        ret = 1
    # Pop from `a` into counter
    elif (ins == 0x30):
        message = (f"JUMPA {hex(a[-1])}")
        t = a[-1]
        a = a[:-1]
        counter = t
        ret = 1
    # Pop second and first elements from `a`, if second element is zero, jump to first element
    elif (ins == 0x31):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        message = (f"JMP {hex(f)} IF {hex(s)} == 0")
        if (s == 0):
            counter = f
        ret = 1
    # Pop second and first elements from `a`, if second element is NOT zero, jump to first element
    elif (ins == 0x32):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        message = (f"JMP {hex(f)} IF {hex(s)} != 0")
        if (s != 0):
            counter = f
        ret = 1
    # Pop second and first elements from `a`, if second element is LESS than zero, jump to first element
    elif (ins == 0x33):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        message = (f"JMP {hex(f)} IF {hex(s)} < 0")
        if (s < 0):
            counter = f
        ret = 1
    # Pop second and first elements from `a`, if second element is LESS than ONE, jump to first element
    elif (ins == 0x34):
        s = a[-2]
        f = a[-1]
        a = a[:-2]
        message = (f"JMP {hex(f)} IF {hex(s)} < 1")
        if (s < 1):
            counter = f
        ret = 1
    else:
        if (ins == 0xc0):
            message = None
            if PRINT:
                print("GETC")
            a.append(ord(input()[0]))
            ret = 1

        if (ins < 0xc1):
            if (ins == 0x80):
                v = prog[eip + 1]
                message = (f"STOREB {hex(v)} ({chr(v)})")
                a.append(v)
                counter = eip + 2
            # Push next word into `a`, jump over word
            elif (ins == 0x81):
                p1 = prog[eip + 2]
                p2 = prog[eip + 1]
                v = 256 * p1 + p2
                # Account for sign of V
                v - ((v >> 15) * (1 << 15))
                message = (f"STOREW {hex(v)}")
                a.append(v)
                counter = eip + 3
            #Invalid instruction, lets fail!
            elif (ins != 0xc0):
                resWin = 1
                message = (f"Invalid instruction {hex(ins)}")
                print(message)
                return 0
            ret = 1
        if (ins == 0xc1):
            t = a[-1]
            a = a[:-1]
            message = (f"PUTC {hex(t)} ({chr(t)})")
            print(chr(t), end="")
            ret = 1
        # just in case?
        ret = 1
    if PRINT and message:
        print(message)
    return ret
print(HELP)
cont = 1
while (cont != 0):
    cont = debug()

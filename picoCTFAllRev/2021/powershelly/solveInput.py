#! /bin/python
lines = []
with open("./input.txt") as f:
    for l in f.readlines():
        if '\n' in l:
            l = l[:-1]
        lines.append(l.split(" "))
ones = ['110011', '100011', '110011', '110011', '100001']

result = []
for i in range(len(lines)):
    b = ""
    for c in lines[i]:
        if c == ones[i]:
            b += "1"
        else:
            b += "0"
    result.append(b)

strings = []
for b in result:
    s = ""
    for i in range(len(b) // 8):
        c = b[8 * i: 8 * i + 8]
        c = int(c, 2)
        s += chr(c)
    strings.append(s)

print(strings)
print(strings[0])


alpha = [x for x in 'zvtwrca57n49u2by1jdqo6g0ksxfi8pelmh3']
print(alpha)
enc = [902,764,141,454,207,51,532,1013,496,181,562,342]
req = 'isaac newton'
name = []

def itemOf(letter):
    if letter not in alpha:
        return 0
    else:
        return alpha.index(letter) + 1

for i in range(len(req)):
    letter = req[i]
    name.append(itemOf(letter))

ans = "aaaabbbbcccc"
inp = [itemOf(x) for x in ans]

print(name)
i = 1
while i <= 12:
    j = ((i * i + name[i - 1]) % len(name)) + 1
    #print(j)
    known = name[i-1] * name[j-1]
    #print(known)
    print((i-1, j-1))
    print(enc[i-1] - known)
    print("====")
    tmp = inp[i - 1] * inp[j - 1] + known
    i += 1


#0  1  2  3  4  5  6  7  8  9  10 11
#17 14 33 32 3  3  36 5  28 17 11 12

solution = [17, 14, 33, 32, 3, 3, 36, 5, 28, 17, 11, 12]
flag = ""
for c in solution:
    flag += alpha[c-1]
print(flag)

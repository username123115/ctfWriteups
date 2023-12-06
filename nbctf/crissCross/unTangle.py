other = 3449711664888782790334923396354433085218951813669043815144799745483347584183883892868078716490762334737115401929391994359609927294549975954045314661787321463018287415952
l = 35 * 2 * 8

b = bin(other)[2:]
length = len(b)
results = []
for i in range(length // 8):
    results.append(b[8 * i: 8 * (i + 1)])

n = []
w = []

#start from end, the end is known to be the value of w after encoding the last byte of the flag
for i in range(35):
    corrEnd = (69 - i)
    #n, w
    if (i % 2):
        n.append(results[i])
        w.append(results[corrEnd])
    else:
        w.append(results[i])
        n.append(results[corrEnd])
    #w, n

data = []

for i in range(35):
    point = (int(n[i], 2), int(w[i], 2))
    data.append(point)

#reverse to get original orderings
data = data[::-1]
print(data)


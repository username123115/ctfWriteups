#! /bin/python

MAZE = "./maze"
with open(MAZE, "r") as f:
    lines = f.readlines()

maze = []
data = []
bad = 0x81fb0030
normal = 0x30000000
x1 = 0x81740530
x2 = 0x817f0530
x3 = 0x81850530

"""
bad = [0x81, 0xfb, 0x0, 0x30]
normal = [0x30, 0x0, 0x0, 0x0]
x1 = [0x81, 0x74, 0x5, 0x30]
x2 = [0x81, 0x7f, 0x5, 0x30]
x3 = [0x81, 0x85, 0x5, 0x30] #only seen once?
"""

mappings = {bad : "#",
            normal: " ",
            x1: "-",
            x2: "+",
            x3: "3"
            }

for l in lines:
    l = l.replace("\n", "")
    for n in l.split(" "):
        h = int(n, 16)
        data.append(h)

points = len(data) // 4

for i in range(points):
    point = (data[4 * i: 4 * i + 4])
    v = 0
    for i in range(4):
        v = v << 8
        v += point[i]
    point = v
    #print([hex(x) for x in point])
    if point in mappings:
        maze.append(mappings[point])
    else:
        maze.append("?")

for i in range(len(maze)):
    e = ""
    if ((i + 1) % 0x10) == 0:
        e = "\n"
    print(maze[i], end = e)


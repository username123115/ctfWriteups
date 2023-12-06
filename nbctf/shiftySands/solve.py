maze = [x for x in ".###.....#..#S.##..##.S#.#SS.##..#.#..##.S.#.#.SS..###.#.S.....#.#...S##.#.####..S.S.#..S...S..#LS.."]

playerX = 0
playerY = 0

width = 10
height = len(maze) // width
directions = ["V", "<", "^", ">"]

def printMaze(moves = 0, doDirections = True):
    global playerX, playerY
    phase = moves % 4
    indicator = directions[phase]
    if not doDirections:
        indicator = 'S'
    copy = list(maze)
    for i, c in enumerate(maze):
        if c == "S":
            copy[i] = indicator
    copy[playerY * width + playerX] = "@"
    m = "".join(copy)
    for i in range(height):
        print(m[i * width: (i + 1) * width])


def shift(moves = 0):
    global maze
    phase = moves % 4
    #shift down
    if phase == 0:
        for y in range(9, -1, -1):
            for x in range(10):
                targetIndex = y * height + x
                target = maze[targetIndex]
                if target == 'S':
                    if (0 <= y + 1 < height):
                        moveIndex = (y + 1) * width + x
                        if maze[moveIndex] == '.':
                            maze[targetIndex] = '.'
                            maze[moveIndex] = 'S'
    #shift left
    if phase == 1:
        for x in range(10):
            for y in range(10):
                targetIndex = y * height + x
                target = maze[targetIndex]
                if target == 'S':
                    if (0 <= x - 1 < width):
                        moveIndex = y * width + (x - 1)
                        if maze[moveIndex] == '.':
                            maze[targetIndex] = '.'
                            maze[moveIndex]='S'
    #shift up
    if phase == 2:
        for y in range(10):
            for x in range(10):
                targetIndex = y * height + x
                target = maze[targetIndex]
                if target == 'S':
                    if (0 <= y - 1 < height):
                        moveIndex = (y - 1) * width + x
                        if maze[moveIndex] == '.':
                            maze[targetIndex] = '.'
                            maze[moveIndex] = 'S'
    #shift right
    if phase == 3:
        for x in range(9, -1, -1):
            for y in range(10):
                targetIndex = y * height + x
                target = maze[targetIndex]
                if target == 'S':
                    if (0 <= x + 1 < width):
                        moveIndex = y * width + (x + 1)
                        if maze[moveIndex] == '.':
                            maze[targetIndex] = '.'
                            maze[moveIndex]='S'
moves = 0
winSeq = ""
#printMaze(0, False)
while (moves <= 0x31):
    printMaze(moves)
    shift(moves)
    moves += 1
    c = ''
    c = input('>')[0]
    oldx, oldy = playerX, playerY
    if c == "w":
        playerY -= 1
    if c == "a":
        playerX -= 1
    if c == "s":
        playerY += 1
    if c == "d":
        playerX += 1
    winSeq += c
    if c == "p":
        print(winSeq)
    tile = maze[playerY * width + playerX]
    if (tile == 'S') or (tile =='#'):
        playerX, playerY = oldx, oldy

    if maze[playerY * width + playerX] == 'S':
        break
    #printMaze(moves)

print("sssss")
print(winSeq)
printMaze(moves)

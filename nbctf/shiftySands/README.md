
# Shifty Sands #

## Overview ##

476 points

Category: [rev](../)

Tags: `nbctf 2023` `rev`

## Description ##

Can you escape the sand-filled maze before it's too late?

`nc chal.nbctf.com 30401`

Downloads:

[sands](https://nbctf.com/uploads?key=45737e2354719a9a27b6f537600086d445ae7ff72c585fa8b4df80fb855a9f9e%2Fsands)

## Solution ##

The initial binary given doesn't offer much information, as all it does is take your input without printing anything.
The only indication that something is happening is that sometimes the game prints "ssssssssss" and exits.

```
[danielj@daniel shiftySands]$ ./sands
wwwwwwww
ssssssd
asdfsd
fadsfdsfdsafdsaf
ssssssssss
```

We can decompile the program in Ghidra to get a look at whats happening. 
This is what main looks like after cleaning up and renaming some variables:

```c
undefined8 main(void)

{
  int input;
  undefined8 uVar1;
  long in_FS_OFFSET;
  int y;
  int x;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  y = 0;
  x = 0;
  while( true ) {
    do {
      input = getchar();
    } while ((char)input == '\n');
    shift();
    moves = moves + 1;
    move((int)(char)input,&y,&x);
    if ((0x31 < moves) || ((&map)[(long)y * 10 + (long)x] == 'S')) break;
    if ((&map)[(long)y * 10 + (long)x] == 'L') {
      win();
      uVar1 = 0;
LAB_00401bb8:
      if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
        return uVar1;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
  }
  puts("ssssssssss");
  uVar1 = 1;
  goto LAB_00401bb8;
}


```
The program has a global `map` variable that contains the initial map as a string. Looking at the arguments to the `move()` function
it can be assumed that the map is 10 tiles wide. If we print it out taking into consideration this width the map will look like this:

```
@###.....#
..#S.##..#
#.S#.#SS.#
#..#.#..##
.S.#.#.SS.
.###.#.S..
...#.#...S
##.#.####.
.S.S.#..S.
..S..#LS..
```

Where the player's position is indicated by the `@` symbol (it is on top of a `.`)

The program's main loop takes a non newline character from the input stream and processes it, incrementing global variable `moves`.
It repeats this until either `moves` exceeds 0x31 (49), the player moves into a `S`, or the player moves into the `L`. If
the player moves into the `L` tile the `win()` functioned is called, which prints the flag. Otherwise the loop is ended and the game
prints out "ssssssssss"

During processing of the input the game calls the two functions `shift()` and `move()`. `shift()` is called with no arguments while `move()`
takes the player's input and the player's position in the form of the `x` and `y` variables.

## shift() ##

`shift()` looks like the following:

```c

void shift(void)

{
  int phase;
  int y;
  int x;
  
  phase = moves % 4;
  if (phase == 3) {
    for (x = 9; -1 < x; x = x + -1) {
      for (y = 0; y < 10; y = y + 1) {
        if (((((&map)[(long)y * 10 + (long)x] == 'S') && (-1 < y)) && (y < 10)) &&
           (((-1 < x + 1 && (x + 1 < 10)) && ((&map)[(long)y * 10 + (long)(x + 1)] == '.')))) {
          (&map)[(long)y * 10 + (long)x] = '.';
          (&map)[(long)y * 10 + (long)(x + 1)] = 'S';
        }
      }
    }
  }
  else if (phase < 4) {
    if (phase == 2) {
      for (y = 0; y < 10; y = y + 1) {
        for (x = 0; x < 10; x = x + 1) {
          if ((((&map)[(long)y * 10 + (long)x] == 'S') && (-1 < y + -1)) &&
             ((y + -1 < 10 &&
              (((-1 < x && (x < 10)) && ((&map)[(long)(y + -1) * 10 + (long)x] == '.')))))) {
            (&map)[(long)y * 10 + (long)x] = '.';
            (&map)[(long)(y + -1) * 10 + (long)x] = 'S';
          }
        }
      }
    }
    else if (phase < 3) {
      if (phase == 0) {
        for (y = 9; -1 < y; y = y + -1) {
          for (x = 0; x < 10; x = x + 1) {
            if ((((&map)[(long)y * 10 + (long)x] == 'S') && (-1 < y + 1)) &&
               (((y + 1 < 10 && ((-1 < x && (x < 10)))) &&
                ((&map)[(long)(y + 1) * 10 + (long)x] == '.')))) {
              (&map)[(long)y * 10 + (long)x] = '.';
              (&map)[(long)(y + 1) * 10 + (long)x] = 'S';
            }
          }
        }
      }
      else if (phase == 1) {
        for (x = 0; x < 10; x = x + 1) {
          for (y = 0; y < 10; y = y + 1) {
            if ((((((&map)[(long)y * 10 + (long)x] == 'S') && (-1 < y)) && (y < 10)) &&
                ((-1 < x + -1 && (x + -1 < 10)))) && ((&map)[(long)y * 10 + (long)(x + -1)] == '.'))
            {
              (&map)[(long)y * 10 + (long)x] = '.';
              (&map)[(long)y * 10 + (long)(x + -1)] = 'S';
            }
          }
        }
      }
    }
  }
  return;
}
```

`shift()` modifies the `map` variable in four different ways. The way that `map` gets changed is dependent on the value of `moves` modulo four, which is
denoted as the `phase` variable. Every modification goes through the map and moves all `S` tiles one tile towards some other direction. This will
only happen for a given `S` tile if the new position for that `S` tile is a `.` tile. Because the map will get changed as the map gets iterated through,
a given `S` tile could have had a neighboring `S` tile during one point in the iteration, but not any more when it becomes time for it to be moved. For
this reason every one of the four transformations will iterate through the map in a different way to give the `S` tiles the highest chance of being moved.
(For example, the transformation that moves `S` tiles down will iterate `y` = 10 to `y` = 0 so that tiles at the bottom move down first, giving the `S` tiles above them a chance to move down if they were previously blocked by an `S` tile)

The ordering of the phases are as follows:

```
0: down
1: left
2: up
3: right
```

This function presents a unique challenge to this maze, as we have to be wary of how the deadly `S` tiles move as we navigate through the maze.

## move() ##

`move()` looks like the following:

```c

void move(char input,int *y,int *x)

{
  if (input == 'w') {
    if (*y == 0) {
      return;
    }
    if ((&map)[(long)(*y + -1) * 10 + (long)*x] == '#') {
      return;
    }
    if ((&map)[(long)(*y + -1) * 10 + (long)*x] == 'S') {
      return;
    }
    *y = *y + -1;
  }
  if (input == 'a') {
    if (*x == 0) {
      return;
    }
    if ((&map)[(long)*y * 10 + (long)(*x + -1)] == '#') {
      return;
    }
    if ((&map)[(long)*y * 10 + (long)(*x + -1)] == 'S') {
      return;
    }
    *x = *x + -1;
  }
  if (input == 's') {
    if (*y == 9) {
      return;
    }
    if ((&map)[(long)(*y + 1) * 10 + (long)*x] == '#') {
      return;
    }
    if ((&map)[(long)(*y + 1) * 10 + (long)*x] == 'S') {
      return;
    }
    *y = *y + 1;
  }
  if ((((input == 'd') && (*x != 9)) && ((&map)[(long)*y * 10 + (long)(*x + 1)] != '#')) &&
     ((&map)[(long)*y * 10 + (long)(*x + 1)] != 'S')) {
    *x = *x + 1;
  }
  return;
}
```

It uses the `map` global variable as the map and tests against the inputs `wasd`. If the player doesn't input one of
these letters it does nothing and a move ends up being wasted. Otherwise it determines if the position the player wants to
move to is valid by checking if the new position contains the `#` or `S` tiles. If the position doesn't contain these tiles,
the player is moved there by updating the `x` and `y` values. Otherwise nothing happens and a move is wasted. 
One thing to note is that `move()` doesn't care if a player is inside of a `S` tile or not, and that the game calls `move()` before
it checks if a player is in a `S` tile so the player can still save themselves if a `S` tile shifts into their position (The player isn't
represented as a tile on the map so sand can still shift onto the player if they're standing on a `.` tile.


## Implementation of game ##

As we know the layout of the map and how it will change over time, we can implement the game in python so that it will print out the map as
it changes, giving us a good shot of finding a solution.

My [implementation](./solve.py) displays the map during the beginning of each loop before `shift()` and `move()` are called and indicate the direction
in which the sands will shift. It also prints the input passed to it after pressing `p` allowing for us to record our moves. This allows for an easy
solve after figuring out that we can bypass tight corridors by letting the sand shift into our player and then moving away from it. The set of inputs
I used was [sdsssssassddssddwwwwwwwwwwdddssssdsssdsasasaa](./solve), which got me the flag after I connected to the challenge instance.

```
[danielj@daniel shiftySands]$ nc chal.nbctf.com 30401
sdsssssassddssddwwwwwwwwwwdddssssdsssdsasasaa
nbctf{5lowly_5huffl3d_5wa110wing_54nd5}
```


## Reflection ##

I spent a lot of time on this challenge with the majority dedicated to writing and debugging my implementation of my game,
but I feel like I could've completely skipped the implementation if I used the GDB python API to print out the contents of
`map` with some added things like direction and player indicators as the game ran as I would only need to access the `map`
and `moves` variables without having to worry about the rewriting the internal logic itself.
Although this idea completely skipped my mind when I was solving I think it'll be an excellent opportunity for me to learn to script GDB and
I'll likely update this write up with that solution once I get around to doing it.


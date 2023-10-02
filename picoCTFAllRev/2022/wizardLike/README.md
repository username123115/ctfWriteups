
# Wizardlike #

## Overview ##

500 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `binary` `game`

## Description ##

Do you seek your destiny in these deplorable dungeons? If so, you may want to look elsewhere. Many have gone before you and honestly, they've cleared out the place of all monsters, ne'erdowells, bandits and every other sort of evil foe. The dungeons themselves have seen better days too. There's a lot of missing floors and key passages blocked off. You'd have to be a real wizard to make any progress in this sorry excuse for a dungeon!
Download the [game](https://artifacts.picoctf.net/c/208/game).
'w', 'a', 's', 'd' moves your character and 'Q' quits. You'll need to improvise some wizardly abilities to find the flag in this dungeon crawl. '.' is floor, '#' are walls, '<' are stairs up to previous level, and '>' are stairs down to next level.

## First attempt ##

We are given a statically linked stripped binary that launches a game in the terminal. When first playing the game you can only progress up to the fourth level before you're left in a room with a gap that makes it impossible to travel to the stairs that take you to the next level. It also appears that the walls (`#`) block portions of the map from being revealed to you until you get past them. 

[walls blocking view](./images/wallsBlockView.png)!

To figure out whats happening in the game, I analyzed it using Ghidra. The result is a ton of unnamed functions as the binary was statically linked.

[Many functions](./images/functions.png)!

Initially I wanted to work in a top down fashion and reverse the functions that were called at the beginning of the code rather than the main game loop. I found a few useful functions during this time but most of the time I just wasted chasing down library functions. 

One function copies a bunch of characters that make up the entire map into a buffer while the other one initializes a same sized buffer to zeroes, this buffer is probably the one that is displayed to the players. These functions get called once at the start and everytime a player changes levels. 

```

void FUN_00401e6d_Copy2Map(long param_1)

{
  int i;
  int j;
  
  for (i = 0; i < 100; i = i + 1) {
    for (j = 0; j < 100; j = j + 1) {
      (&DAT_0053a4a0_Map)[(long)i * 100 + (long)j] =
           *(undefined *)((long)i * 100 + param_1 + (long)j);
    }
  }
  return;
}

```

```
void FUN_00401e05_InitBlankMap(void)

{
  int i;
  int j;
  
  for (i = 0; i < 100; i = i + 1) {
    for (j = 0; j < 100; j = j + 1) {
      (&DAT_00537d80_BlankMap)[(long)i * 100 + (long)j] = 0;
    }
  }
  return;
}
```

After a while I also tried using IDA FLIRT signatures to detect library functions but the ones I tried didn't end up finding anything so I gave up looking at some of the other functions that were called when initializing the game.

## Solution ##

Afterwards I come across a block of code that seems to be taking the player's input and deciding what do do based on it.

```
    iVar4 = FUN_00403a00_Fgets(DAT_00536b50_Stdin);
    if (iVar4 == 0x51) {
      playing = false;
    }
    else if (iVar4 == 0x77) {
      FUN_00402247_InputW();
    }
    else if (iVar4 == 0x73) {
      FUN_004022c3_InputS();
    }
    else if (iVar4 == 0x61) {
      FUN_0040233f_InputA();
    }
    else if (iVar4 == 100) {
      FUN_004023bb_InputD();
    }

```

All of these functions perform a collision check to see whether or not to update the player's position. As an example this is what gets called when you press `w`

```
void FUN_00402247_InputW(void)

{
  char cVar1;
  
  cVar1 = FUN_00402188_CheckCollision(DAT_00533f70_PlayerX,DAT_00533f74_PlayerY + -1);
  if (cVar1 != '\0') {
    if ((DAT_0053679c / 2 < DAT_00533f74_PlayerY) &&
       (DAT_00533f74_PlayerY <= 100 - DAT_0053679c / 2)) {
      DAT_00536794 = DAT_00536794 + -1;
    }
    DAT_00533f74_PlayerY = DAT_00533f74_PlayerY + -1;
  }
  return;
}
```

If the collision function returns `'\0'` that means the player would hit a wall or empty space if they move in their requested direction and nothing will happen. Otherwise, if any other value is returned, the game will move them in their requested direction.

The collision function simply checks whether or not the tile is a `'#'` or space a space.

```
undefined8 FUN_00402188_CheckCollision(int x,int y)

{
  undefined8 uVar1;
  
  if ((((x < 100) && (y < 100)) && (-1 < x)) && (-1 < y)) {
    if (((&DAT_0053a4a0_Map)[(long)y * 100 + (long)x] == '#') ||
       ((&DAT_0053a4a0_Map)[(long)y * 100 + (long)x] == ' ')) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}
```

What I did was patch two instructions using radare2 so that it would compare against something else so that the player wouldn't be stopped by the walls or blank spaces.

```
    004021f4 3c 23           CMP        AL,0x23
    ->
    004021f4 3c 55           CMP        AL,0x55
```

```
    0040222e 3c 20           CMP        AL,0x20
    ->
    0040222e 3c 55           CMP        AL,0x55
```

Now the only character that will stop the character is `'U'`, which isn't on the map. Now we can move around freely.

Moving around on the map unhindered lets us see that the map actually contains ascii art in the areas that we can't normally access.

[map](images/map.png)!

The first level spells out `picoCTF{`, the second spells out `ur_4_w1z4rd_`, and the other 8 levels each contribute 1 random character along with the final `}` at the end of the flag. Unfortunately, while we do have the ability to walk anywhere, its still quite tedious as we have to walk around in order to reveal the entire map. This is also incredibily annoying at the final level as most of it is covered in `#`'s, which hide the final characters. 

There is a chunk of code right before the player input handling that controls what is output to the player. 

```
    for (local_28 = 0; local_28 < iVar2; local_28 = local_28 + 1) {
      for (local_24 = 0; local_24 < iVar3; local_24 = local_24 + 1) {
        if ((((local_24 + DAT_00536790 < 100) && (local_28 + DAT_00536794 < 100)) &&
            (-1 < local_24 + DAT_00536790)) && (-1 < local_28 + DAT_00536794)) {
          cVar1 = FUN_00401f0e_CreateFog
                            (DAT_00533f70_PlayerX,DAT_00533f74_PlayerY,DAT_00536790 + local_24,
                             DAT_00536794 + local_28);
          if ((cVar1 != '\0') || ((&DAT_00537d80_BlankMap) [(long)(DAT_00536794 + local_28) * 100 + (long)(local_24 + DAT_00536790)] != '\0')) {
            (&DAT_00537d80_BlankMap)
            [(long)(DAT_00536794 + local_28) * 100 + (long)(local_24 + DAT_00536790)] = 1;
            local_12 = (ushort)(byte)(&DAT_0053a4a0_Map)
                                     [(long)(DAT_00536794 + local_28) * 100 +
                                      (long)(local_24 + DAT_00536790)];
            FUN_00406350(local_28,local_24,&local_12);
          }
        }
        else {
          FUN_00406350(local_28,local_24,&DAT_004de004);
        }
      }
    }
```

In this code, an area on the buffer `DAT_00537d80_BlankMap` is only written to with the characters from the level if `cVar1` is non zero or that area has already been revealed and written to. Because the buffer is initially set to all zeroes everytime we enter a new level, the amount of data that is written to it depends on the value of `cVar1` and thus the output of the function i've named `CreateFog`.  

Instead of reversing the function and figuring out what it does, I just patched it in radare2 so that it would always return 1 instead of zero, which should make it so that every tile of the level is written to the `BlankMap` buffer which is what is printed out. I do this by finding all points where the `EAX` register is set to zero and setting it to 1 instead.

```
    0x0040201a      b800000000     mov eax, 0
    ->
    0x0040201a      b801000000     mov eax, 1
```

```
    0x004020da      b800000000     mov eax, 0
    ->
    0x004020da      b801000000     mov eax, 1
```

With these patches, every level is visible immediately and you can just read the ascii art immediately. For example, here is level 10. Obviously it would take forever for someone to walk around and try to find the final two characters with all the walls blocking the way.

[level 10](images/10.png)!

Finally, by reading all the levels the flag is

`picoCTF{ur_4_w1z4rd_4844AD6F}`

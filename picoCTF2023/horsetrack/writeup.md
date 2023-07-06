*Disclaimer*: I didn't end up solving this challenge by myself and used the following writeups for help: <br>
* https://github.com/AlexSutila/picoCTF-2023-writeups/blob/main/horsetrack/horsetrack.md
* https://www.youtube.com/watch?v=6c4QSlJJADA&ab_channel=SloppyJoePirates

picoCTF2023 Horsetrack writeup:
From the challenge description this is heap exploitation? 
This will be my first heap exploitation challenge, sounds fun!

## First impressions

Apart from proving an executable for us to examine, we are also provided with a libc shared object and ld-linux shared object file. The executable will not run unless these files exist and have their permissions changed to be executable.

![add desc](images/firstImpressions.png)
When you do something wrong (like entering a name when the game prompts for name length) the game just kicks you out. 

Going over the character limit when setting the horse name doesn't do anything, as it turns out the extra characters just get ignored. 
![add desc](images/weirdLengthThing.png)

You must add horses in order to race, you can have a maximum of 18 horses as the stable index range is 0-17.
After you have 5 or more horses added, you can start racing. The horses all line up to race and go towards the finish line as the game prints out a nice representation of the horses' positions on the field.
![horses](images/race.png)

Long names get trunctuated to only 16 characters, it looks like it takes the first 16 characters of the horse name to display when racing, although when the winner is printed out we get the full name of the horse.
![add desc](images/trunctoBeg.png)

There is also a remove option that lets you remove an existing horse. 

## Reversing the binary

Now that all features have been explored, lets open the game in ghidra and see how it looks. <br>
Oh no where did all the symbols go (it is stripped file D:)
![add desc](images/noSymbols.png)

We can still use entry point to find main though, so its not too big of a deal! It seems main is located at `0x401c0c`
![We find entry](images/findingEntry.png)

Lets go to main and take a look at whats happening

```c
/* WARNING: Switch with 1 destination removed at 0x00401cea */
/* WARNING: Exceeded maximum restarts with more pending */

undefined8 main(void)

{
  long in_FS_OFFSET;
  uint local_24;
  int local_20;
  void *local_18;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_18 = malloc(0x120);
  local_24 = 0;
  local_20 = 0;
  FUN_00401b4d();
  FUN_0040130f(local_18);
  while (local_20 == 0) {
    puts("1. Add horse");
    puts("2. Remove horse");
    puts("3. Race");
    puts("4. Exit");
    printf("Choice: ");
    __isoc99_scanf(&DAT_0040204b,&local_24);
    if (local_24 < 5) {
                    /* WARNING: Could not find normalized switch variable to match jumptable */
                    /* WARNING: This code block may not be properly labeled as switch case */
      FUN_00401a39(local_18);
      uRam00000000004040ec = 1;
    }
    else {
      puts("Invalid choice");
    }
  }
  puts("Goodbye!");
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

Before going on with analysis of the game I want to note that there should be a switch statement in the decompiler output, but Ghidra was unable to properly display it. I solve this later by using the switch override script and manually specifying the jump destinations. The version of Ghidra used was 10.3 and it seems 10.1.3 doesn't have this issue so downgrading would also fix this.

0x120 bytes malloc()ed to **local_18**, which is then passed to **FUN_0040130f**, **FUN_00401b4d** is
called without arguments and doesn't return anything, we'll have to look into that.

**local_20** is checked against zero before the prompt screen appears and you are sent to goodbye
if it is nonzero, it is init to zero so one of the 4 options must change its value which is probably whats responsible for kicking us out when we give the game incorrect inputs, I'll call it **exitCondition**

**local_24** is probably user input seeing how it is read into, I'll rename it **userInput**.

Lets look at **FUN_00401b4d** first, it is the one passed no arguments
```c
void FUN_00401b4d(void)

{
  long in_FS_OFFSET;
  uint local_1c;
  FILE *local_18;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  local_18 = fopen("/dev/urandom","r");
  local_1c = 0;
  fread(&local_1c,4,1,local_18);
  fclose(local_18);
  srand(local_1c);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

It uses setbuf to change the type of buffering of the streams stdin, stdout, and stderr to unbuffered. I'm not too sure what difference this makes.

**local_1c** is an integer that gets filled with data from /dev/urandom, it is then passed to srand, which sets the random seed for rand() meaning it just sets the seed of rand using 4 bytes of data from /dev/urandom

Ok that function wasn't too interesting but its good to take a look at everything.

Next we'll look at **FUN_0040130f** that takes the 0x120 byte buffer as input

```c
void FUN_0040130f(long param_1)

{
  int i;
  
  for (i = 0; i < 0x12; i = i + 1) {
    *(undefined8 *)(param_1 + (long)i * 0x10) = 0;
    *(int *)(param_1 + (long)i * 0x10 + 8) = i;
    *(undefined4 *)(param_1 + (long)i * 0x10 + 0xc) = 0;
  }
  return;
}
```

It seems it divides these 0x120 bytes into 0x12 segments with 0x10 bytes each

`0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 |valc 0x00 0x00 0x00| 0x00 0x00 0x00 0x00`

Here is image of horses after being setup on the heap
![horses](images/initHorses.png)

This suggests that **local_18** might be an array with 0x12 elements, although there are multiple data types in each element. 0x12 is 18 in decimal, and we can have at most 18 horses, this means that **local_18** is an array of horse data structures. Based on how the function acts on this array, it seems that each horse data structure contains one 8 byte field and two 4 byte fields. Ok lets rename **local_18** to **horseData** and make it of type horseStruct*

![horses](images/horseInformation.png)

### Addressing broken switches
Most people won't have this problem I had, but I think i'm still going to include this section because it was something I had to solve in order to complete this challenge. You can skip this section if you want to, its not very important for solving this challenge in general.

Ghidra wasn't able to display the switch that involved basically all of the game logic so I had to take a look at some of the assembly instructions to figure out what was happening.
![switch instructions](images/switchInstructions.png)

As you can see, Ghidra isn't able to dissasemble any of the  bytes beyond where the different switch cases start. Looking at the instructions, a jump table is used to determine the addresses to jump to. This table is located at **0x402288** and consists of signed 4 byte integers.  The game adds these integers to the base address of the jump table, and because the jump table is so close to where the instructions to jump to are, it only needs to use 4 byte integers instead of 8 byte long integers. 

The jump table values are:

```0xfffffa65 0xfffffa80 0xfffffaa0 0xfffffac0 0xfffffb7a```

Signed they are:

```-0x59b -0x580 -0x560 -0x540 -0x486```

Note that there are 5 values because there is actually 5 options! Apart from the options 1-4 the game tells us about, there is also an option 0.

Adding these numbers to the address of the jump table, we get the following addresses to jump to:

```0x401ced 0x401d08 0x401d28 0x401d48 0x401e02``` 

After disassembling the undisassembled bytes and highlighting these addresses for the switch override script, the switch shows up!

The switch looks quite janky, but it goes from 0-4 for input from top to bottom.

```c

undefined8 main(void)

{
  int iVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  uint input;
  int exitCondition;
  int iStack_1c;
  horseStruct *horseData;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  horseData = (horseStruct *)malloc(0x120);
  input = 0;
  exitCondition = 0;
  FUN_00401b4d();
  FUN_0040130f(horseData);
  while (exitCondition == 0) {
    puts("1. Add horse");
    puts("2. Remove horse");
    puts("3. Race");
    puts("4. Exit");
    printf("Choice: ");
    __isoc99_scanf("%d",&input);
    if (input < 5) {
                    /* WARNING: Switch is manually overridden */
      switch(jumpTable[input]) {
      case -0x59b:
        FUN_00401a39(horseData);
        DAT_004040ec = 1;
        break;
      case -0x580:
        iVar1 = addHorse(horseData);
        if (iVar1 == 0) {
          exitCondition = 1;
        }
        break;
      case -0x560:
        iVar1 = removeHorse(horseData);
        if (iVar1 == 0) {
          exitCondition = 1;
        }
        break;
      case -0x540:
        if (DAT_004040ec == 0) {
          iVar1 = FUN_00401660(horseData);
          if (iVar1 == 0) {
            puts("Not enough horses to race");
          }
          else {
            while (iVar1 = FUN_004016b1(horseData), iVar1 == 0) {
              FUN_004017af(horseData);
              FUN_00401854(horseData);
            }
            uVar2 = FUN_00401715(horseData);
            printf("WINNER: %s\n\n",uVar2);
            for (iStack_1c = 0; iStack_1c < 0x12; iStack_1c = iStack_1c + 1) {
              horseData[iStack_1c].horseShort1 = 0;
            }
          }
        }
        else {
          puts("You have been caught cheating!");
          exitCondition = 1;
        }
        break;
      case -0x486:
        exitCondition = 1;
      }
    }
    else {
      puts("Invalid choice");
    }
  }
  puts("Goodbye!");
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

### Player options
Now that the switch and all the logic inside of it is displaying, we can take a look at the switch cases!

There are two functions I already named in the above code called addHorse() and removeHorse(), this is because they are fairly easy to find out based on what they print.

#### Add Horse
```c

undefined8 addHorse(horseStruct *horse)

{
  uint uVar1;
  undefined8 uVar2;
  void *pvVar3;
  long in_FS_OFFSET;
  uint stableIndex;
  int nameLength;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  stableIndex = 0;
  nameLength = 0;
  printf("Stable index # (0-%d)? ",0x11);
  __isoc99_scanf("%d",&stableIndex);
  if (((int)stableIndex < 0) || (0x11 < (int)stableIndex)) {
    puts("Invalid stable index");
    uVar2 = 0;
  }
  else if (horse[(int)stableIndex].horseShort2 == 0) {
    printf("Horse name length (%d-%d)? ",0x10,0x100);
    __isoc99_scanf("%d",&nameLength);
    uVar1 = stableIndex;
    if ((nameLength < 0x10) || (0x100 < nameLength)) {
      puts("Invalid horse name length");
      uVar2 = 0;
    }
    else {
      pvVar3 = malloc((long)(nameLength + 1));
      horse[(int)uVar1].horseLong = pvVar3;
      if (horse[(int)stableIndex].horseLong == 0) {
        puts("Failed to allocate memory for horse name");
        uVar2 = 0;
      }
      else {
        FUN_00401226(horse[(int)stableIndex].horseLong,nameLength);
        horse[(int)stableIndex].horseShort2 = 1;
        printf("Added horse to stable index %d\n",(ulong)stableIndex);
        uVar2 = 1;
      }
    }
  }
  else {
    puts("Stable location already in use");
    uVar2 = 0;
  }
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```

First the game recieves the stable index, which it indexes into horseData with. There is no overflow here because it checks if the stable index is within the bounds of the array. When the game gets the stable index, it checks if one of its fields **horseShort2** is set to zero, if its not, it tells us the stable location is already in use and returns a nonzero value, this will cause **exitCondition** to be set to something other then zero and kick us out of the game. If **horseShort2** isn't set, it checks for a name length to see if its within bounds (16-256) and allocates a buffer in heap to store the horse's name. It sets the horse's **horseLong** field to the buffer's address meaning that **horseLong** is a pointer to its name. The function **FUN_00401226** is tasked with populating this buffer with a name, it is passed the length of the name and the buffer address. Afterwards it sets **horseShort2** to 1 and returns. This means **horseShort2** marks whether a horse is in use.
Now we can update horseStruct

![updated horse struct](images/horseInformation2.png)


In race there is function I name checkForEnd that lookas at one of the numbers set in initheap
and sees if one is above 0x1d so I think its not actually stableIndex but position of horse

Function called later adds a number between 0-4 to horse position for every horse


Looking at gdb I look at heap to see what happens when add hors

Usefule info???

```
Redefine command "hook-stop"? (y or n) y
Type commands for definition of "hook-stop".
End with a line saying just "end".
>x/80wx 0x405290
>x/40wx 0x004055b0 - 0x10
>end
(gdb) info breakpoints 
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x0000000000401c65 
	breakpoint already hit 2 times
(gdb) 
```

Oppsie daisy looks like I forgot to look at remove horse function silly me :P
It turns out it frees the name pointer associated with the horse, but it does not get rid
of the pointer, so it is still in memory. This pointer can be accessed by headStart() because
it does not check if use bit is set before writing to address (hence why headStart on non-initialized
horse causes segfault because it is trying to write to NULL) Use after freee????

Doing some heap work I was going to give up until I looked a bit at a video by sloppyJoePirates and an azeria-labs
guide on heap exploitation. I still don't know if I'll be able to solve this but I do wanna explore a bit more.

Video points out as I failed to realize that writing \0xff to setHorseName or whatever function it is stops it from
reading anymore because it stops writing when char is -1 (255 = 0xff) for some weird reason. Basically you can make
horse which allocates a chunk, don't write anything to name, free horse, and make a new horse which will put it on the
same freed chunk. User data will have forward and backward pointers as long as you don't write anything when the game
asks for horse name (0xff) so when you race the game will leak these pointers.

Using GEF 
![unsorted bins](images/forceUnsortedBins.png)

From other writeups I learned that the fd pointers for heap chunks use something called safe linking which just means
that the fd pointer is mangled up a bit. What happens is you take the address of the fd pointer, shift it the the right
by 12 bits (you lose data), and xor it with the fd pointer. This makes it harder to do stuff even after leaking data because
you don't know where the fd pointer is pointing without the address of the fd pointer. However, this also means that theres
a way to leak the address of one special fd pointer, specifically tcache end of linked list. This pointer will be NULL, so
what happens is address >> 12 is xored with zero so the value stored here (which we can read) is just the address shifted
right by 12, precisely the value we need to forge a valid fd! Therefore if we can get target tcache chunk to be last at
linked list (this is done by having it added to tcache bin first), we can "sign" valid file pointers and pwn!!! I think you
can also use this to get address of code to pwn

Operation so far:
Allocate horses x12 (0-11)
HHHHHHHHHHHH
Free horses starting from end remove horses (11-0)
HHHHHHHHHHH<
HHHHHHHHHH<
HHHHHHHHH<
HHHHHHHH<
HHHHHHH<
HHHHHH<
HHHHH<
These go into tcache bin rest end up becoming unsorted
UUUUU		(unsorted chunks)
TTTTTT**T**		(tcache bold one should leak because it was free()ed first)

So basically horse 11 should have cheat go into it?

I've written some code that gets leaked addresses here is output
![leaked](images/gotLeakedAddress.png)
As you can see, 12 horses were initialized, but only 8 values were returned, this is because some of the horses were in
the large unsorted chunk, and some of the data areas are set to zero. The code ignores zeros, so this is all that is output.
Code looks like this

```python
def getPointers():
	p.sendlineafter("Choice: ", b"3")
	data = b""
	x = p.recvline()
	data += x
	while (not (b"WINNER" in x)):
		x = p.recvline()
		data += x
		if (b"\n\n" in data):
			print("done recieving data!")
			break
	somePointers = data.split(b"|")
	leakedPointers = []
	
	print(data)
	for pointer in somePointers:
		pointer = pointer.strip(b" \n")
		pointer = pointer.ljust(8, b"\x00")
		pointer = pwn.u64(pointer)
		if (pointer != 0):
			leakedPointers.append(pointer)
			print(hex(pointer))
	
	print(leakedPointers)
```

Sorry for very messy
From the output, everything below the large value containing 0x7fcaa4357040 is part of what was unsorted bin
Of course horse containing this addr should be 8th horse allocated (because it gets allocated after all the
tcache bins are allocated, so this is the orse in stable 7) Likewise horse containing forgable value is horse
6 because it goes into the tcache bin that was last freed.

Wait heap addresses are very large and what we get are heap shifted right 12 bits so almost all other pointers should
be heap shifted right 12 bits too so that means we can use the value thats leaked to decode addresses of all fd pointers
that are leaked!!! (and sign too)

Ok what??? So there are two values that get leaked that are one off to each other, one can be used to sign/decode tcache addresses
but the heap base address is different so it doesn't work for unsorted which means no libc :( but everytime I check gdb the key
for unsorted is alyways the latter of the two values thats one off, and its from a chunk in the middle of unsorted. Whaaat?
What does this mean

Ok it turns out pointer mangling happens on Tcache chunks but they do not happen on unsorted chunks so those are free to
exploit, I was trying to unmangle unsorted chunk FD pointers the entire time when that wasn't neccessary, which resulted in
wrong guesses for libc base. When I realized this, I started getting being able to correctly find libc base addr based on 
these leaks, now can do tcache poison and pwn!!!

First find address to override in GOT. We can choose any function that will be called later, we can change this function address
to that of libc sys and pass it a pointer to a string "/bin/sh", if we use free we can do just that, so lets overwrite free
to sys call and name a horse "/bin/sh" to pass it to.

![finding free](images/findingFree.png)

Free is at 0x404018 but we need to align addresses by 0x10 so we need to alloc 8 bits below free at 0x404010. What we can do
is free two horses which will place two chunks into tcache bin. Bin -> T1 -> T2, We can modify T1 next pointer, normally
it will point to T2, but we can set it to point to 0x404010 (also note that value at 0x404010 is 0x0000000000000000 so it will
appear as end of chain). Afterwards we can allocate a chunk of same size as bin size which will allocate a bin at where
T1 points, giving us the ability to write to 0x404010. 








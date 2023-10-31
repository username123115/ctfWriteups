
# riscy business #

## Overview ##

300 points

Category: [picoMini by redpwn](../)

Tags: `picoMini by redpwn` `Reverse Engineering`

## Description ##

Try not to take too many riscs when finding the flag.

[download riscy](https://artifacts.picoctf.net/picoMini+by+redpwn/Reverse+Engineering/riscy/riscy)

## Solution ##

The binary we are given was compiled for the RISC-V architecture. Because my laptop does not run on this architecture, I won't be able to run the program unless I emulate it.

We can emulate the architecture using QEMU, I followed [this guide by azeria labs](https://azeria-labs.com/arm-on-x86-qemu-user/) to do so.

```
[danielj@daniel riscy]$ qemu-riscv64 riscy
You've gotten yourself into some riscy business...
Got yourself a flag for me?
>
```

After providing an input, the program either responds with

`You need to take some more riscs than that.`

or

`That was a bit too riscy for me!`

depending on whether or not the input was longer then 7 characters or not.

Opening the binary in Ghidra gives us a better view of whats happening, although when annoying problem is that Ghidra is unable to tell what the `ecall` instructions are doing, so we are going to have to use a syscall table to figure those out.


```c
void entry(void)

{
  byte bVar1;
  long inputLength;
  byte *userInput;
  byte bVar2;
  byte *pbVar3;
  byte *pbVar4;
  byte abStack_179 [65];
  char array [272];
  
                    /* Sys call 0x40 (write) a buffer with the contents "You've gotten yourself
                       into..." to stdout */
  ecall();
  userInput = (byte *)((long)register0x00002010 + -0x178);
                    /* Sys call 0x3f (read) from stdin (0x40 bytes max), number of bytes read is put
                       into a0 register */
  ecall();
  do {
    ecall();
    FUN_00010078Exit(1,"You need to take some more riscs than that.\n",0x2c,0x40);
  } while (inputLength < 8);
                    /* This is really hard to reverse engineer... but it only takes the first 8
                       characters of your input as a "key" which should be "picoCTF{"~ */
  generateArray(array,userInput,8);
  pbVar3 = userInput;
  do {
    bVar1 = *pbVar3;
    bVar2 = getByte(array);
    pbVar4 = pbVar3 + 1;
    *pbVar3 = bVar1 ^ bVar2;
    pbVar3 = pbVar4;
  } while (userInput + (inputLength - (long)pbVar4) != (byte *)0x0);
  pbVar3 = &DAT_00010210;
  do {
    bVar1 = *userInput;
    bVar2 = *pbVar3;
    userInput = userInput + 1;
    pbVar3 = pbVar3 + 1;
    if (bVar1 != bVar2) goto LAB_000101f2;
  } while (pbVar3 != &UNK_00010244);
  ecall();
  FUN_00010078Exit(0,"Success!\n",9,0x40);
LAB_000101f2:
  ecall();
  FUN_00010078Exit(1,"That was a bit too riscy for me!\n",0x21,0x40);
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}
```

From here we can see that our input is being checked to have length greater then
length 8 before being used in the `generateArray` function. Afterwards our input gets
xor-red from elements of that array using the `getByte` function before being compared
against a desired output stored at `0x10210`. I'm going to solve by figuring out what
these functions are doing and implement them in python to get our flag.

### generateArray ###

```c
void generateArray(byte *array,byte *input,ulong modulus)

{
  ulong j;
  ulong uVar1;
  long i;
  ulong uVar2;
  byte *pbVar3;
  byte currentChar;
  
  i = 0;
  do {
    array[i] = (byte)i;
    i = i + 1;
  } while (i != 0x100);
  j = 0;
  uVar2 = 0;
  pbVar3 = array;
  do {
    uVar1 = j % modulus;
    currentChar = *pbVar3;
    j = j + 1;
    uVar1 = (ulong)(int)((int)uVar2 + (uint)input[uVar1] + (uint)currentChar);
    uVar2 = uVar1 & 0xff;
    *pbVar3 = array[uVar1 & 0xff];
    array[uVar1 & 0xff] = currentChar;
    pbVar3 = pbVar3 + 1;
  } while (j != 0x100);
  return;
}
```

It seems that the first 256 elements of the array get filled with the values 0 to 255 before being shuffled
around depending on the input given. One thing to note is that only the first 8 bytes of the input is
used for shuffling the values of the array. This is good because the first 8 characters of our flag is
`picoCTF{`, which means the final array will have the same value as calling `generateArray` with an
input of `picoCTF{`

Here is an implementation in python:

```python

array = [0 for i in range(272)]
def generateArray():
    global array
    key = "picoCTF{"
    u = 0

    for i in range(0x100):
        array[i] = i

    for i in range(0x100):
        j = i % 8
        current = array[i]
        j = u + ord(key[j]) + current
        u = j & 0xff
        array[i] = array[j & 0xff]
        array[j & 0xff] = current
```

### getByte ###

This function takes as input our generated array. Because we already know what this array is going
to look like, we just need to figure out what this function is outputting and xor it against the
desired output to find the desired input.

Decompiler output:

```c
char getByte(char *param_1)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  
  cVar1 = param_1[0x100];
  cVar2 = param_1[0x101];
  param_1[0x100] = cVar1 + 1U;
  cVar3 = param_1[(byte)(cVar1 + 1U)];
  param_1[0x101] = cVar2 + cVar3;
  cVar4 = param_1[(byte)(cVar2 + cVar3)];
  param_1[(byte)(cVar1 + 1U)] = cVar4;
  param_1[(byte)(cVar2 + cVar3)] = cVar3;
  return param_1[(byte)(cVar3 + cVar4)];
}
```

Implementation in python:

```python
def getByte():
    global array
    v1 = array[0x100]
    v2 = array[0x101]

    array[0x100] = 1 + v1
    v3 = array[(1 + v1) % 0x100]
    
    array[0x101] = v2 + v3
    v4 = array[(v2 + v3) % 0x100]

    array[(1 + v1) % 0x100] = v4
    array[(v2 + v3) % 0x100] = v3
    return array[(v3 + v4) % 0x100]
```

### solving ###

Combining these two function implementations and our desired output, we can run the following script:

```python
array = [0 for i in range(272)]
def generateArray():
    global array
    key = "picoCTF{"
    u = 0

    for i in range(0x100):
        array[i] = i

    for i in range(0x100):
        j = i % 8
        current = array[i]
        j = u + ord(key[j]) + current
        u = j & 0xff
        array[i] = array[j & 0xff]
        array[j & 0xff] = current

def getByte():
    global array
    v1 = array[0x100]
    v2 = array[0x101]

    array[0x100] = 1 + v1
    v3 = array[(1 + v1) % 0x100]
    
    array[0x101] = v2 + v3
    v4 = array[(v2 + v3) % 0x100]

    array[(1 + v1) % 0x100] = v4
    array[(v2 + v3) % 0x100] = v3
    return array[(v3 + v4) % 0x100]

generateArray()

d = [197, 117, 149, 165, 129, 128, 243, 68, 241, 153, 52, 129, 58, 95, 80, 147, 103, 238, 18, 12, 21, 58, 218, 28, 111, 80, 128, 73, 99, 242, 54, 211, 147, 100, 70, 99, 132, 181, 58, 90, 156, 62, 64, 245, 25, 32, 127, 8, 0, 72, 10, 3]

for k in d:
    y = getByte()
    char = y ^ k
    print(chr(char), end="")

print("")
```

To get the flag

`picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}`


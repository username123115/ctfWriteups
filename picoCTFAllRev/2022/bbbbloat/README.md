
# bbbbloat #

## Overview ##

300 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `binary` `obfuscation`

## Description ##

Can you get the flag?
Reverse engineer [this](https://artifacts.picoctf.net/c/45/bbbbloat) binary.

## Solution ##

We are given a binary that asks us for a number. Opening in Ghidra it seems to be comparing our input to the number 0x86187 or 549255.

```c
...
  __isoc99_scanf(&DAT_00102020,&input);
  local_44 = 0xd2c49;
  if (input == 0x86187) {
    local_44 = 0xd2c49;
    local_40 = (char *)FUN_00101249(0,&local_38);
    fputs(local_40,stdout);
    putchar(10);
    free(local_40);
  }
...
```

If we input this number we get the flag

```
[danielj@daniel bloat]$ ./bbbbloat
What's my favorite number? 549255
picoCTF{cu7_7h3_bl047_36dd316a}
```

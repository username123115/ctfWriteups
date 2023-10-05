
# Unpackme #

## Overview ##

300 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `binary` `packed`

## Description ##

Can you get the flag?
Reverse engineer [this](https://artifacts.picoctf.net/c/203/unpackme-upx) binary.

## Solution ##

We are given a binary called "unpackme-upx" and the hint asks us "What is UPX?". A search reveals that UPX is a packer for executables, which means that the program we are given contains a stub for un-compressing and running the main program. We can confirm this is a program packed by UPX by running the strings on it and searching for UPX. 

```
...
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.95 Copyright (C) 1996-2018 the UPX Team. All Rights Reserved. $
...
```

Because the main program has been compressed, we can't analyze what it's doing until we extract its contents. Fortunately we can use the `upx` utility to extract the main program by using the `-d` flag. `upx -d unpackme-upx -o chal` will leave us with the extracted program with the name of `chal`. In the disassembly of this program we see that it'll print the flag if we input "754635".

```c
...
  if (input == 0xb83cb) {
    local_40 = (char *)rotate_encrypt(0,&local_38);
    fputs(local_40,(FILE *)stdout);
    putchar(10);
    free(local_40);
  }
...
```

Now to get the flag

```
[danielj@daniel unpackme]$ ./unpackme-upx
What's my favorite number? 754635
picoCTF{up><_m3_f7w_77ad107e}
```


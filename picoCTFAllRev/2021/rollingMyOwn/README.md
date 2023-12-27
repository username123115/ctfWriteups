
# Rolling My Own #

## Overview ##

300 points

Category: [picoCTF 2021](../)

Tags: `picoCTF 2021` `Reverse Engineering`

## Description ##

I don't trust password checkers made by other people, so I wrote my own. It doesn't even need to store the password! If you can crack it I'll give you a flag.

[remote](https://mercury.picoctf.net/static/8224230849be08fe780b22f7578fa034/remote) 

`nc mercury.picoctf.net 5075`

## Solution ##

Paper in the hints is also available [here](https://pages.cpsc.ucalgary.ca/~aycock/papers/eicar06-ad.pdf)

The paper describes a method of hiding code so that it only runs when a correct key is provided.
The way this works is that a salt is combined with part of a key and hashed, the byte sequence from bytes `lb` to `ub` of this resulting hash is called the `run` and used as part of the code. 

The idea is that somebody will start with a known key and desired sequence and start searching for salts such that the hash of the combined key and salt contains the desired sequence. From there `lb` and `ub` are needed to specify the location of that byte sequence. The paper also states that in order to find a `run` containing b bits, the hash generally needs to be b-1 bits long.

In this challenge, we provide a 16 character key (more characters get ignored) that gets split up evenly into four 4 character keys with an 8 byte salt.

Our program looks like this:

```c
undefined8 main(void)

{
  size_t keyLength;
  uchar *hashed;
  undefined8 *run;
  long in_FS_OFFSET;
  int i;
  int j;
  int offsets [4];
  uchar local_d8 [16];
  char salts [33];
  char key [65];
  char mixed [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdout,(char *)0x0);
  salts[0] = 'G';
  salts[1] = 'p';
  salts[2] = 'L';
  salts[3] = 'a';
  salts[4] = 'M';
  salts[5] = 'j';
  salts[6] = 'E';
  salts[7] = 'W';
  salts[8] = 'p';
  salts[9] = 'V';
  salts[10] = 'O';
  salts[11] = 'j';
  salts[12] = 'n';
  salts[13] = 'n';
  salts[14] = 'm';
  salts[15] = 'k';
  salts[16] = 'R';
  salts[17] = 'G';
  salts[18] = 'i';
  salts[19] = 'l';
  salts[20] = 'e';
  salts[21] = 'd';
  salts[22] = 'p';
  salts[23] = '6';
  salts[24] = 'M';
  salts[25] = 'v';
  salts[26] = 'c';
  salts[27] = 'e';
  salts[28] = 'z';
  salts[29] = 'x';
  salts[30] = 'l';
  salts[31] = 's';
  salts[32] = '\0';
  offsets[0] = 8;
  offsets[1] = 2;
  offsets[2] = 7;
  offsets[3] = 1;
  memset(key + 1,0,0x40);
  memset(mixed,0,0x40);
  printf("Password: ");
  fgets(key + 1,0x40,stdin);
                    /* Null terminate key
                        */
  keyLength = strlen(key + 1);
  key[keyLength] = '\0';
  for (i = 0; i < 4; i = i + 1) {
    strncat(mixed,key + (long)(i << 2) + 1,4);
    strncat(mixed,salts + (i << 3),8);
  }
  hashed = (uchar *)malloc(0x40);
  keyLength = strlen(mixed);
                    /* This calculates 4 hashes in total, one for each group of 4 input chars and 8
                       precomputed ones. Each hash contributes 4 bytes of code to the end result,
                       offsets 8 through 11 inclusive */
  runHash(hashed,mixed,(int)keyLength);
  for (i = 0; i < 4; i = i + 1) {
    for (j = 0; j < 4; j = j + 1) {
      local_d8[j * 4 + i] = hashed[offsets[j] + j * 0x10 + i];
    }
  }
  run = (undefined8 *)mmap((void *)0x0,0x10,7,0x22,-1,0);
  *run = local_d8._0_8_;
  run[1] = local_d8._8_8_;
  (*(code *)run)(win);
  free(hashed);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

The salts are "GpLaMjEW", "pVOjnnmk", "RGiledp6", and "Mvcezxls".
If our input was `aaaabbbbccccdddd` we would end up with four sub-keys like

```
aaaaGpLaMjEW
bbbbpVOjnnmk
ccccRGiledp6
ddddMvcezxls
```

Stored like that (without spaces) in the string `mixed`

The offsets are stored in the array `offsets` and contain the value of `lb` for each sub-key.
The value of `ub` seems to be 4 greater then the value of `lb` as suggested by the loop running after `runHash()` is called. 
The value of the offsets are 8, 2, 7, and 1

`runHash()` takes in as input a 0x40 byte buffer `hashed`, the `mixed` string with the salted sub-keys, and the length of the `mixed` string.
It calculates the MD5 hash of each 12 byte hashed sub-key and stores the resulting 0x10 byte hash in the `hashed` buffer, one after another until all 4 keys have been hashed.

```c

void runHash(uchar *output,uchar *input,int length)

{
  int blocks;
  long in_FS_OFFSET;
  uchar *currentData;
  int i;
  int j;
  int bytes;
  MD5_CTX context;
  uchar hash [24];
  long local_10;
  
                    /* Take an array of 12 byte keys (4 byte sub-key + 8 byte salt) and store their
                       hashes in the output array */
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (length % 0xc == 0) {
    blocks = length / 0xc;
  }
  else {
    blocks = length / 0xc + 1;
  }
  currentData = input;
  for (i = 0; i < blocks; i = i + 1) {
    bytes = 0xc;
                    /* remaining bytes if length of message does not evenly divide 0xc */
    if ((i == blocks + -1) && (length % 0xc != 0)) {
      bytes = blocks % 0xc;
    }
    MD5_Init(&context);
    MD5_Update(&context,currentData,(long)bytes);
    currentData = currentData + bytes;
    MD5_Final(hash,&context);
                    /* because hash results in a 128 bit or 16 byte result */
    for (j = 0; j < 0x10; j = j + 1) {
      output[(i * 0x10 + j) % 0x40] = hash[j];
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

After hashing the keys and adding each of the 4 byte sub-sequences to `run`, the program interprets `run` as a function and calls it with the address of the `win()` function.

Now, the objective is clear. 
We have four sub-keys that when salted and hash generate a 4 byte sequence each. 
This means we have to create code with at most 16 bytes that manages to call `win()`, however, we can't just call `win()` by itself.

```c
void win(long param_1)

{
  FILE *__stream;
  long in_FS_OFFSET;
  char local_98 [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (param_1 == 0x7b3dc26f1) {
    __stream = fopen("flag","r");
    if (__stream == (FILE *)0x0) {
      puts("Flag file not found. Contact an admin.");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    fgets(local_98,0x80,__stream);
    puts(local_98);
  }
  else {
    puts("Hmmmmmm... not quite");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Win needs as an argument the value 0x7b3dc26f1, meaning that along with calling `win()`, we need to set the `rdi` register to 0x7b3dc26f1.

This is simple enough, and our code looks like this:

```
mov rsi, rdi
mov rdi, 0x7b3dc26f1
call rsi
```

We save the address of `win()` in `rsi` and set `rdi` to 0x7b3dc26f1 before calling `rsi`, which will call `win()` with the first parameter as our desired number.

This bit of assembly looks like this when assembled:

```
48 89 fe
48 bf f1 26 dc b3 07 00 00 00
ff d6 ??
```

Or

```
48 89 fe 48 ;key1
bf f1 26 dc ;key2
b3 07 00 00 ;key3
00 ff d6 ?? ;key4
```

Where the ?? means that the byte is unneeded and can be any value

Knowing this, we can can brute force these solutions as the guessable part of each key is only 4 bytes and we can narrow our search to printable characters! (Also the hint tells us the first part of the key is `D1v1` so we only need to brute force 3 sets of keys)

The script [solve.py](./solve.py) brute forces all solutions and finds the solution in around 3 minutes.

The final key will be `D1v1d3AndC0nqu3r` and when we submit it at the challenge instance we get a flag!

```
[danielj@daniel rollingMyOwn]$ nc mercury.picoctf.net 5075
Password: D1v1d3AndC0nqu3r
picoCTF{r011ing_y0ur_0wn_crypt0_15_h4rd!_f3d54f2d}
```

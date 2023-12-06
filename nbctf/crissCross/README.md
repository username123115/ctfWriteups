
# Crisscross #

## Overview ##

446 points

Category: [rev](../)

Tags: `nbctf 2023` `rev`

## Description ##

X

Downloads:

[main.py](https://nbctf.com/uploads?key=226a4fcb29d86ff64b45df06af6a6819a63383ce9021605538f307bd783c322d%2Fmain.py)

[output.txt](https://nbctf.com/uploads?key=6b15e29dba2992e4e982e270f86164dd96b97ab3d16cccc2973a19d9cd27df1a%2Foutput.txt)

## Solution ##

The python file defines an encoding operation `enc()` that takes in two keys, one which contains 20 random integers from 0 to 255 and another 
that contains the numbers 1-256 in a random order. `enc()` takes in an integer and returns two values. The value of the two keys and the result of
an operation involving involving `enc` and the flag is given to us, and we need to find the original flag given these three values.

The operation that we are given the result of looks like this: (`x` is the third value we are given along with the keys)

```
x = 0
for i, c in enumerate(flag):
    x <<= 8
    n, w = enc(c)
    if i % 2:
        n, w = w, n
    x |= n
    x |= w << ((2 * i + 1) * 8)
```

Where flag is a byte array. This means that every byte of the flag will result in two bytes of output as `n` and `w` from `enc()` are embedded seperately
into `x`. If we print the status of the operation on a dummy flag we can see how `n` and `w` are embedded into `x`. The modified program 
[display.py](./display.py) demonstrates how the dummy flag 'abc' gets operated on by the program.


```
[danielj@daniel crissCross]$ python display.py
77777777 66666666 55555555 44444444 33333333 22222222 VVVVVVVV 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000

start
77777777 66666666 55555555 44444444 33333333 22222222 VVVVVVVV 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000

77777777 66666666 55555555 44444444 33333333 22222222 VVVVVVVV 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00011101

77777777 66666666 55555555 44444444 33333333 22222222 VVVVVVVV 00000000
00000000 00000000 00000000 00000000 00000000 00000000 10100111 00011101

new
77777777 66666666 55555555 44444444 VVVVVVVV 22222222 11111111 00000000
00000000 00000000 00000000 00000000 00000000 10100111 00011101 00000000

77777777 66666666 55555555 44444444 VVVVVVVV 22222222 11111111 00000000
00000000 00000000 00000000 00000000 00000000 10100111 00011101 11110001

77777777 66666666 55555555 44444444 VVVVVVVV 22222222 11111111 00000000
00000000 00000000 00000000 00000000 11001001 10100111 00011101 11110001

new
77777777 66666666 VVVVVVVV 44444444 33333333 22222222 11111111 00000000
00000000 00000000 00000000 11001001 10100111 00011101 11110001 00000000

77777777 66666666 VVVVVVVV 44444444 33333333 22222222 11111111 00000000
00000000 00000000 00000000 11001001 10100111 00011101 11110001 11001011

77777777 66666666 VVVVVVVV 44444444 33333333 22222222 11111111 00000000
00000000 00000000 11100101 11001001 10100111 00011101 11110001 11001011

new
VVVVVVVV 66666666 55555555 44444444 33333333 22222222 11111111 00000000
00000000 11100101 11001001 10100111 00011101 11110001 11001011 00000000

VVVVVVVV 66666666 55555555 44444444 33333333 22222222 11111111 00000000
00000000 11100101 11001001 10100111 00011101 11110001 11001011 10100101

VVVVVVVV 66666666 55555555 44444444 33333333 22222222 11111111 00000000
00101000 11100101 11001001 10100111 00011101 11110001 11001011 10100101

new
77777777 66666666 55555555 44444444 33333333 22222222 VVVVVVVV 00000000
00101000 11100101 11001001 10100111 00011101 11110001 11001011 10100101

```

As seen here bytes get added to the outer edges of `x` while the stuff in the "middle" remains unchanged. When `i` is even the value of 
`w` of `enc(flag[i])` is stored to the left while the value of `n` is stored to the right, this order gets reversed when `i` is odd. We
can use this fact to seperate the `x` we were given into the values of `w` and `n` for each byte of the flag.

The program [unTangle.py](./unTangle.py) prints out a list of tuples such that item `i` of the list contains `w` and `n` for byte `i` of
the flag.

```
[danielj@daniel crissCross]$ python unTangle.py
[(14, 106), (235, 234), (171, 127), (2, 77), (156, 66), (197, 66), (171, 127), (182, 106), (62, 164), (196, 81), (36, 87), (31, 222), (171, 127), (182, 106), (4, 73), (36, 87), (36, 87), (31, 222), (36, 87), (2, 77), (182, 106), (161, 154), (22, 234), (235, 234), (1, 66), (182, 106), (182, 106), (58, 87), (31, 222), (36, 87), (161, 154), (146, 162), (254, 73), (1, 66), (144, 234)]
```

Using these results we can brute force every byte of the flag by trying values between 0 and 255 and seeing of their values of `w` and `v` match the
ones given in the list. See [solve.py](./solve.py) for an implementation.

```
[danielj@daniel crissCross]$ python solve.py
nbctf{cr15s_cr0ss_str4wb3rry_s4uz3}
```



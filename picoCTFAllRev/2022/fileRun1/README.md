
# file-run1 #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering`

## Description ##

A program has been provided to you, what happens if you try to run it on the command line? 
Download the program [here](https://artifacts.picoctf.net/c/220/run).

## Solution ##

Add executable permission and run the program.

```
[danielj@daniel fileRun1]$ chmod +x run
[danielj@daniel fileRun1]$ ./run
The flag is: picoCTF{U51N6_Y0Ur_F1r57_F113_47cf2b7b}
```

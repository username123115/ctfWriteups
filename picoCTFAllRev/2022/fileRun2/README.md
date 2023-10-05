
# file-run2 #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering`

## Description ##

Another program, but this time, it seems to want some input. What happens if you try to run it on the command line with input "Hello!"?
Download the program [here](https://artifacts.picoctf.net/c/157/run).

## Solution ##

Add executable permission and run the file with argument `Hello!`

```
[danielj@daniel fileRun2]$ chmod +x run
[danielj@daniel fileRun2]$ ./run Hello!
The flag is: picoCTF{F1r57_4rgum3n7_f65ed63e}
```




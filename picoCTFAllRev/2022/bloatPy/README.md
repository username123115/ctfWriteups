
# bbbbloat #

## Overview ##

200 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `obfuscation`

## Description ##

Can you get the flag?
Reverse engineer [this](https://artifacts.picoctf.net/c/45/bbbbloat) binary.
Run this [Python program](https://artifacts.picoctf.net/c/105/flag.txt.enc) in the same directory as this [encrypted flag](https://artifacts.picoctf.net/c/105/flag.txt.enc).

## Solution ##

When running the program we are prompted for a password.

```
Please enter correct password for flag: adfssdf
That password is incorrect
```

It seems we need to find the correct password. Looking at the python file, we see that the function which asks us for input is called `arg232` 

```python
def arg232():
  return input(a[47]+a[75]+a[68]+a[64]+a[82]+a[68]+a[94]+a[68]+a[77]+a[83]+\
a[68]+a[81]+a[94]+a[66]+a[78]+a[81]+a[81]+a[68]+a[66]+a[83]+\
a[94]+a[79]+a[64]+a[82]+a[82]+a[86]+a[78]+a[81]+a[67]+a[94]+\
a[69]+a[78]+a[81]+a[94]+a[69]+a[75]+a[64]+a[70]+a[25]+a[94])
```

This gets called somewhere near the end and the result is stored in the variable `arg432` which is passed into the function `arg133`

```python
arg444 = arg132()
arg432 = arg232()
arg133(arg432)
arg112()
arg423 = arg111(arg444)
print(arg423)
sys.exit(0)
```

`arg133` compares the input against the password, if its correct it returns true and if its incorrect it exits. 

```python
def arg133(arg432):
  if arg432 == a[71]+a[64]+a[79]+a[79]+a[88]+a[66]+a[71]+a[64]+a[77]+a[66]+a[68]:
    return True
  else:
    print(a[51]+a[71]+a[64]+a[83]+a[94]+a[79]+a[64]+a[82]+a[82]+a[86]+a[78]+\
a[81]+a[67]+a[94]+a[72]+a[82]+a[94]+a[72]+a[77]+a[66]+a[78]+a[81]+\
a[81]+a[68]+a[66]+a[83])
    sys.exit(0)
    return False
```

However, I don't want to spend the time deciphering the password so instead I'll just patch it to return True regardless of the password.

```python
def arg133(arg432):
    return True
```

Now when we run the program it will give us the flag regardless of the password that we input.

```
[danielj@daniel bloatPY]$ python bloat.flag.py
Please enter correct password for flag: ignored
Welcome back... your flag, user:
picoCTF{d30bfu5c4710n_f7w_5e14b257}
```


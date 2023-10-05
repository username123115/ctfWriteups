
# patchme.py #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering`

## Description ##

Can you get the flag?
Run this [Python program](https://artifacts.picoctf.net/c/200/patchme.flag.py) in the same directory as this [encrypted flag](https://artifacts.picoctf.net/c/200/flag.txt.enc).

## Solution ##

We are asked for a password, lookinng at the file we see that the file is decrypted if the password is correct.

```python
def level_1_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    if( user_pw == "ak98" + \
                   "-=90" + \
                   "adfjhgj321" + \
                   "sleuth9000"):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), "utilitarian")
        print(decryption)
        return
    print("That password is incorrect")
```

We can patch it to give us the decrypted contents without asking for a password.

```
def level_1_pw_check():
    print("Welcome back... your flag, user:")
    decryption = str_xor(flag_enc.decode(), "utilitarian")
    print(decryption)
```

Running the patched file we get our flag.

```
[danielj@daniel patchmePy]$ python patchme.flag.py
Welcome back... your flag, user:
picoCTF{p47ch1ng_l1f3_h4ck_c4a4688b}
```



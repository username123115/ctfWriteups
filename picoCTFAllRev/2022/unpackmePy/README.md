
# unpackme.py #

## Overview ##

100 points

Category: [picoCTF 2022](../)

Tags: `picoCTF 2022` `Reverse Engineering` `packing`

## Description ##

Can you get the flag?
Reverse engineer this [Python program](https://artifacts.picoctf.net/c/50/unpackme.flag.py).

## Solution ##

When we run the program we are asked for a password. Looking at the program itself, it seems that it decrypts some code and run it.

```python
...
key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())
f = Fernet(key_base64)
plain = f.decrypt(payload)
exec(plain.decode())
```

We can print out whats being executed by modifying the source code.

```python
...
code = plain.decode()
print(code)
exec(code)
```

The code being ran is

```python
pw = input('What\'s the password? ')

if pw == 'batteryhorse':
  print('picoCTF{175_chr157m45_85f5d0ac}')
else:
  print('That password is incorrect.')
```

The password is `batteryhorse` and the flag is `picoCTF{175_chr157m45_85f5d0ac}`

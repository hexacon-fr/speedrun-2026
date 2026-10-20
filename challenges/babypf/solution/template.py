#!/usr/bin/python3
from pwn import *

elf = ELF('./babypf')

context.arch = 'amd64'
context.log_level = 'debug'

if __name__ == '__main__':
    flag = b'HXN{...}'

    r = elf.process()
    r.sendlineafter(b'Flag: ', flag)
    print(r.recvall().decode().strip())
    r.close()

#!/usr/bin/python3
from pwn import *

elf = ELF('./unchained')

context.arch = 'amd64'
context.log_level = 'debug'

if __name__ == '__main__':
    flag = b'HXN{...}'

    r = elf.process([flag])
    print(r.recvall().decode().strip())
    r.close()

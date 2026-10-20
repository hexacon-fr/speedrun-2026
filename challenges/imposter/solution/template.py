#!/usr/bin/python3

from pwn import *

elf = ELF('./imposter')

context.arch = 'amd64'
context.log_level = 'debug'

if __name__ == '__main__':
    flag = 'HXN{...}'

    r = elf.process()
    r.sendlineafter(b'Enter password: ', flag)
    print(r.recvall().decode().strip())


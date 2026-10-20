#!/usr/bin/python3

from pwn import *

"""
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
"""

elf = ELF('./dompwnify')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

def hello(r, message):
    r.sendlineafter(b') ', message)

# The flag filename is "flag.txt"

if __name__ == '__main__':
    r = get_remote()

    # TODO: Exploit !
    hello(r, 'johndoe')

    r.interactive()

#!/usr/bin/python3

from pwn import *

"""
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
"""

elf = ELF('./vault')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

if __name__ == '__main__':
    r = get_remote()

    guess = b'maybe this will open the vault'

    r.sendlineafter(b'? ', str(len(guess)).encode())
    r.sendafter(b': ', guess)

    r.interactive()

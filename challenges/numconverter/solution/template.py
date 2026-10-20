#!/usr/bin/python3

from pwn import *

"""
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
"""

elf = ELF('./numconverter')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

DECIMAL = 0
HEXADECIMAL = 1
OCTAL = 2

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

buf_addr = elf.sym['buf']
formatters_addr = elf.sym['formatters']
win_addr = elf.sym['win']

if __name__ == '__main__':
    r = get_remote()

    # TODO: Exploit !

    # Input formatter
    r.sendlineafter(b'> ', str(DECIMAL).encode())

    # Input number
    r.sendlineafter(b': ', str(0xdeadbeef).encode())
    
    # Output formatter
    r.sendlineafter(b'> ', str(HEXADECIMAL).encode())

    r.interactive()

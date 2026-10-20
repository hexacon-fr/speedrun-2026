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

elf = ELF('./checksum')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

def write_data(r, data):
    r.sendlineafter(b'> ', b'1')
    r.sendafter(b'Enter data: ', data)

def compute_sha1(r, length):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'Length: ', str(length).encode())
    r.recvuntil(b'SHA-1: ')
    return r.recvline().strip().decode()

if __name__ == '__main__':
    r = get_remote()

    # TODO: Exploit !

    r.interactive()

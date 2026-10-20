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
elf = ELF('./echo_chamber')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

def say(r, msg):
    r.sendlineafter(b'Say something (max 255 bytes):\n', msg)
    return r.recvline()

if __name__ == '__main__':
    r = get_remote()

    # TODO: Exploit !

    r.interactive()

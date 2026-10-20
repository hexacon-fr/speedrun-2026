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

elf = ELF('./tensorflaw')

REMOTE = True

context.arch = 'amd64'
context.log_level = 'debug'

def get_remote():
    return remote('localhost', 1337) if REMOTE else elf.process()

def load(r, rows, cols):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'Rows: ', str(rows).encode())
    r.sendlineafter(b'Cols: ', str(cols).encode())

def upload(r, weights):
    # weights: list of str, example: ['0.5', '1', '-2'] (append 'x' to stop early)
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'Weights: ', ' '.join(weights).encode())

def gpu_status(r):
    r.sendlineafter(b'> ', b'3')

# Float helpers

def f32(dword):
    return str(struct.unpack('<f', p32(dword))[0])

def f64(value):
    return [f32(value & 0xffffffff), f32(value >> 32)]

if __name__ == '__main__':
    r = get_remote()

    # TODO: Exploit !

    r.interactive()

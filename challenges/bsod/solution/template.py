#!/usr/bin/python3
from pwn import *

REMOTE = True

def get_remote():
    return remote('localhost', 1337) if REMOTE else process('./bsod')

if __name__ == '__main__':
    r = get_remote()

    r.sendlineafter(b'CD Key: ', b'XXXXX-OEM-XXXXXXX-XXXXX')
    r.interactive()

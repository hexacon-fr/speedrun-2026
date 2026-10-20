#!/usr/bin/env python3
import socket
import sys

# Sample program
# Create your own to get the flag !
PROGRAM = bytes.fromhex(
    "0b000b100b200b300b400b500b600b700b800b900ba00bb00bc00bd00be00bf0"
)

def send(program):
    payload = len(program).to_bytes(2, "big") + program
    with socket.create_connection(('localhost', 1337), timeout=10) as s:
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    return data

def main():
    report = send(PROGRAM)
    sys.stdout.write(report.decode("latin-1"))


if __name__ == "__main__":
    main()

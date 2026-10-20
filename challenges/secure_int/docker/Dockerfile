FROM debian:bookworm

RUN apt update && apt install -y socat python3-pip python3-pwntools python3-pycryptodome
RUN pip3 install --break pycryptodome
RUN useradd -m -s /bin/bash user
WORKDIR /home/user

COPY --chmod=755 src/chall.py .
COPY docker/flag.txt .

USER user

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'/home/user/chall.py'"]

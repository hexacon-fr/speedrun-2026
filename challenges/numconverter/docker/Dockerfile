FROM ubuntu:24.04

RUN apt-get update && apt-get install -y socat 

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

COPY --chmod=755 numconverter .
COPY flag.txt .

USER user

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/user/numconverter"]

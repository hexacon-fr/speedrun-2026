FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

COPY --chmod=755 bsod .
COPY --chmod=444 flag.txt .

USER user
EXPOSE 1337

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/user/bsod"]

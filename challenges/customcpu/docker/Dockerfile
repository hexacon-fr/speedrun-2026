FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

COPY --chmod=755 cpu.py .
COPY flag.txt .

USER user
EXPOSE 1337
ENV PORT=1337

# cpu.py is its own threaded TCP server (no socat needed).
ENTRYPOINT ["python3", "/home/user/cpu.py"]

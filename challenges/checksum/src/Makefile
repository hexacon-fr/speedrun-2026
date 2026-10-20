CC=gcc
CFLAGS=-Wall -Wextra -O0 -fno-stack-protector -no-pie
LDFLAGS=-lcrypto
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/checksum

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/challenge.o: challenge.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/checksum: $(OBJ_PATH)/challenge.o
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

CC=gcc
CFLAGS=-Wall -Wextra -fno-stack-protector -no-pie
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/bsod

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/main.o: main.c logo.h
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/bsod: $(OBJ_PATH)/main.o
	$(CC) $(CFLAGS) -o $@ $<
	strip --strip-all $@

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

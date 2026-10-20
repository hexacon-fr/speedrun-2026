CC=gcc
CFLAGS=-Wall -Wextra -fno-stack-protector -no-pie
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/babypf

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/challenge.o: challenge.c filter.h
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/babypf: $(OBJ_PATH)/challenge.o
	$(CC) $(CFLAGS) -o $@ $<
	strip --strip-all $@

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

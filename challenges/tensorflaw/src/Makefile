CC=gcc
CFLAGS=-Wall -Wextra -O0 -fstack-protector-strong -no-pie -Wl,-z,lazy
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/tensorflaw

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/challenge.o: challenge.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/tensorflaw: $(OBJ_PATH)/challenge.o
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

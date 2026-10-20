CC=gcc
CFLAGS=-Wall -Wextra -fno-stack-protector -no-pie
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/unchained

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/challenge.o: challenge.c flag.h
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJ_PATH)/gadgets.o: gadgets.S
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/unchained: $(OBJ_PATH)/challenge.o $(OBJ_PATH)/gadgets.o
	$(CC) $(CFLAGS) -o $@ $^
	strip --strip-all $@

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

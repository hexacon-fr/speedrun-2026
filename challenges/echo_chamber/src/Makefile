CC=gcc
CFLAGS=-Wall -Wextra -O0 -fno-stack-protector -Wno-format-security
LDFLAGS=-no-pie
BIN_PATH := bin
OBJ_PATH := obj

.PHONY: all clean makedir

all: makedir $(BIN_PATH)/echo_chamber

makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH)

$(OBJ_PATH)/challenge.o: challenge.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/echo_chamber: $(OBJ_PATH)/challenge.o
	$(CC) -o $@ $< $(LDFLAGS)

clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

CC=gcc
DEPS=
OBJ=challenge.o
BIN=numconverter
CFLAGS=-Wno-nonnull -fno-stack-protector
LDFLAGS=-no-pie

BIN_PATH := bin
OBJ_PATH := obj

.PHONY: default
default: all

.PHONY: all
all: makedir $(BIN_PATH)/$(BIN)

.PHONY: clean
clean:
	rm -rf $(OBJ_PATH) $(BIN_PATH)

.PHONY: makedir
makedir:
	@mkdir -p $(BIN_PATH)
	@mkdir -p $(OBJ_PATH)

$(OBJ_PATH)/%.o: %.c $(DEPS)
	echo $@ $<
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN_PATH)/$(BIN): $(addprefix $(OBJ_PATH)/,$(OBJ))
	$(CC) -o $@ $^ $(LDFLAGS)

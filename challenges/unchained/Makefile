CHALLENGE := unchained
SRC_PATH := src
BIN_PATH := $(SRC_PATH)/bin

.PHONY: default all clean

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	@mkdir -p $(SRC_PATH)/obj
	make -C src/
	cp $(BIN_PATH)/$(CHALLENGE) dist/
	cp solution/template.py dist/solve.py
	make -C src/ clean

clean:
	rm -rf dist/
	make -C src/ clean

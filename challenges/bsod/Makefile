CHALLENGE := bsod
SRC_PATH  := src
BIN_PATH  := $(SRC_PATH)/bin

.PHONY: default all clean test

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	@mkdir -p $(SRC_PATH)/obj
	make -C $(SRC_PATH)/
	cp $(BIN_PATH)/$(CHALLENGE) dist/
	cp $(BIN_PATH)/$(CHALLENGE) docker/
	cp solution/template.py dist/solve.py
	make -C $(SRC_PATH)/ clean

clean:
	rm -rf dist/
	rm -f docker/$(CHALLENGE)
	make -C $(SRC_PATH)/ clean

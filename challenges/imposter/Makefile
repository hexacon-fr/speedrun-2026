CHALLENGE := imposter
SRC_PATH  := src
BIN_PATH  := $(SRC_PATH)/bin

.PHONY: default all clean

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	@mkdir -p $(SRC_PATH)/obj
	make -C $(SRC_PATH)/
	cp $(BIN_PATH)/$(CHALLENGE) dist/
	cp solution/template.py dist/solve.py
	make -C $(SRC_PATH)/ clean

clean:
	rm -rf dist/
	make -C $(SRC_PATH)/ clean

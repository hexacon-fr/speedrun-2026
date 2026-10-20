CHALLENGE := echo_chamber
SRC_PATH := src
BIN_PATH := $(SRC_PATH)/bin

.PHONY: default all clean

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	cp -r src/ dist/
	@mkdir -p $(SRC_PATH)/obj
	make -C src/
	cp $(BIN_PATH)/$(CHALLENGE) docker/
	cp $(BIN_PATH)/$(CHALLENGE) docker/Dockerfile dist/
	cp solution/template.py dist/exploit.py
	make -C src/ clean

clean:
	rm -f docker/$(CHALLENGE)
	rm -rf dist/
	make -C src/ clean

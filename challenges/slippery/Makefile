CHALLENGE := slippery
SRC_PATH  := src

.PHONY: default all clean

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	cp $(SRC_PATH)/index.php docker/
	cp $(SRC_PATH)/index.php dist/
	cp $(SRC_PATH)/flag.txt dist/flag.txt
	cp docker/Dockerfile dist/
	cp solution/template.py dist/exploit.py

clean:
	rm -f docker/index.php
	rm -rf dist/

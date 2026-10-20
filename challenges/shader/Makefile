CHALLENGE := shader
SRC_PATH  := src

.PHONY: default all clean

default: all

all: clean $(CHALLENGE)

$(CHALLENGE):
	@mkdir -p dist
	cp src/index.html dist/index.html
	cp src/open.sh dist/open.sh

clean:
	rm -rf dist/

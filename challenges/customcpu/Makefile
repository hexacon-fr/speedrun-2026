CHALLENGE := customcpu

.PHONY: default
default: all

.PHONY: all
all: clean
	@mkdir -p dist
	@cp solution/template.py dist/client.py
	@cp README-dist.md dist/README.md
	@cp src/cpu.py docker/cpu.py

.PHONY: clean
clean:
	@rm -rf dist
	@rm -f docker/cpu.py

# Everything runs in the cad container (docker-compose.yml).
export UID := $(shell id -u)
export GID := $(shell id -g)
CAD := docker compose run --rm -T cad

.PHONY: model clean

# STEP files for each part and the assembly, plus SVG views, in build/.
model:
	mkdir -p build
	$(CAD) python jig.py

clean:
	rm -rf build

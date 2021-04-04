SERVICE=app

.PHONY: build
build:
	docker-compose build
	docker-compose up -d $(SERVICE)
	# for install the package locally
	docker-compose exec $(SERVICE) poetry install

# Docker commands
.PHONY: dcb
dcb:
	docker-compose build

.PHONY: dcu
dcu:
	docker-compose up -d $(SERVICE)

.PHONY: dcd
dcd:
	docker-compose down

.PHONY: dce
dce:
	docker-compose exec $(SERVICE) /bin/bash

# in Docker container
.PHONY: test
test:
	pytest -v tests
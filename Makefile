SERVICE=app

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
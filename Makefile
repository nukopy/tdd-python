SERVICE="app"

# Docker commands
.PHONY: dcb
dcb:
	docker-compose build

.PHONY: dce
dcb:
	docker-compose exec $(SERVICE) /bin/bash

.PHONY: dcu
dcu:
	docker-compose up $(SERVICE) -d


.PHONY: dcd
dcd:
	docker-compose down

# in Docker container
.PHONY: test
test:
	pytest -v tests
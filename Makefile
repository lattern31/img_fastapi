.PHONY: up
up:
	docker-compose -f docker-compose.yaml up -d

.PHONY: down
down:
	docker-compose -f docker-compose.yaml down 

.PHONY: logs
logs: 
	docker-compose -f docker-compose.yaml logs -f

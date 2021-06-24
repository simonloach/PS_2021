.PHONY: up down server client
up:
	@docker compose build
	@docker compose up -d

down:
	@docker compose down

server:
	@docker attach ps_2021_server_cont_1

client:
	@docker attach ps_2021_client_cont_1

demo:
	@docker compose -f docker-compose-demo.yml build
	@docker compose -f docker-compose-demo.yml up
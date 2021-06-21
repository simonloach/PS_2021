.PHONY: up down server client
up:
	@docker compose build
	@docker compose up

down:
	@docker compose down

server:
	@docker attach ps_2021_server_cont_1

client:
	@docker attach ps_2021_client_cont_1
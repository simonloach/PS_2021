.PHONY: up
up:
	@docker compose build
	@docker compose up -d
.PHONY: down
down:
	@docker compose down
.PHONY: attach_serv
attach_serv:
	@docker attach ps_2021_server_cont_1
.PHONY: attach_cli
attach_cli:
	@docker attach ps_2021_client_cont_1
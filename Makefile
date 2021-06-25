.PHONY: up down server client demo demo-down
up:
	@docker-compose build
	@docker-compose up -d

debug:
	@docker-compose build
	@docker-compose up

down:
	@docker-compose down --rmi all

server:
	@docker attach ps_2021_server_cont_1

client:
	@docker attach ps_2021_client_cont_1

demo:
	@docker-compose -f docker-compose-demo.yml build
	@docker-compose -f docker-compose-demo.yml up

demo-down:
	@docker-compose -f docker-compose-demo.yml down
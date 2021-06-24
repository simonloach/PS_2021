# Tic Tac Toe Game Documentation


## Project Design Assumtions

The whole project consists of two applications:
- Client 
- Server
  
That are meant to work together to provide a way to play Tic Tac Toe over the Internet using sockets using the socket library in Python.

## Setting the Demo up
Demo can be fired of using Docker Engine. 
### Need to have:
- ```docker``` installed
- ```git``` installed
- ```make``` (optional but really useful)

### Steps if you have ```make```
- `git clone https://github.com/simonloach/PS_2021.git`
- `make demo`

That builds and runs a total of 11 docker containers(1 server and 10 clients) that work over docker instantiated network defined in `docker-compose.yml` basing on [server/Dockerfile](server/Dockerfile) and [client/Dockerfile](client/Dockerfile). 

Entrypoint scripts are [server.py](server/server.py) and [client.py](client/client.py)

Clients will run with option to randomize moves `(x,y)` and sort of play on its own.

All will be viewed from the scope of `docker compose up` command and each instance of container is distinguishable by color of the `stdout`.

# Documentation

## Client
Client is an application that functions as combination of user interface and endpoint translator of users inputs and Server messages. All user's inputs are being translated into our Communication Protocol described more throughly in protocol.md.

## Server 
Server is an application that functions as a deamon. It allows users to connect to it and provides backend for each instance of Client to connect to. Server then handles fiding oponent for the Client initiates an instance of a Game between two Clients that become Player at this stage. Game session is being handled by server until one of the Players wins by aligning three.

## Game rules
- Game is being played on a grid of 3x3 size
- Each player is either 'O' or 'X'
- 'O' starts
- Player put their marks on empty tiles of the grid taking turns
- The first player to put 3 consecutive marks that line up(horizontaly or verticaly or diagonaly) wins

## Technical documentation
#TODO
import sys
import socket
import time
import threading
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
class Server:
    def __init__(self):
        self.players = list()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', 2137))
        except socket.error:
            logging.info('Failed')
            sys.exit()

        self.socket.listen(5)
        logging.info('Listening')


    def connect(self, client_socket):
        try:
            self.players.append(client_socket)
            logging.info("Sending")
            client_socket.send(b"You have been queued for a game. Waiting for oponents.")
            logging.info("Sent")
            while True:
                if len(self.players)>1:
                    #TODO game creation
                    logging.info("Starting game")
                else:
                    logging.info("Before sleep")
                    time.sleep(0.5)
                    logging.info(".")
        except Exception as e:
            logging.info(e)



    def accept(self):
        clientSocket, addr = self.socket.accept()
        logging.info('Accepted')
        t=threading.Thread(target=Server.connect, args=(self, clientSocket))
        t.start()
        logging.info('Threaded')


x=Server()
while True:
    logging.info('Accept')
    x.accept()

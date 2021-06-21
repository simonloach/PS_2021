import os
print(os.listdir())
print(os.path)
import sys
import socket

class Server:
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', 2137))
        except socket.error:
            print('Failed')
            sys.exit()

        self.socket.listen(5)
        print('Listening')

x=Server()
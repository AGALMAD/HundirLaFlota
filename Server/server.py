import socket, threading
import Objets.ship, Objets.board


host = '127.0.0.1'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
server.bind((host, port)) #binding host and port to socket

server.listen()


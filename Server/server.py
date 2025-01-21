import socket, threading
import Objets.ship, Objets.board


host = '172.31.22.104'
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
server.bind((host, port)) #binding host and port to socket

server.listen()


server.listen()
clients = []
games = []

def init_game (client) :

    while True:
        mesagge = client.recv(1024)

        ships = mesagge.decode('utf-8')



def shot():
    while not gam:
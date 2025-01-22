import socket, threading

from Objets.user import User

host = ''
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization

server.bind((host, port)) #binding host and port to socket

server.listen()

players = []
shot_player1 = True

def init_game (client) :

    while True:
        mesagge = client.recv(1024)

        ships = mesagge.decode('utf-8')



def game_play(game) :
    while not game.end:
        try:
            mesagge = client.recv(1024)
            print(mesagge.decode('utf-8'))
        except:

            break


def receive():
    if len(players) < 2 :
        while True:
            if len(players) < 1:
                client, address = server.accept()
                print("Connected with {}".format(str(address)))
                client.send('NICKNAME'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')

                user = User(nickname, client)
                players.append(user)

                client.send('Esperando a otro jugador'.encode('ascii'))

            else:
                client, address = server.accept()
                print("Connected with {}".format(str(address)))
                client.send('NICKNAME'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')

                user = User(nickname, client)
                players.append(user)

                client.send('Empieza la partida'.encode('ascii'))




receive()

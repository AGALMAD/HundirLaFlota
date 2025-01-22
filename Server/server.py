import socket, threading

from Objets.game import Game
from Objets.user import User

host = ''
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization

server.bind((host, port)) #binding host and port to socket

server.listen()

players = []

def init_game (client) :

    while True:
        mesagge = client.recv(1024)

        ships = mesagge.decode('utf-8')



def game_play(game) :

    shot_player1 = True

    while not game.end:
        try:
            if shot_player1 :
                game.player1.client.send('SHOT'.encode('ascii'))
                shot = game.player1.recv(1024)
                print(shot.decode('utf-8'))
                game.player1.client.send('Esperando al jugador 2'.encode('ascii'))
                shot_player1 = False
            else:
                game.player2.client.send('SHOT'.encode('ascii'))
                shot = game.player2.recv(1024)
                print(shot.decode('utf-8'))
                game.player2.client.send('Esperando al jugador 1'.encode('ascii'))
                shot_player1 = True
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

                for player in players :
                    player.client.send('Empieza la partida'.encode('ascii'))

                game = Game(players[0],players[1])

                thread = threading.Thread(target=game_play, args=(game,))
                thread.start()




receive()

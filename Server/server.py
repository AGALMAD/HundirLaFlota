import json
import socket, threading

from Objets.game import Game
from Objets.user import User

host = ''
port = 7976

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization

server.bind((host, port))  # binding host and port to socket

server.listen()

game = Game()

def init_game(client):
    while True:
        mesagge = client.recv(1024)

        ships = mesagge.decode('utf-8')



def send_message(client, message_dic):
    """ Convierte el mensaje en JSON y lo envía al cliente. """
    message_json = json.dumps(message_dic)  # Convierte el diccionario a JSON
    client.send(message_json.encode('utf-8'))

def receive_message(client):
    try:
        message_json = client.recv(1024).decode('utf-8')
        return json.loads(message_json)  # Convierte a diccionario
    except:
        return None

def game_play():

    global game
    shot_player1 = True

    while not game.end:
        #Si estan los dos jugadores, empieza la partida
        if game.player1 and game.player2:
            try:
                if shot_player1:
                    # Pide el disparo al jugador 1
                    game.player1.client.send('SHOT'.encode('ascii'))
                    message_to_send["TYPE"] = "SHOT"
                    # El jugador 2 espera a recibir el disparo
                    message_to_send.message = "Esperando al disparo del jugador 2"
                    game.player2.client.send(message_to_send.encode('ascii'))

                    shot = game.player1.client.recv(1024)
                    print(shot.decode('utf-8'))
                    shot_player1 = False
                else:
                    # Pide el disparo al jugador 2
                    game.player2.client.send('SHOT'.encode('ascii'))
                    # El jugador 1 espera a recibir el disparo
                    game.player1.client.send('Esperando al disparo del jugador 1'.encode('ascii'))

                    shot = game.player2.client.recv(1024)
                    print(shot.decode('utf-8'))
                    shot_player1 = True
            except Exception as e:
                print(e)
                break


def start():
    while True:
        if not game.player1:
            #Conexión con el cliente
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            message_to_send = {"TYPE":"NICKNAME"}
            send_message(client,message_to_send)

            nickname = client.recv(1024).decode('ascii')

            # Añade el usuario a la partida
            game.player1 = User(nickname, client)

            # Hilo del jugador 1
            thread = threading.Thread(target=game_play, args=())
            thread.start()

            client.send('Esperando a otro jugador'.encode('ascii'))

        else:
            #Conexión con el cliente
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            message_to_send = {"TYPE": "NICKNAME"}
            send_message(client, message_to_send)

            nickname = client.recv(1024).decode('ascii')

            # Añade el usuario a la partida
            game.player2 = User(nickname, client)

            #Mensaje de comienzo de partida
            message_to_send = {"TYPE": "MESSAGE", "MESSAGE": "Empieza la partida"}
            send_message(game.player1.client, message_to_send)
            send_message(game.player2.client, message_to_send)

            # Hilo del jugador 2
            thread = threading.Thread(target=game_play, args=())
            thread.start()


start()

import json
import socket, threading

from Objets.board import Board
from Objets.game import Game
from Objets.position import Position
from Objets.ship import Ship
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
    message_json = json.dumps(message_dic)  # Convierte el diccionario a JSON
    client.send(message_json.encode('utf-8'))

def receive_message(client):
    try:
        message_json = client.recv(1024).decode('utf-8')
        return json.loads(message_json)  # Convierte a diccionario
    except:
        return None



def game_play():
    shot_player1 = True

    while not game.end:
        try:
            current_player = game.player1 if shot_player1 else game.player2
            opponent = game.player2 if shot_player1 else game.player1

            send_message(current_player.client, {"TYPE": "SHOT"})
            send_message(opponent.client, {"TYPE": "MESSAGE", "MESSAGE": "Esperando al oponente."})

            shot = receive_message(current_player.client)
            if shot:
                result = opponent.board.register_shot(Position(shot["x"], shot["y"]))
                send_message(current_player.client, {"TYPE": "RESULT", "MESSAGE": result})

                # Revisar fin del juego
                if opponent.board.lose():
                    send_message(current_player.client, {"TYPE": "MESSAGE", "MESSAGE": "¡Ganaste!"})
                    send_message(opponent.client, {"TYPE": "MESSAGE", "MESSAGE": "¡Perdiste!"})
                    game.end = True
                    break

            shot_player1 = not shot_player1

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
            thread = threading.Thread(target=init_board, args=(game.player1))
            thread.start()

            message_to_send = {"TYPE": "MESSAGE", "MESSAGE": "Esperando a otro jugador"}
            send_message(game.player1.client, message_to_send)

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
            thread = threading.Thread(target=init_board, args=(game.player2))
            thread.start()


def init_board(user):
    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "INICIALIZA TU TABLERO"})

    ships = []
    ship_sizes = [5, 4, 3, 3, 2]
    occupied_positions = set()  # Para evitar solapamientos

    for size in ship_sizes:
        ship_positions = []

        send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": f"Coloca tu barco de {size} posiciones."})

        while len(ship_positions) < size:
            send_message(user.client, {"TYPE": "ENTER_SHIP_POSITION", "MESSAGE": f"Posición {len(ship_positions) + 1}: "})

            ship_json = receive_message(user.client)

            if ship_json and "x" in ship_json and "y" in ship_json:
                position = Position(ship_json["x"], ship_json["y"])

                if position in occupied_positions:
                    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Posición ya ocupada."})
                    continue
                if not (0 <= position.x < 10 and 0 <= position.y < 10):
                    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Posición fuera de rango."})
                    continue

                ship_positions.append(position)

            else:
                send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Error en la posición, inténtalo de nuevo."})

        # Validar barco completo
        if not correct_ship(ship_positions):
            send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Barco inválido, colócalo recto."})
            return init_board(user)

        # Agregar barco
        ship = Ship(ship_positions)
        ships.append(ship)
        occupied_positions.update(ship_positions)

    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Tablero configurado correctamente."})
    user.board = Board(ships)

    # Iniciar el juego si los tableros están listos
    if game.player1.board and game.player2.board:
        game_play()



#Comprueba que el barco esté recto
def correct_ship(ship):





    return False


start()

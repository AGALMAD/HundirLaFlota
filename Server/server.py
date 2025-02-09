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
    message_json = json.dumps(message_dic)  + "\n"  #Agrega un salto de linea para poder mandar mensajes consecutivos al cliente
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
            # Conexión con el cliente
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            message_to_send = {"TYPE": "NICKNAME"}
            send_message(client, message_to_send)

            nickname = client.recv(1024).decode('ascii')

            # Añade el usuario a la partida
            game.player1 = User(nickname, client)

            message_to_send = {"TYPE": "MESSAGE", "MESSAGE": "Esperando a otro jugador"}
            send_message(game.player1.client, message_to_send)

        else:
            # Conexión con el cliente
            client, address = server.accept()
            print("Connected with {}".format(str(address)))

            message_to_send = {"TYPE": "NICKNAME"}
            send_message(client, message_to_send)

            nickname = client.recv(1024).decode('ascii')

            # Añade el usuario a la partida
            game.player2 = User(nickname, client)

            # Mensaje de comienzo de partida
            message_to_send = {"TYPE": "MESSAGE", "MESSAGE": "Empieza la partida"}
            send_message(game.player1.client, message_to_send)
            send_message(game.player2.client, message_to_send)


            #Cuando se conectan los dos jugadores pide los barcos

            # Hilo del jugador 1
            thread = threading.Thread(target=init_board, args=(game.player1,))
            thread.start()

            # Hilo del jugador 2
            thread = threading.Thread(target=init_board, args=(game.player2,))
            thread.start()


def init_board(user):
    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "INICIALIZA TU TABLERO"})

    ships = []
    ship_sizes = [5, 4, 3, 3, 2]
    occupied_positions = []  # Para no poder poner 2 barcos en las mismas posiciones

    for size in ship_sizes:

        while True:  # Se repite hasta que el barco se coloca bien
            ship_positions = []
            send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": f"Coloca tu barco de {size} posiciones."})

            #Pide cada posición del barco
            while len(ship_positions) < size:
                send_message(user.client, {"TYPE": "ENTER_SHIP_POSITION", "MESSAGE": f"Posición {len(ship_positions) + 1}: "})

                ship_json = receive_message(user.client)

                # Verifica que la posición no esté ocupada y que no se salga del tablero
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


            # Valida barco completo
            if not correct_ship(ship_positions):
                send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Barco inválido, debe estar en línea recta y sin espacios."})
                continue  # Reintenta colocar el barco

            # Agrega el barco a la lista y termina el bucle para pedir el siguiente
            ships.append(Ship(ship_positions))
            occupied_positions.append(ship_positions)
            break

    # Inicia el juego si los tableros están listos
    if game.player1.board and game.player2.board:
        game_play()


# Verifica si un barco está en línea recta y sin huecos
def correct_ship(ship_positions):
    x_coords = sorted([pos.x for pos in ship_positions])
    y_coords = sorted([pos.y for pos in ship_positions])

    return (
        len(set(x_coords)) == 1 and y_coords == list(range(min(y_coords), max(y_coords) + 1))  # Horizontal
        or
        len(set(y_coords)) == 1 and x_coords == list(range(min(x_coords), max(x_coords) + 1))  # Vertical
    )


start()

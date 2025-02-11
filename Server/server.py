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



#Funcion para poder enviar mensajes en formato json
def send_message(client, message_dic):
    message_json = json.dumps(message_dic)  + "\n"  #Agrega un salto de linea para poder mandar mensajes consecutivos al cliente
    client.send(message_json.encode('utf-8'))

#Funcion para poder recibir mensajes en formato json y pasarlos a diccionario
def receive_message(client):
    try:
        message_json = client.recv(1024).decode('utf-8')
        return json.loads(message_json)  # Convierte a diccionario
    except:
        return None


#Función que espera la conexicón de 2 clientes
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
            game.player1 = User(nickname, client, Board())

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
            game.player2 = User(nickname, client, Board())

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


def game_play():
    shot_player1 = True

    while not game.end:
        try:
            #Jugador que le toca disparar y oponente
            current_player = game.player1 if shot_player1 else game.player2
            opponent = game.player2 if shot_player1 else game.player1

            #Mensaje al jugador para que dispare
            send_message(current_player.client, {"TYPE": "SHOT","MESSAGE": "Dispara : "})
            send_message(opponent.client, {"TYPE": "MESSAGE", "MESSAGE": "Esperando al disparo del oponente."})

            shot = receive_message(current_player.client)
            if shot:
                result = opponent.board.shot(Position(shot["x"], shot["y"]))

                #Mando un mensaje al cliente para saber si lo ha tocado o no
                match result:
                    case 0:
                        send_message(current_player.client, {"TYPE": "MESSAGE", "MESSAGE": "Agua"})
                    case 1:
                        send_message(current_player.client, {"TYPE": "MESSAGE", "MESSAGE": "Tocado"})
                    case 2:
                        send_message(current_player.client, {"TYPE": "MESSAGE", "MESSAGE": "Hundido"})


                # Muestra el tablero
                send_message(current_player.client,
                             {"TYPE": "MESSAGE", "MESSAGE": print_opponent_board(opponent.board)})

                # Revisar fin del juego
                if opponent.board.lose():
                    send_message(current_player.client, {"TYPE": "MESSAGE", "MESSAGE": show_trophy()})
                    send_message(opponent.client, {"TYPE": "MESSAGE", "MESSAGE": show_game_over()})
                    game.end = True
                    break

            shot_player1 = not shot_player1



        except Exception as e:
            print(e)
            break



def init_board(user):
    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "INICIALIZA TU TABLERO"})
    send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": print_ships(user.board)})

    ships = []
    #ship_sizes = [5,4,3, 3, 2]
    ship_sizes = [2]

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
                    if not (0 <= position.x < 9 and 0 <= position.y < 9):
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
            user.board.ships = ships
            send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": print_ships(user.board)})
            occupied_positions.extend(ship_positions)
            break

    # Inicia el juego si los tableros están listos
    if game.player1.board.ships and game.player2.board.ships:
        game_play()
    else:
        send_message(user.client, {"TYPE": "MESSAGE", "MESSAGE": "Esperando a que el enemigo posicione sus barcos"})


# Verifica si un barco está en línea recta y sin huecos
def correct_ship(ship_positions):
    x_coords = sorted([pos.x for pos in ship_positions])
    y_coords = sorted([pos.y for pos in ship_positions])

    return (
        len(set(x_coords)) == 1 and y_coords == list(range(min(y_coords), max(y_coords) + 1))  # Horizontal
        or
        len(set(y_coords)) == 1 and x_coords == list(range(min(x_coords), max(x_coords) + 1))  # Vertical
    )


#Función para que el usuario pueda ver los barcos colocados al iniciar la partida
def print_ships(board):
    header = "    " + "   ".join(str(i) for i in range(0, 10)) + "\n"

    rows = ""
    for i, letra in enumerate("ABCDEFGHIJ"):
        row = f"{letra}  "
        for j in range(10):
            #Si hay alguna posición ocupada la imprime como B
            if any(Position(i, j) in ship.positions for ship in board.ships):
                row += " B  "
            else:
                row += " .  "
        rows += row + "\n"

    return header + rows


#Función para que el usuario pueda ver las posiciones en las que ha tirado
def print_opponent_board(board):
    header = "    " + "   ".join(str(i) for i in range(0, 10)) + "\n"

    rows = ""
    for i, letra in enumerate("ABCDEFGHIJ"):
        row = f"{letra}  "
        for j in range(10):
            position = Position(i, j)
            #Si hay alguna posición tocada la muestra
            if any(position == ship_pos and ship_pos.touched for ship in board.ships for ship_pos in ship.positions):
                row += " B  "
            #Posiciones no tocadas
            elif any(position == not_touched_position for not_touched_position in board.not_touched_ships):
                row += " X  "
            #Posiciones no disparadas
            else:
                row += " .  "
        rows += row + "\n"

    return header + rows


def show_trophy():
    return """
           ___________
          '._==_==_=_.'
          .-\\:      /-.
         | (|:.     |) |
          '-|:.     |-'
            \\::.    /
             '::. .'
               ) (
             _.' '._
            `"""""""`
    """

def show_game_over():
    return """
      _____                         ____                 
     / ____|                       / __ \\                
    | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
    | | |_ |/ _` | '_ ` _ \\ / _ \\ | |  | \\ \\ / / _ \\ '__|
    | |__| | (_| | | | | | |  __/ | |__| |\\ V /  __/ |   
     \\_____|\\__,_|_| |_| |_|\\___|  \\____/  \\_/ \\___|_|   
    """



start()

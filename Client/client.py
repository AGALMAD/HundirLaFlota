import json
import socket, threading

import board, ship

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(( '192.168.1.83' , 7976 )) #connecting client to server

ships = []


def initBoards () :
        #Pide barco 1
        print("Enter Ship 1 :")
        positions = []
        for i in range(5):
            position = input("Enter position #" + str(i + 1) + " : " )
            positions.append(position)
        new_ship = ship.Ship(positions)
        ships.append(new_ship)

        #Pide barco 2
        print("Enter Ship 2 :")
        positions = []
        for i in range(4):
            position = input("Enter position #" + str(i + 1) + " : " )
            positions.append(position)
        new_ship = ship.Ship(positions)
        ships.append(new_ship)

        #Pide barcos 3 y 4
        for i in range(2):
            positions = []
            print("Enter Ship #" + str(i + 3) + " : " )
            for j in range(3):
                position = input("Enter position #" + str(j + 1) + " : ")
                positions.append(position)
            new_ship = ship.Ship(positions)
            ships.append(new_ship)

        #Pide barcos 5
        print("Enter Ship 5 :")
        positions = []
        for i in range(2):
            position = input("Enter position #" + str(i + 1) + " : " )
            positions.append(position)

        new_ship = ship.Ship(positions)
        ships.append(new_ship)


def receive () :
    while True : #making valid connection
        try :

            message_receive = client.recv( 1024 ).decode( 'ascii' )

            message_dic = json.loads(message_receive)

            match message_dic.get("TYPE",""):
                case 'NICKNAME':
                    nickname = input("Enter nickname: ")
                    client.send(nickname.encode('ascii'))

                case'SHOT' :
                    shot = input("Dispara: ")
                    client.send(shot.encode('ascii'))
                case 'MESSAGE':
                    print(message_receive["MESSAGE"])
                case _ :
                    print(message_receive)

        except json.JSONDecodeError:
            print("Error al decodificar JSON:", message_receive)

        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break





#Hilo de escucha
receive_thread = threading.Thread(target=receive) #receiving multiple messages
receive_thread.start()


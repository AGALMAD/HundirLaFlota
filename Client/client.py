import socket, threading

import board, ship

nickname = input( "Choose your nickname: " )
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




initBoards()

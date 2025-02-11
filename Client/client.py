import json
import socket, threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(( '172.31.22.104' , 7976 )) #connecting client to server



def receive():
    buffer = ""

    while True:
        try:
            buffer += client.recv(1024).decode('ascii')

            while "\n" in buffer:  # Lee el json separado por un salto de lines
                message_json, buffer = buffer.split("\n", 1)  # Separa el JSON
                message_dic = json.loads(message_json.strip())

                type = message_dic.get("TYPE", "")

                if type == "NICKNAME":
                    nickname = input("Enter nickname: ")
                    client.send(nickname.encode('ascii'))
                elif type == "SHOT" or type == "ENTER_SHIP_POSITION":
                    # Pide posición hasta que introduce un formato correcto
                    while True:
                        position = input(message_dic.get("MESSAGE", ""))
                        try:
                            # Convierte el formato de hundir la flota (ejemplo: B1) en formato númerico para que el servidor maneje mejor los mensajes
                            x = ord(position[0].upper()) - ord('A')
                            y = int(position[1])
                            position_data = json.dumps({"TYPE": "ENTER_SHIP_POSITION", "x": x, "y": y})
                            client.send(position_data.encode('utf-8'))
                            break
                        except (ValueError, IndexError):
                            print("Formato inválido. Usa una letra y un número (ejemplo: B1).")
                elif type == 'MESSAGE':
                    print(message_dic.get("MESSAGE", ""))
                else:
                    print(message_json)

        except json.JSONDecodeError:
            print("Error al decodificar JSON:", buffer)

        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break


#Hilo de escucha
receive_thread = threading.Thread(target=receive) #receiving multiple messages
receive_thread.start()


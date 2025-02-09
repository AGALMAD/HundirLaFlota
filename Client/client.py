import json
import socket, threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(( '192.168.18.79' , 7976 )) #connecting client to server



def receive():
    buffer = ""

    while True:
        try:
            buffer += client.recv(1024).decode('ascii')

            while "\n" in buffer:  # Lee el json separado por un salto de lines
                message_json, buffer = buffer.split("\n", 1)  # Separa el JSON
                message_dic = json.loads(message_json.strip())

                #Procesa el mensaje
                match message_dic.get("TYPE", ""):
                    case 'NICKNAME':
                        nickname = input("Enter nickname: ")
                        client.send(nickname.encode('ascii'))
                    case 'ENTER_SHIP_POSITION':
                        position = input(message_dic.get("MESSAGE", ""))
                        try:
                            x = ord(position[0].upper())  # Convertir letra a número
                            y = int(position[1])
                            position_data = json.dumps({"TYPE": "ENTER_SHIP_POSITION", "x": x, "y": y})
                            client.send(position_data.encode('utf-8'))
                        except (ValueError, IndexError):
                            print("Formato inválido. Usa una letra y un número (ejemplo: B1).")
                    case 'SHOT':
                        shot = input("Dispara: ")
                        client.send(shot.encode('ascii'))
                    case 'MESSAGE':
                        print(message_dic.get("MESSAGE", ""))
                    case _:
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


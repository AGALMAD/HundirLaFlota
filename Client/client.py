import json
import socket, threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(( '192.168.1.83' , 7976 )) #connecting client to server


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
                    print(message_dic.get("MESSAGE",""))
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


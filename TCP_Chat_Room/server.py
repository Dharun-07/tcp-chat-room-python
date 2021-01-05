
import socket


import threading
#port = 55555
ok = input("What host u wanna run in?\nChoose 'local ip' for local host else enter the ip\n")
if ok == "local ip":
    host = socket.gethostbyname(socket.gethostname())
else:
    host = ok

ok_port = input("Choose a Port")
port = ok_port
port = int(port)
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server Started!")
clients = {}
def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            message = client.recv(1024)

            broadcast(message)
        except:
            # Removing And Closing Clients
            nickname = clients[client][0]
            del clients[client]
            client.close()
            broadcast('{nickname} just left :('.encode('ascii'))
            break
def receive():
    while True:
        # Accept Connection
        client_connected, address = server.accept()

        # Request And Store Nickname
        client_connected.send('NICK'.encode('ascii'))
        nickname = client_connected.recv(1024).decode('ascii')

        # Print And Broadcast Nickname
        print(f"User Connected Named {nickname}\n Address is {address} ")
        broadcast(f"{nickname}  just joined the party".encode('ascii'))
        clients[client_connected] = (nickname, address)

        client_connected.send('You are connected to the server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_connected,))
        thread.start()
receive()
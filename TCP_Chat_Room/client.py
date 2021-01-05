
import socket
import threading



#port = 55555
ok = input("What host u connect in?\n choose 'local ip' for local host else enter the ip\n")
if ok == "local ip":
    host = socket.gethostbyname(socket.gethostname())
else:
    host = ok

ok_port = input("Choose a Port\n")
port = ok_port
port = port.strip()
# Choosing Nickname
def ask_for_nick():
    nickname = input("Choose your nickname: ")
    if nickname == "" or nickname is None:
        print("Invalid Characters")
        ask_for_nick()
    else:
        return nickname
nick = ask_for_nick()


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((int(float(host)), port))
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nick.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        message = '{}: {}'.format(nick, input('Enter message'))
        client.send(message.encode('ascii'))
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
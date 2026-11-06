import socket
import threading

host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

prompt = client.recv(1024).decode('ascii')
if prompt == 'NICK':
    nickname = input('Nickname: ')
    client.sendall(nickname.encode('ascii'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            print(message)
        except:
            print("Error occured")
            client.close()
            break


def write():
    while True:
        message = input('> ')
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
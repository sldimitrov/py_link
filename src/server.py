import socket
import threading

host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def receive_line(client):
    data = bytearray()
    while True:
        byte = client.recv(1)
        if not byte:
            return None if not data else data.decode('ascii')
        if byte == b'\n':
            return data.decode('ascii')
        data.extend(byte)

def send_line(client, message):
    client.sendall(f'{message}\n'.encode('ascii'))

def broadcast(message):
    for client in clients:
        send_line(client, message)

def handle(client):
    nickname = nicknames[clients.index(client)]

    while True:
        try:
            message = receive_line(client)
            if message is None:
                break

            if message == '/quit':
                break

            broadcast(f'{nickname}: {message}')
        except OSError:
            break

    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nicknames.remove(nicknames[index])

    client.close()
    broadcast(f'{nickname} left the chat!')

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        nickname = None
        while nickname is None:
            send_line(client, 'NICK')
            received_nickname = receive_line(client)
            if received_nickname is None:
                client.close()
                break

            received_nickname = received_nickname.strip()
            if not received_nickname:
                send_line(client, 'Invalid nickname. It cannot be empty.')
                continue
            if any(existing.casefold() == received_nickname.casefold() for existing in nicknames):
                send_line(client, 'Nickname already taken. Try another one.')
                continue

            nickname = received_nickname
            send_line(client, 'OK')

        if nickname is None:
            continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!')
        send_line(client, 'Connected to the server!')

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
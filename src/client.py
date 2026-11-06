import socket
import threading

host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_line():
    data = bytearray()
    while True:
        byte = client.recv(1)
        if not byte:
            return None if not data else data.decode('ascii')
        if byte == b'\n':
            return data.decode('ascii')
        data.extend(byte)

def send_line(message):
    client.sendall(f'{message}\n'.encode('ascii'))

while True:
    prompt = receive_line()
    if prompt is None:
        print('Disconnected from the server.')
        client.close()
        raise SystemExit
    if prompt != 'NICK':
        print(f'Unexpected server response: {prompt}')
        client.close()
        raise SystemExit

    nickname = input('Nickname: ')
    send_line(nickname)
    response = receive_line()
    if response == 'OK':
        break
    if response is None:
        print('Disconnected from the server.')
        client.close()
        raise SystemExit
    print(response)

def receive():
    while True:
        try:
            message = receive_line()
            if message is None:
                print('Disconnected from the server.')
                break
            print(message)
        except OSError as error:
            print(f'Connection error: {error}')
            client.close()
            break


def write():
    while True:
        message = input('> ')
        try:
            send_line(message)
        except OSError:
            client.close()
            break
        if message == '/quit':
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
import socket
from _thread import start_new_thread

def handle_client(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            break
        print("Sending data: ", data)
        c.send(data)
    c.close()

def main():
    host = ''
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Server running on port", port)

    while True:
        c, addr = s.accept()
        print('Connected to:', addr[0], ':', addr[1])
        start_new_thread(handle_client, (c,))

if __name__ == '__main__':
    main()
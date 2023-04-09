import socket
import threading
import rsa

HEADER = 64
PORT = 5050
HOST = "localhost"
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

p = 61
q = 53
public_key, private_key = rsa.generate_key_pair(p, q)
public_key = str(public_key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print("Connected:", addr)
    conn.send(public_key.encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            plaintext = rsa.decrypt(msg, private_key)
            print(msg, '/', plaintext)
            if plaintext == DISCONNECT_MESSAGE:
                connected = False
    conn.close()
    print("Disconnected:", addr)


if __name__ == "__main__":
    print("Server is starting...")
    server.listen()
    print(f"Server is listening on host: {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

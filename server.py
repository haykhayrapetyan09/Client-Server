import socket
import threading
from copy import copy

import rsa
import rle

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

client_list = []
client_number = 0


def handle_client():
    client_number, conn, addr = client_list[-1]
    other_clients = client_list[:-1]

    print("Connected:", addr)
    first_message = 'You are client ' + str(client_number) + '. Successful connection. '
    if len(other_clients) == 0:
        first_message += " Waiting for other clients."

    send_length = str(len(str(public_key))).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(public_key.encode(FORMAT))

    send_length = str(len(first_message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(first_message.encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = rle.decode(msg)
            plaintext = rsa.decrypt(msg, private_key)
            print(msg, '/', plaintext)

            if plaintext == DISCONNECT_MESSAGE:
                connected = False
                plaintext = "disconnected from chat."

            plaintext = "Client " + str(client_number) + ": " + plaintext
            send_message(plaintext, (client_number, conn, addr))

    conn.close()
    client_list.remove((client_number, conn, addr))
    print("Disconnected:", addr)


def send_message(message, sender_details):
    ciphertext = rsa.encrypt(message, private_key)
    ciphertext = rle.encode(ciphertext)
    message = ciphertext.encode(FORMAT)

    other_clients = copy(client_list)
    other_clients.remove(sender_details)

    send_length = str(len(message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    for other_client in other_clients:
        other_conn = other_client[1]
        other_conn.send(send_length)
        other_conn.send(message)


if __name__ == "__main__":
    print("Server is starting...")
    server.listen()
    print(f"Server is listening on host: {HOST}")
    while True:
        conn, addr = server.accept()
        client_number += 1
        client_list.append((client_number, conn, addr))
        thread = threading.Thread(target=handle_client)
        thread.start()

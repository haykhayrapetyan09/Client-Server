import socket
import sys
import rsa
import rle
import threading
from ast import literal_eval as make_tuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTextEdit, QPushButton, QLineEdit

HEADER = 64
PORT = 5050
HOST = "localhost"
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
connected = True

public_key_length = client.recv(HEADER).decode(FORMAT)
if public_key_length:
    public_key = client.recv(int(public_key_length)).decode(FORMAT)
    public_key = make_tuple(public_key)

first_msg_length = client.recv(HEADER).decode(FORMAT)
if first_msg_length:
    first_message = client.recv(int(first_msg_length)).decode(FORMAT)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Messaging App')
        self.setGeometry(100, 100, 600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        grid_layout.addWidget(self.message_box, 0, 0, 1, 2)
        self.message_box.append(first_message)

        self.input_box = QLineEdit()
        grid_layout.addWidget(self.input_box, 1, 0)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        grid_layout.addWidget(self.send_button, 1, 1)

    def send_message(self):
        global connected
        message = self.input_box.text()
        self.input_box.setText('')
        if message == DISCONNECT_MESSAGE:
            connected = False
        ciphertext = rsa.encrypt(message, public_key)
        ciphertext = rle.encode(ciphertext)
        self.message_box.append("You: " + message)
        message = ciphertext.encode(FORMAT)
        send_length = str(len(message)).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def receive_message(self):
        while connected:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                msg = rle.decode(msg)
                plaintext = rsa.decrypt(msg, public_key)
                self.message_box.append(plaintext)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    thread = threading.Thread(target=window.receive_message)
    thread.start()
    sys.exit(app.exec_())

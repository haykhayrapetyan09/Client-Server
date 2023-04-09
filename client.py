import socket
import sys
import rsa
from ast import literal_eval as make_tuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTextEdit, QPushButton, QLineEdit

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
HOST = "localhost"
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
public_key = client.recv(2048).decode(FORMAT)
public_key = make_tuple(public_key)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Messaging App')
        self.setGeometry(100, 100, 600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        # Create text box to display messages
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        grid_layout.addWidget(self.message_box, 0, 0, 1, 2)

        # Create text box for user input
        self.input_box = QLineEdit()
        grid_layout.addWidget(self.input_box, 1, 0)

        # Create button to send messages
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        grid_layout.addWidget(self.send_button, 1, 1)

    def send_message(self):
        message = self.input_box.text()
        # Code to send message to other user(s)
        self.input_box.setText('')
        ciphertext = rsa.encrypt(message, public_key)
        self.message_box.append(message + " / " + ciphertext)
        message = ciphertext.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

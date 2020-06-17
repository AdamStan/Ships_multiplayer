import socket
import threading

from zadanie4.server_socket import HOST, PORT


class ClientSocket:
    def send_in_background(self, diameter):
        threading.Thread(target=lambda d: self.send(d), args=[diameter]).start()

    def send(self, diameter):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(diameter)
            print(diameter.to_bytes(4, byteorder='big'))
            s.send(diameter.to_bytes(4, byteorder='big'))
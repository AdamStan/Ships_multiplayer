
import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class ServerSocket:
    def __init__(self, circle):
        self.connected = False
        self.circle = circle

    def turn_off(self):
        self.connected = False
        self.socket.close()

    def run_in_background(self):
        self.background_thread = threading.Thread(target=lambda: self.turn_on())
        self.background_thread.daemon = True
        self.background_thread.start()

    def turn_on(self):
        self.connected = True
        while self.connected:
            print("server running")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((HOST, PORT))
            self.socket.listen()
            conn, addr = self.socket.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(data)
                        print(int.from_bytes(data, "big"))
                        self.circle.d = int.from_bytes(data, "big")
                        self.circle.update()
                        conn.sendall(data)
                    except ConnectionAbortedError:
                        break
                    except ConnectionResetError:
                        break
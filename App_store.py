import socket
import requests
import threading
import os

def start(store):
    store.start_store()

class Application:
    def __init__(self, name: str, file):
        self.name: str = name
        self.content: str = file


class ServerAppStore:
    """This is the Server App Store object documentation"""

    def __init__(self, public_ip, ip, port):
        """This is the Server App Store documentation"""

        self.IP: str = ip
        self.PUBLIC_IP: str = public_ip
        self.PORT: int = port
        self.status: str = "Online"
        self.available_apps: dict = {'main.py': 'main.py', 'test.txt': 'test.txt'}
        self.status_thread: threading.Thread = threading.Thread(target=self.status_checker)
        # self.status_thread.start()
        print(f"[STARTING] Server {self.PUBLIC_IP} started")

    def status_checker(self):
        print(threading.active_count())

        while True:
            nb_status = str(requests.get(f'http://{self.PUBLIC_IP}'))
            if nb_status == 200:
                self.status = 'Online'
                return 'Online'

            elif nb_status[0] == 4 or nb_status[0] == 5:
                self.status = 'Offline'
                return 'Offline'

            else:
                self.status = 'Unknown'
                return 'Unknown'

    def handle_client(self, address, request: bytes, port: bytes):  # Detects the request
        print(f"[REQUEST] {address} requested {request.decode('utf-8')} to be installed")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((address[0], int(port.decode('utf-8'))))  # Prepares to send the files

        if str(request.decode("utf-8")) in list(self.available_apps.keys()):
            print("[DOWNLOAD] Application downloading...")
            file = open(request.decode("utf-8"), "rb")
            file_size = os.path.getsize(request.decode("utf-8"))
            ext = os.path.splitext(request.decode("utf-8"))[-1].lower()  # Checks the extension and send it
            client.send(b't' + request)
            client.send(b'\n')
            client.send(str(file_size).encode())
            client.send(b'\n')

            data = file.read()
            client.sendall(data)
            client.send(b"|END|")

            file.close()
            client.close()

        else:
            print("j'avais raison")

    def start_store(self):
        print("[STARTING] Store will be started in a few seconds...")
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Making so it can receive a request
        socket_.bind((self.IP, self.PORT))                           # to download an app
        socket_.listen()

        print(f"[LISTENING] Now listening on {self.PORT}")

        client_socket, client_address = socket_.accept()
        print(f"[CONNECTION] {client_address} has connected")
        request = bytes()
        while b'\n' not in request:
            request += client_socket.recv(1)

        port = bytes()
        while b'\n' not in port:
            port += client_socket.recv(1)

        request = request.split(b'\n')[0]
        port = port.split(b'\n')[0]

        client_socket.close()

        self.handle_client(client_address, request, port)

        # thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, request, port))

        print("[CLOSED] Store terminated")

#

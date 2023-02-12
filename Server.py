import socket
import tqdm
import threading
import App_store
from itertools import count

class Server:
    _ids = count(0)

    def __init__(self, ip, port, app_store_, public_ip,installation_folder="/apps"):
        self.mods: list = ["Idle", "Under attack", "Attacking", "Honey Pot"]
        self.IP: str = ip
        self.PUBLIC_IP: str = public_ip
        self.PORT: int = port
        self.status: str = "online"
        self.open_ports: list = []
        self.apps: dict = {}
        self.mode: str = self.mods[0]
        self.id: int = next(self._ids)
        self.app_store: App_store.ServerAppStore = app_store_
        self.installation_folder: str = installation_folder

    def __repr__(self):
        return f"({self.IP}, {self.PORT}, {self.status}, {self.id})"

    def install_(self, app: App_store.Application, _) -> str:
        request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sending the download request to the app store server
        print(f"[CONNECTING] Attempting connection on {self.app_store.IP}:{self.app_store.PORT}")
        request_socket.connect((self.app_store.IP, self.app_store.PORT))
        print(f"[CONNECTED] Connected to {self.app_store.IP}:{self.app_store.PORT}")
        request_socket.send(app.name.encode())
        request_socket.send(b'\n')
        request_socket.send(str(self.PORT).encode())
        request_socket.send(b'\n')
        request_socket.close()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.IP, self.PORT))
        server.listen()
        print(f"[LISTENING] Now listening on {self.PORT}")
        client, address = server.accept()

        file_name = b''
        file_size = b''

        while b'\n' not in file_name:
            file_name += client.recv(1)

        while b'\n' not in file_size:
            file_size += client.recv(1)

        file_name = file_name.split(b'\n')[0]
        file_size = file_size.split(b'\n')[0]

        file_name = file_name.decode('utf-8')
        file_size = file_size.decode('utf-8')

        print(file_name)

        file = open(file_name, "wb")
        file_bytes: bytes = b""

        done: bool = False

        progress = tqdm.tqdm(unit="b", unit_scale=True, unit_divisor=1000, total=int(file_size), colour='blue')

        while not done:
            data = client.recv(1024)
            if file_bytes[-5:] == b'|END|':
                done = True

            else:
                file_bytes += data
            progress.update(1024)

        progress.close()

        while b'|END|' in file_bytes:
            file_bytes = file_bytes.split(b'|END|')[0]

        file.write(file_bytes)
        file.close()
        client.close()
        server.close()

        return f"{app.name} has been successfully installed"

    def install(self, app: App_store.Application):  # Is only used to start the threads
        thread1 = threading.Thread(target=self.install_, args=(app, None))
        thread2 = threading.Thread(target=self.app_store.start_store)

        thread2.start()
        thread1.start()

#

import socket
from saver import saver

def listen(host, port) :
    path = "data/Inbox.json"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net :
        net.bind((host, port))
        net.listen(2)
        while True :
            conn, _ = net.accept()
            with conn :
                data = conn.recv(1024)
                saver(path, data)


import socket
import json

def listen(host, port) :
    path = "data/Inbox.json"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net :
        net.bind((host, port))
        net.listen(2)
        while True :
            conn, address = net.accept()
            with conn :
                data = conn.recv(1024)
                try :
                    with open(path, "r") as file :
                        loader = json.load(file)
                        loader.append(json.loads(data.decode()))
                    with open(path, "w") as file :
                        json.dump(loader, file, indent = 4)
                except FileNotFoundError :
                    with open(path, "x") as file :
                        json.dump([], file)
                    with open(path, "r") as file :
                        loader = json.load(file)
                        loader.append(json.loads(data.decode()))
                    with open(path, "w") as file :
                        json.dump(loader, file, indent = 4)

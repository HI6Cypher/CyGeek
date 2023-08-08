import socket
import threading
import json

#handshake to response client handshake : when a client handshakes to server, the server checks unsend
#messages file and if found unsend message about the client, will send it again.

#listen to port : listening to receive new message, analyse them and prepare them to give'em to the post

#post : to forwarding messages and if post fail, message saves in unsend messages.

#saver : to save unsend messages.
class MainServer :
    def __init__(self) :
        pass

    def main(self) :
        pass

    def handshake(self) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handshake :
            handshake.bind((socket.gethostbyname(socket.gethostname()), 50321))
            handshake.listen(5)
            while True :
                _, address = handshake.accept()
                with address :
                    with open("data/unsend.json", "r") as file :
                        unsends = json.load(file)
                    for unsend in unsends :
                        if unsend["host"] == address[0] :
                            self.post(address[0], unsend, address)
                        else :
                            continue

    def listen(self) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen :
            listen.bind((socket.gethostbyname(socket.gethostname()), 40321))
            listen.listen(5)
            while True :
                conn, address = listen.accept()
                with conn :
                    data = conn.recv(1024)
                    if not data :
                        payload = "your message is not recognized".upper()
                        listen.sendto(payload, address)
                    else :
                        data = json.loads(data.decode())
                        self.post(data["host"], data, address)

    def post(self, host, payload, address) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as post :
            try :
                post.connect((host, 60321))
                post.sendall(json.dumps(payload).encode())
                delivery_report = f"[+] {address[0]} is online and received your message".encode()
                post.sendto(delivery_report, address)
            except :
                delivery_report = f"[*] {address[0]} isn't online but will receive your message".encode()
                post.sendto(delivery_report, address)
                self.saver("data/unsend.json", payload)

    def saver(self, path, data) : #TODO
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
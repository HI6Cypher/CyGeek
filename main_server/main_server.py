import socket
import threading
import json
import os

#handshake to response client handshake : when a client handshakes to server, the server checks unsend
#messages file and if found unsend message about the client, will send it again.

#listen to port : listening to receive new message, analyse them and prepare them to give'em to the post

#post : to forwarding messages and if post fail, message saves in unsend messages.

#saver : to save unsend messages.
class MainServer :
    def __init__(self) :
        self.text = """\nmainserver\n"""
        self.path_unsends = f"{os.getcwd()}/data/unsends.json"

    def main(self) :
        if not os.path.exists(self.path_unsends) :
            first = [{
                    "time": "01/01/1970--00:00:00",
                    "sender": "None",
                    "hostname": "None",
                    "host": "None",
                    "message": "MainServer"
                }]
            with open(self.path_unsends, "x") as file :
                json.dump(first, file, indent = 4)
        task_0 = threading.Thread(target = self.handshake)
        task_0.start()
        task_1 = threading.Thread(target = self.listen)
        task_1.start()
        print(self.text)
        input("Press anykey to setup the Server... ")


    def handshake(self) :
        payload = "Hi [HOST:%s:HOST][PORT:40321:PORT]" % (socket.gethostbyname(socket.gethostname()))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as handshake :
            handshake.bind((socket.gethostbyname(socket.gethostname()), 50321))
            while True :
                try :
                    conn, address = handshake.recvfrom(1024)
                    print(address)
                    handshake.sendto(payload.encode(), address)
                    with open(self.path_unsends, "r") as file :
                        unsends = json.load(file)
                    for unsend in unsends : #TODO to remove unsend message
                        if unsend["host"] == address[0] :
                            self.post(address[0], unsend, address)
                            unsends.remove(unsend)
                            with open(self.path_unsends, "w") as file :
                                json.dump(unsends, file, indent = 4)
                        else :
                            continue
                except OSError as error:
                    continue
                except Exception as error :
                    print(f"[HANDSHAKE] Error!--> {error}")
                    continue

    def listen(self) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen :
            listen.bind((socket.gethostbyname(socket.gethostname()), 40321))
            listen.listen(5)
            while True :
                try :
                    conn, address = listen.accept()
                    with conn :
                        data = conn.recv(1024)
                        if not data :
                            payload = "your message is not recognized".upper()
                            conn.send(payload)
                        else :
                            data = json.loads(data.decode("utf-8"))
                            self.post(data["host"], data, address)
                except Exception as error:
                    print(f"[LISTEN] Error!--> {error}")

    def post(self, host, payload, address) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as post :
            try :
                post.connect((host, 60321))
                post.sendall(json.dumps(payload).encode())
            except :
                pass

    def saver(self, path, data) : #TODO
        try :
            with open(path, "r") as file :
                loader = json.load(file)
                loader.append(json.loads(data))
            with open(path, "w") as file :
                json.dump(loader, file, indent = 4)
        except FileNotFoundError :
            with open(path, "x") as file :
                json.dump([], file)
            with open(path, "r") as file :
                loader = json.load(file)
                loader.append(json.loads(data))
            with open(path, "w") as file :
                json.dump(loader, file, indent = 4)

if __name__ == "__main__" :
    server = MainServer()
    server.main()
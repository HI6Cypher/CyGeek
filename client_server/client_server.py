import socket
import threading
import json
import re
import datetime


class ClientServer :
    def __init__(self) :
        self.text = "\n1.Post\n2.Inbox\n3.Sent"

    def main(self) :
        task_0 = threading.Thread(target = self.handshake)
        task_0.start()
        task_0.join()
        task_1 = threading.Thread(target = self.listen)
        task_1.start()
        while True :
            print(self.text)
            choice = input("-> ")
            if choice == "1" :
                hostname_input = input("Hostname: ")
                message_input = input("Message: ")
                task_2 = threading.Thread(target = self.post, args = (hostname_input, message_input))
                task_2.start()
                task_2.join()
            elif choice == "2" :
                counter = 1
                with open("data/Inbox.json", "r") as file :
                    for i in json.load(file) :
                        text = "[%s]\n------------\nTime: %s\nSender: %s\nHostname: %s\nHost: %s\nMessage: %s\n------------\n" \
                            % (counter, i["time"], i["sender"], i["hostname"], i["host"], i["message"])
                        counter += 1
                        print(text)

    def handshake(self) :
        server = dict()
        payload = f"Hi i am [{socket.gethostbyname(socket.gethostname())}]"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handshake :
            try :
                with open("data/server_info.json", "r") as file :
                    info = json.load(file)
            except :
                for i in range(2, 256) :
                    handshake.connect((f"192.168.43.{i}", 50321))
                    handshake.sendall(payload.encode())
                    data = handshake.recv(1024)
                    if "Hi" in data.decode() :
                        try :
                            server_host = re.search(r"(?<=HOST:).+(?=:HOST)", data.decode()).group()
                            server_port = re.search(r"(?<=PORT:).+(?=:PORT)", data.decode()).group()
                        except :
                            print("[!] security problem in network".upper())
                            break
                        else :
                            server["server_host"] = server_host
                            server["server_port"] = server_port
                            with open("data/server_info.json", "w") as file :
                                json.dump(server, file)
                    else :
                        continue
            else :
                handshake.connect((info["server_host"], int(info["server_port"])))
                handshake.sendall(payload.encode())

    def listen(self) :
        path = "data/Inbox.json"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net :
            net.bind((socket.gethostbyname(socket.gethostname()), 60321))
            net.listen(2)
            while True :
                conn, _ = net.accept()
                with conn :
                    data = conn.recv(1024)
                    self.saver(path, data)

    def post(self, hostname, message) :
        time = datetime.datetime.today()
        packet = {
                "time" : time.strftime("%m/%d/%Y--%H:%M:%S"),
                "sender" : socket.gethostbyname(socket.gethostname()),
                "hostname" : hostname,
                "host" : socket.gethostbyname(hostname),
                "message" : message
            }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net :
            try :
                with open("data/server_info.json", "r") as file :
                    info = json.load(file)
                net.connect((info["server_host"], 40321)) #TODO
                net.sendall(json.dumps(packet).encode())
            except OSError as error :
                error = " ".join(str(error).split()[2:])
                print(f"[*] Error!--> {error}")

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

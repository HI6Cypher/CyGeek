import socket
import threading
import json
import re
import os
import datetime


class ClientServer :
    def __init__(self) :
        self.text = "\n1.Post\n2.Inbox\n3.Sent"
        self.path_Inbox = f"{os.getcwd()}/data/Inbox.json"
        self.path_server_info = f"{os.getcwd()}/data/server_info.json"

    def main(self) : #TODO
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
                with open(self.path_Inbox, "r") as file :
                    for i in json.load(file) :
                        text = "[%s]\n------------\nTime: %s\nSender: %s\nHostname: %s\nHost: %s\nMessage: %s\n------------\n" \
                            % (counter, i["time"], i["sender"], i["hostname"], i["host"], i["message"])
                        counter += 1
                        print(text)

    def handshake(self) :
        server = dict()
        payload = f"Hi i am [{socket.gethostbyname(socket.gethostname())}]"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as handshake :
            handshake.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try :
                with open(self.path_server_info, "r") as file :
                    info = json.load(file)
            except :
                    try :
                        handshake.settimeout(2)
                        handshake.sendto(payload.encode(), ("255.255.255.255", 50321))
                        handshake.settimeout(10)
                        data = handshake.recvfrom(1024)
                        print(f"[*] the server found {data[1]}".upper())
                    except :
                        pass
                    else :
                        if "Hi" in data[0].decode() :
                            try :
                                server_host = re.search(r"(?<=HOST:).+(?=:HOST)", data[0].decode()).group()
                                server_port = re.search(r"(?<=PORT:).+(?=:PORT)", data[0].decode()).group()
                            except :
                                print("[!] security problem in network".upper())
                            else :
                                server["server_host"] = server_host
                                server["server_port"] = server_port
                                with open(self.path_server_info, "w") as file :
                                    json.dump([server], file)
                        else :
                            pass
            else :
                handshake.connect((info[0]["server_host"], 50321))
                handshake.sendall(payload.encode())

    def listen(self) :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen :
            listen.bind((socket.gethostbyname(socket.gethostname()), 60321))
            listen.listen(5)
            while True :
                conn, _ = listen.accept()
                with conn :
                    data = conn.recv(1024)
                    self.saver(self.path_Inbox, data)

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
                with open(self.path_server_info, "r") as file :
                    info = json.load(file)
                net.connect((info[0]["server_host"], 40321)) #TODO
                net.sendall(json.dumps(packet).encode())
            except OSError as error :
                error = " ".join(str(error).split()[2:])
                print(f"[POST] Error!--> {error}")


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

if __name__ == "__main__" :
    client = ClientServer()
    client.main()

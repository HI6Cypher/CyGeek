import socket
import json
import datetime

def post(hostname, message) :
    time = datetime.datetime.today()
    
    packet = {
            "time" : time.strftime("%m/%d/%Y--%H:%M:%S"),
            "hostname" : hostname,
            "host" : socket.gethostbyname(hostname),
            "message" : message
        }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net :
        try :
            net.connect((packet["host"], 321))
            net.sendall(json.dumps(packet).encode())
        except OSError as error :
            print(f"\n{error}\n")
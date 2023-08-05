import socket
import threading
import json
from listen import listen
from post import post

#TODO add contacts
task_1 = threading.Thread(target = listen, args = (socket.gethostbyname(socket.gethostname()), 321))
task_1.start()
while True :
    history = None
    text = "\n1.Post\n2.Inbox\n3.Contacts"
    print(text)
    choice = input("-> ")
    if choice == "1" :
        post_choice = input("Hostname: ")
        message_choice = input("Message: ")
        task_2 = threading.Thread(target = post, args = (post_choice, message_choice))
        task_2.start()
        task_2.join()
    elif choice == "2" :
        counter = 1
        with open("data/Inbox.json", "r") as file :
            for i in json.load(file) :
                text = "[%s]\n------------\nTime: %s\nHostname: %s\nHost: %s\nMessage: %s\n------------\n" \
                    % (counter, i["time"], i["hostname"], i["host"], i["message"])
                counter += 1
                print(text)
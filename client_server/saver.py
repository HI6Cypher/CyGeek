import json

def saver(path, data) : #TODO
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
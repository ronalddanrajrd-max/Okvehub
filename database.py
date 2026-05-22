import json

FILE = "data.json"

def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "brainrot": {},
            "orders": []
        }

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

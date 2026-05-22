import json
import os

FILE = "data.json"

DEFAULT = {
    "brainrot": {},
    "orders": []
}

def load():
    if not os.path.exists(FILE):
        save(DEFAULT)
        return DEFAULT

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

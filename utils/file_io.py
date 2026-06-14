import json

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)
    return True    

def load_from_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
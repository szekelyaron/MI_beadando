import json, os

FILE = "feedback.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE, "r", encoding="utf-8"))

def save_data(data):
    json.dump(data, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def update_feedback(name, liked):
    data = load_data()

    if name not in data:
        data[name] = {"positive": 0, "negative": 0, "preference": 0.5}

    if liked:
        data[name]["positive"] += 1
    else:
        data[name]["negative"] += 1

    pos = data[name]["positive"]
    neg = data[name]["negative"]
    total = pos + neg

    if total > 0:
        data[name]["preference"] = round(pos / total, 3)
    else:
        data[name]["preference"] = 0.5

    save_data(data)

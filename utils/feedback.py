import json
from pathlib import Path

FEEDBACK_FILE = Path("data/feedback.json")

def load_feedback():
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_feedback(data):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_feedback(food_name, liked):
    data = load_feedback()
    if food_name not in data:
        data[food_name] = {"positive": 0, "negative": 0}
    if liked:
        data[food_name]["positive"] += 1
    else:
        data[food_name]["negative"] += 1
    save_feedback(data)

def get_preference(food_name):
    data = load_feedback()
    if food_name not in data:
        return 0.5
    pos = data[food_name]["positive"]
    neg = data[food_name]["negative"]
    if pos + neg == 0:
        return 0.5
    return pos / (pos + neg)

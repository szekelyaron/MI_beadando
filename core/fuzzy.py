from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = BASE_DIR / "data" / "feedback.json"


def _load_feedback():
    if not FEEDBACK_FILE.exists():
        return {}
    return json.load(open(FEEDBACK_FILE, "r", encoding="utf-8"))

def _feedback_membership(food_name):
    data = _load_feedback()
    if food_name in data:
        return float(data[food_name].get("preference", 0.5))
    return 0.5

def _age_membership(age, min_age):
    if age >= min_age:
        return 1.0
    low = min_age - 3
    if age <= low:
        return 0.0
    return (age - low) / 3.0

def _texture_membership(texture, prefs, age):
    if prefs:
        if texture in prefs:
            return 1.0
        else:
            if age <= 8:
                ideal = "püré"
            elif age <= 12:
                ideal = "puha"
            else:
                ideal = "darabos"
            if texture == ideal:
                return 0.7
            else:
                return 0.4
    else:
        if age <= 8:
            ideal = "püré"
        elif age <= 12:
            ideal = "puha"
        else:
            ideal = "darabos"
        if texture == ideal:
            return 0.8
        else:
            return 0.5

def _health_membership(food_name):
    name = food_name.lower()
    score = 0.0
    if "zöldség" in name or "főzelék" in name:
        score += 0.4
    if "gyümölcs" in name or "alma" in name or "körte" in name or "banán" in name:
        score += 0.3
    if "csirke" in name or "pulyka" in name or "hal" in name or "lazac" in name:
        score += 0.3
    if "tészta" in name or "palacsinta" in name or "gombóc" in name:
        score -= 0.2
    if score < 0.0:
        score = 0.0
    if score > 1.0:
        score = 1.0
    return score

def fuzzy_score(food, age, allergies, prefs):
    if set(food["allergens"]) & set(allergies):
        return 0.0

    age_m = _age_membership(age, food["min_age"])
    texture_m = _texture_membership(food["texture"], prefs, age)
    health_m = _health_membership(food["name"])
    feedback_m = _feedback_membership(food["name"])

    total = (
        0.4 * age_m +
        0.25 * texture_m +
        0.2 * health_m +
        0.15 * feedback_m
    )

    if total < 0.0:
        total = 0.0
    if total > 1.0:
        total = 1.0

    return round(total, 2)

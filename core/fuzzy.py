def fuzzy_score(food, age, allergies, prefs):
    if set(food["allergens"]) & set(allergies):
        return 0.0

    if age >= food["min_age"]:
        age_score = 1.0
    elif age + 1 == food["min_age"]:
        age_score = 0.5
    else:
        age_score = 0.0

    texture_score = 1.0 if food["texture"] in prefs else 0.3

    total = (age_score * 0.6) + (texture_score * 0.4)

    return round(total, 2)

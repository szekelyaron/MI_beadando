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

    keywords = ["zöldség", "gyümölcs", "csirke", "püré", "hal", "főzelék"]
    type_bonus = 0.1 if any(k in food["name"].lower() for k in keywords) else 0.0

    total = (age_score * 0.6) + (texture_score * 0.3) + (type_bonus * 0.1)

    return round(total, 2)

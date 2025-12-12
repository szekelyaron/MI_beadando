from core.evolution import evolve

def recommend_day_menu(foods, age, allergies, prefs):
    score, menu = evolve(foods, age, allergies, prefs)
    return menu, score

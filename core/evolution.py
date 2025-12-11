import random
from core.fuzzy import fuzzy_score

def fitness(menu, age, allergies, prefs):
    scores = [fuzzy_score(f, age, allergies, prefs) for f in menu]
    return sum(scores) / len(scores)

def evolve(foods, age, allergies, prefs, generations=1, pop_size=10, menu_size=3):
    population = []
    for _ in range(pop_size):
        population.append(random.sample(foods, menu_size))

    scored = sorted(
        [(fitness(m, age, allergies, prefs), m) for m in population],
        key=lambda x: x[0],
        reverse=True
    )

    return scored[0]

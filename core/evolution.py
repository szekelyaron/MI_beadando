import random
from core.fuzzy import fuzzy_score

def fitness(menu, age, allergies, prefs):
    scores = [fuzzy_score(f, age, allergies, prefs) for f in menu]
    return sum(scores) / len(scores)

def evolve(foods, age, allergies, prefs, generations=12, pop_size=20, menu_size=3):
    population = []
    for _ in range(pop_size):
        population.append(random.sample(foods, menu_size))

    for _ in range(generations):
        scored = sorted(
            [(fitness(m, age, allergies, prefs), m) for m in population],
            key=lambda x: x[0],
            reverse=True
        )

        best = [m for _, m in scored[:5]]
        new_pop = best[:]

        while len(new_pop) < pop_size:
            p1, p2 = random.sample(best, 2)
            cut = random.randint(1, menu_size - 1)
            child = p1[:cut] + p2[cut:]
            child = list({f["name"]: f for f in child}.values())

            while len(child) < menu_size:
                child.append(random.choice(foods))

            if random.random() < 0.3:
                child[random.randint(0, menu_size - 1)] = random.choice(foods)

            new_pop.append(child)

        population = new_pop

    scored = sorted(
        [(fitness(m, age, allergies, prefs), m) for m in population],
        key=lambda x: x[0],
        reverse=True
    )

    return scored[0]

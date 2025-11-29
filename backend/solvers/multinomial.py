from math import factorial
from typing import List

def multinomial_prob(**params):
    # Extraer c1, c2, c3... y p1, p2, p3...
    counts = []
    probs = []

    count_keys = sorted([k for k in params if k.startswith("c")], key=lambda x: int(x[1:]))
    prob_keys = sorted([k for k in params if k.startswith("p")], key=lambda x: int(x[1:]))

    for k in count_keys:
        counts.append(int(params[k]))

    for k in prob_keys:
        probs.append(float(params[k]))

    if len(counts) != len(probs):
        raise ValueError("El número de 'c' debe coincidir con el número de 'p'")

    # Validar counts
    if any(c < 0 for c in counts):
        raise ValueError("counts deben ser >= 0")

    # Normalizar probabilidades para que sumen 1
    total_p = sum(probs)
    if total_p == 0:
        raise ValueError("La suma de probabilidades no puede ser 0")

    probs = [p / total_p for p in probs]

    # Fórmula multinomial
    n = sum(counts)

    coef = factorial(n)
    for c in counts:
        coef /= factorial(c)

    prob = 1.0
    for c, p in zip(counts, probs):
        prob *= (p ** c)

    return coef * prob
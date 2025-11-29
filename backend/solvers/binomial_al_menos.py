from math import comb

def binomial_al_menos(n: int, p: float, k: int) -> float:
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1")
    if not (0 <= k <= n):
        raise ValueError("k debe cumplir 0 <= k <= n")
    q = 1 - p
    total = 0
    for i in range(k, n + 1):
        total += comb(n, i) * (p ** i) * (q ** (n - i))
    return total
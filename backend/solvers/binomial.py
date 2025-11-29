from math import comb

def binomial_exact(n: int, p: float, x: int) -> float:
    """Calcula P(X = x) para una distribución binomial."""
    return comb(n, x) * (p ** x) * ((1 - p) ** (n - x))

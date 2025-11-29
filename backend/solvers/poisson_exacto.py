from math import exp, factorial

def poisson_exacto(lambda_: float, k: int) -> float:
    if lambda_ < 0:
        raise ValueError("lambda debe ser >= 0")
    if k < 0:
        raise ValueError("k debe ser >= 0")
    return exp(-lambda_) * (lambda_ ** k) / factorial(k)
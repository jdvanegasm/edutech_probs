from math import erf, sqrt

def normal_mayor_que(mu: float, sigma: float, limite: float) -> float:
    if sigma <= 0:
        raise ValueError("sigma debe ser > 0")
    z = (limite - mu) / sigma
    cdf = 0.5 * (1 + erf(z / sqrt(2)))
    return 1 - cdf
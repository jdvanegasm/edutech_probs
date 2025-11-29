from math import erf, sqrt
from typing import Any, Dict

def prob_bateria_entre(**params) -> float:
    """
    Calcula P(t_min <= X <= t_max) para X ~ Normal(mu, sigma)
    """

    mu = float(params.get("media_horas"))
    sigma = float(params.get("desviacion_horas"))
    t_min = float(params.get("t_min"))
    t_max = float(params.get("t_max"))

    if sigma <= 0:
        raise ValueError("desviacion_horas debe ser > 0")
    if t_min > t_max:
        raise ValueError("t_min no puede ser mayor que t_max")

    # CDF normal
    def normal_cdf(x):
        z = (x - mu) / sigma
        return 0.5 * (1 + erf(z / sqrt(2)))

    return normal_cdf(t_max) - normal_cdf(t_min)
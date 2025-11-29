from math import exp

def prob_bateria_operacion(**params) -> float:
    """
    P(T > t) = exp(-(t / alpha) ** beta)
    """

    alpha = float(params.get("alpha"))
    beta = float(params.get("beta"))
    anos = float(params.get("anos"))

    if alpha <= 0:
        raise ValueError("alpha debe ser > 0")
    if beta <= 0:
        raise ValueError("beta debe ser > 0")
    if anos < 0:
        raise ValueError("anos >= 0")

    return exp(-(anos / alpha) ** beta)
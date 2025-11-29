from math import exp

def prob_falla_antes(**params) -> float:
    """
    P(T < t) = 1 - exp(-lambda * t)
    """

    tasa = float(params.get("tasa"))
    horas = float(params.get("horas"))

    if tasa < 0:
        raise ValueError("tasa >= 0")
    if horas < 0:
        raise ValueError("horas >= 0")

    return 1 - exp(-tasa * horas)
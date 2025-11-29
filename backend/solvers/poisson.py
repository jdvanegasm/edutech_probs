from math import exp

def poisson_mas_de_un(**params) -> float:
    """
    Solver compatible con FastAPI: recibe params planos y los extrae:

    Espera:
    - n  = número de átomos
    - p  = prob de decaimiento en 1 minuto
    - t  = tiempo en minutos

    Calcula:
    P(X > 1) = 1 - e^{-λ} (1 + λ)
    con λ = n * p * t
    """

    # Obtener valores del JSON
    n = int(params.get("n"))
    p = float(params.get("p"))
    t = float(params.get("t"))

    # Validaciones
    if n < 0:
        raise ValueError("n debe ser >= 0")
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1")
    if t < 0:
        raise ValueError("t debe ser >= 0")

    # Parámetro Poisson
    lmbda = n * p * t

    # Fórmula final
    return 1 - exp(-lmbda) * (1 + lmbda)
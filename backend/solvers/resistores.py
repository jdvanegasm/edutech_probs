from typing import Dict

def media_var_resistores(**params) -> Dict[str, float]:
    """
    Calcula media y varianza de X con:
    P(X=0) = p0
    P(X=1) = p1
    P(X=2) = p2
    """

    p0 = float(params.get("p_0"))
    p1 = float(params.get("p_1"))
    p2 = float(params.get("p_2"))

    # Validaciones
    for p in (p0, p1, p2):
        if not (0 <= p <= 1):
            raise ValueError("Probabilidades deben estar entre 0 y 1")

    total = p0 + p1 + p2
    if total == 0:
        raise ValueError("Suma de probabilidades no puede ser 0")

    # Normalizamos si no suma exactamente 1
    p0 /= total
    p1 /= total
    p2 /= total

    # Media
    media = p1 * 1 + p2 * 2

    # E[X²]
    ex2 = p1 * 1 + p2 * 4

    # Varianza
    var = ex2 - media**2

    return {
        "media": media,
        "varianza": var
    }

def utilidad_maxima(tasa: float, costo: float) -> float:
    """
    Calcula la utilidad máxima U(μ) = tasa*μ - costo*μ^2.
    Retorna SOLO la utilidad máxima.
    """

    if costo <= 0:
        raise ValueError("costo debe ser > 0")

    mu_opt = tasa / (2 * costo)
    utilidad = tasa * mu_opt - costo * (mu_opt ** 2)

    return utilidad
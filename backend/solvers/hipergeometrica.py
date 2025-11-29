def hiper_media_var(n_total: int, n_buenos: int, n_muestra: int) -> dict:
    """
    Retorna {"media": ..., "varianza": ...}
    """

    if not (0 < n_muestra <= n_total):
        raise ValueError("0 < n_muestra <= n_total")
    if not (0 <= n_buenos <= n_total):
        raise ValueError("0 <= n_buenos <= n_total")
    if n_total <= 1:
        raise ValueError("n_total debe ser > 1")

    N = n_total
    K = n_buenos
    n = n_muestra

    p = K / N

    media = n * p
    varianza = n * p * (1 - p) * (N - n) / (N - 1)

    return {"media": media, "varianza": varianza}
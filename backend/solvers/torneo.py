from math import comb

def torneo_segundo_gana(**params) -> float:
    """
    Solver compatible con FastAPI. Espera:
    - n_partidos
    - k_min
    - p   (prob de que gane el PRIMER equipo)

    Retorna: Probabilidad de que el SEGUNDO gane el torneo.
    """

    n_partidos = int(params.get("n_partidos"))
    k_min = int(params.get("k_min"))
    p = float(params.get("p"))  # prob de que el PRIMER equipo gane

    # Validaciones
    if n_partidos <= 0:
        raise ValueError("n_partidos debe ser > 0")

    if not (0 <= k_min <= n_partidos):
        raise ValueError("k_min debe estar entre 0 y n_partidos")

    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1")

    # Probabilidad que el segundo gane un partido
    p_segundo = 1 - p
    q_segundo = 1 - p_segundo

    prob_total = 0.0

    # Sumar P(X = i) para i = k_min .. n
    for i in range(k_min, n_partidos + 1):
        prob_total += comb(n_partidos, i) * (p_segundo ** i) * (q_segundo ** (n_partidos - i))

    return prob_total
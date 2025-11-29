def clean_params(params: dict, solver: str) -> dict:
    """
    Arregla y normaliza parámetros generados aleatoriamente:
    - Normaliza probabilidades para que sumen 1
    - Garantiza relaciones como t_min <= t_max
    - Clips, redondeos y consistencia lógica
    """

    # -------------------------------
    # 1. Normalizar probabilidades tipo p_0, p_1, p_2
    # -------------------------------
    prob_keys = [k for k in params.keys() if k.startswith("p_")]
    if len(prob_keys) >= 2:
        total = sum(params[k] for k in prob_keys)
        if total > 0:
            for k in prob_keys:
                params[k] = round(params[k] / total, 5)

    # -------------------------------
    # 2. Normalizar probabilidades tipo multinomial p1, p2, p3...
    # -------------------------------
    probn_keys = [k for k in params.keys() if k.startswith("p") and k[1:].isdigit()]
    if len(probn_keys) >= 2:
        total = sum(params[k] for k in probn_keys)
        if total > 0:
            for k in probn_keys:
                params[k] = round(params[k] / total, 5)

    # -------------------------------
    # 3. Exchange if t_min > t_max (normal distribution)
    # -------------------------------
    if "t_min" in params and "t_max" in params:
        if params["t_min"] > params["t_max"]:
            params["t_min"], params["t_max"] = params["t_max"], params["t_min"]

    # -------------------------------
    # 4. Defectuosos: limitar k_excede, k_menor <= n_muestra
    # -------------------------------
    if solver == "probs_defectuosos":
        n = params["n_muestra"]
        params["k_excede"] = min(params["k_excede"], n)
        params["k_menor"] = min(params["k_menor"], n)

    # -------------------------------
    # 5. Torneo: k_min <= n_partidos
    # -------------------------------
    if solver == "torneo_segundo_gana":
        n = params["n_partidos"]
        params["k_min"] = min(params["k_min"], n)

    # -------------------------------
    # 6. Variables que deben ser positivas
    # -------------------------------
    for key in ["alpha", "desviacion_horas", "tasa", "anos"]:
        if key in params and params[key] < 0:
            params[key] = abs(params[key])

    # -------------------------------
    # 7. Redondeo general final
    # -------------------------------
    for k, v in params.items():
        if isinstance(v, float):
            params[k] = round(v, 5)

    return params
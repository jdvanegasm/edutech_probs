from math import comb
from typing import Dict, Any

def probs_defectuosos(**params) -> Dict[str, float]:
    """
    Calcula dos probabilidades:
    - P(X > k_excede)
    - P(X < k_menor)
    """

    p = float(params.get("p_defectuosos"))
    n = int(params.get("n_muestra"))
    k_excede = int(params.get("k_excede"))
    k_menor = int(params.get("k_menor"))

    # Validaciones
    if n <= 0:
        raise ValueError("n_muestra debe ser > 0")
    if not (0 <= p <= 1):
        raise ValueError("p_defectuosos debe estar entre 0 y 1")
    if not (0 <= k_excede <= n):
        raise ValueError("k_excede fuera de rango")
    if not (0 <= k_menor <= n):
        raise ValueError("k_menor fuera de rango")

    q = 1 - p

    # CDF de binomial: P(X <= t)
    def binom_cdf(t: int) -> float:
        total = 0.0
        for k in range(t + 1):
            total += comb(n, k) * (p ** k) * (q ** (n - k))
        return total

    # P(X > k_excede)
    prob_excede = 1 - binom_cdf(k_excede)

    # P(X < k_menor)
    prob_menor = binom_cdf(k_menor - 1) if k_menor > 0 else 0.0

    return {
        "prob_excede": prob_excede,
        "prob_menor": prob_menor
    }
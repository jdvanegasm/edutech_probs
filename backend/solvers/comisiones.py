from typing import Any

def valor_esperado_comisiones(**params) -> float:
    """
    E = p1*c1 + p2*c2
    """

    p1 = float(params.get("p_exito_1"))
    p2 = float(params.get("p_exito_2"))
    c1 = float(params.get("comision_1"))
    c2 = float(params.get("comision_2"))

    if not (0 <= p1 <= 1):
        raise ValueError("p_exito_1 fuera de rango")
    if not (0 <= p2 <= 1):
        raise ValueError("p_exito_2 fuera de rango")

    return p1 * c1 + p2 * c2
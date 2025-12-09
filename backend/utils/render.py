# utils/render.py

import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from typing import Any, Dict


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def _to_string(value: Any) -> str:
    """
    Convierte valores numéricos a string limpio,
    evitando notación científica para floats.
    """
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


# ---------------------------------------------------------
# TEMPLATE RENDERING (LATEX + PYTHON FORMAT SEGURO)
# ---------------------------------------------------------

def render_template(template: str, params: Dict[str, Any]) -> str:
    """
    Safe LaTeX + Python format renderer:

    1. Escapa TODAS las llaves LaTeX ({ -> {{, } -> }})
    2. Restaura ONLY placeholders reales {n}, {p}, etc.
    """

    # 1. Escapar todas las llaves
    safe = template.replace("{", "{{").replace("}", "}}")

    # 2. Restaurar SOLO placeholders reales
    for key in params.keys():
        safe = safe.replace("{{" + key + "}}", "{" + key + "}")

    # 3. Convertir valores a strings seguros
    safe_params = {k: _to_string(v) for k, v in params.items()}

    # 4. Aplicar format
    return safe.format(**safe_params)


# ---------------------------------------------------------
# SAFE MATH ENVIRONMENT
# ---------------------------------------------------------

SAFE_MATH_FUNCS = {
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "factorial": math.factorial,
    "binom": math.comb,
    "comb": math.comb,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
    "Phi": lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))   # Normal CDF
}


# ---------------------------------------------------------
# SYMBOLIC EXPRESSION EVALUATOR — FIXED VERSION
# ---------------------------------------------------------

def eval_symbolic_expression(expr: str, params: Dict[str, Any], q) -> float:
    """
    Evalúa expresiones simbólicas (pueden tener múltiples statements).

    FIX IMPORTANTE:
        Convierte a entero todos los parámetros cuyo tipo en el JSON es "int".
        Esto evita errores en factorial(), comb(), binom(), etc.
    """

    statements = [s.strip() for s in expr.split(";") if s.strip()]

    local_vars = {}

    # Convertir valores según corresponda (int / float)
    for k, v in params.items():

        # Revisar si en el JSON está como entero
        if k in q.params and q.params[k].type == "int":
            local_vars[k] = int(round(v))
        else:
            local_vars[k] = float(v)

    safe_globals = {"__builtins__": {}, **SAFE_MATH_FUNCS}

    result = None
    for st in statements:
        result = eval(st, safe_globals, local_vars)

    if not isinstance(result, (int, float)):
        raise ValueError(f"Expresión no produjo un número: {expr}")

    return float(result)


# ---------------------------------------------------------
# NUMERIC FORMATTING
# ---------------------------------------------------------

ROUNDING_MODES = {
    "half_up": ROUND_HALF_UP,
    "half_even": ROUND_HALF_EVEN
}


def format_numeric(value: float, spec: Dict[str, Any]) -> str:
    """
    Formatea el número final para UI.
    """
    spec = spec or {"type": "decimal", "decimals": 4}
    n_dec = spec.get("decimals", 4)
    rounding = spec.get("rounding", "half_up")

    q = Decimal(str(value)).quantize(
        Decimal("1." + ("0" * n_dec)),
        rounding=ROUNDING_MODES.get(rounding, ROUND_HALF_UP)
    )

    return str(q)


# ---------------------------------------------------------
# MASTER RENDER FOR EACH MATH RESULT
# ---------------------------------------------------------

def render_math_result(math_def: Dict[str, Any], params: Dict[str, Any], q) -> Dict[str, Any]:

    expr_latex = render_template(math_def["expression_latex_template"], params)

    # 👉 AHORA eval recibe "q"
    raw_value = eval_symbolic_expression(math_def["expression_symbolic"], params, q)

    numeric_fmt = math_def.get("numeric_format", {"type": "decimal", "decimals": 4})
    formatted = format_numeric(raw_value, numeric_fmt)

    return {
        "id": math_def["id"],
        "label": math_def["label"],
        "general_formula_latex": math_def["general_formula_latex"],
        "expression_latex": expr_latex,
        "numeric_value": formatted,
        "raw_numeric": raw_value
    }
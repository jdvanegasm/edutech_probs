from .binomial import binomial_exact
from .multinomial import multinomial_prob
from .torneo import torneo_segundo_gana
from .poisson import poisson_mas_de_un
from .defectuosos import probs_defectuosos
from .exponencial import prob_falla_antes
from .weibull import prob_bateria_operacion
from .normal_bateria import prob_bateria_entre
from .resistores import media_var_resistores
from .comisiones import valor_esperado_comisiones
from .utilidad import utilidad_maxima
from .esferas import proporcion_esferas
from .hipergeometrica import hiper_media_var
from .binomial_al_menos import binomial_al_menos
from .poisson_exacto import poisson_exacto
from .normal_mayor_que import normal_mayor_que

SOLVERS = {
    "binomial_exact": binomial_exact,
    "multinomial_prob": multinomial_prob,
    "torneo_segundo_gana": torneo_segundo_gana,
    "poisson_mas_de_un": poisson_mas_de_un,
    "probs_defectuosos": probs_defectuosos,
    "prob_falla_antes": prob_falla_antes,
    "prob_bateria_operacion": prob_bateria_operacion,
    "prob_bateria_entre": prob_bateria_entre,
    "media_var_resistores": media_var_resistores,
    "valor_esperado_comisiones": valor_esperado_comisiones,
    "utilidad_maxima": utilidad_maxima,
    "proporcion_esferas": proporcion_esferas,
    "hiper_media_var": hiper_media_var,
    "binomial_al_menos": binomial_al_menos,
    "poisson_exacto": poisson_exacto,
    "normal_mayor_que": normal_mayor_que
}
from math import erf, sqrt

def proporcion_esferas(media: float, desviacion: float, centro: float, tolerancia: float) -> float:
    if desviacion <= 0:
        raise ValueError("desviacion debe ser > 0")
    if tolerancia < 0:
        raise ValueError("tolerancia debe ser >= 0")

    a = centro - tolerancia
    b = centro + tolerancia

    def normal_cdf(x):
        z = (x - media) / desviacion
        return 0.5 * (1 + erf(z / sqrt(2)))

    return normal_cdf(b) - normal_cdf(a)

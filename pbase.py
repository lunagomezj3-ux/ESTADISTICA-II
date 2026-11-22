"""
pbase.py · Utilidades comunes de los generadores de ejercicios
--------------------------------------------------------------
Un ejercicio es un diccionario:
  tema, nivel, enunciado (texto plano), tabla (filas o None), formulas (lista de LaTeX de ayuda),
  pasos (lista de (texto, latex|None)), respuesta (texto plano).
Los números se dan con punto decimal. Los textos no usan letras griegas (para que el PDF salga limpio);
las letras griegas solo aparecen dentro del LaTeX.
"""

from __future__ import annotations

import math

from scipy.stats import norm
from scipy.stats import t as tdist

Step = tuple  # (texto, latex | None)


def g(x: float, d: int = 2) -> str:
    """Número compacto: 70.0 -> '70', 4.50 -> '4.5', 0.1234 -> '0.12' (d decimales máx.)."""
    s = f"{x:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def mk(tema, nivel, enunciado, pasos, respuesta, formulas=None, tabla=None) -> dict:
    return {"tema": tema, "nivel": nivel, "enunciado": enunciado, "tabla": tabla,
            "formulas": formulas or [], "pasos": pasos, "respuesta": respuesta}


def zcrit(area_right: float) -> float:
    """z que deja area_right a su derecha, con 3 decimales (1.645, 1.960, 2.326, 2.576...)."""
    return round(float(norm.ppf(1 - area_right)), 3)


def tcrit(area_right: float, gl: int) -> float:
    return round(float(tdist.ppf(1 - area_right, gl)), 3)


def phi(z: float) -> float:
    """Área a la izquierda como en la tabla Z (z redondeado a 2 decimales)."""
    return float(norm.cdf(round(z, 2)))


# --------------------------------------------------------------------------- contextos
CTX_N = [
    ("la estatura de los estudiantes de una universidad", "cm", (165, 175), (5, 8)),
    ("el tiempo de espera para ser atendido en una EPS", "minutos", (25, 45), (5, 9)),
    ("el consumo mensual de energía de un hogar", "kWh", (150, 250), (20, 40)),
    ("el peso de los paquetes de café de una empacadora", "gramos", (480, 520), (8, 15)),
    ("el puntaje de un examen de admisión", "puntos", (60, 75), (8, 12)),
    ("la duración de la batería de un celular", "horas", (10, 16), (2, 3)),
]

# (sujeto de la media, unidad, rango de mu0, rango de sigma o s)
CTX_H = [
    ("el tiempo medio de entrega de un pedido", "minutos", (30, 60), (4, 9)),
    ("el contenido medio de una botella de bebida", "mililitros", (350, 500), (4, 10)),
    ("la duración media de un lote de bombillas", "horas", (800, 1200), (40, 90)),
    ("el gasto medio mensual de un hogar en transporte", "miles de pesos", (120, 250), (15, 35)),
    ("el rendimiento medio de combustible de un vehículo", "km por galón", (30, 50), (2, 5)),
    ("el peso medio de un bulto de cemento", "kg", (48, 52), (1, 3)),
]

CTX_P = [
    ("la proporción de clientes que compra por internet", "clientes"),
    ("la proporción de piezas defectuosas de una fábrica", "piezas"),
    ("la proporción de estudiantes que aprueba un curso", "estudiantes"),
    ("la proporción de votantes que apoya una propuesta", "votantes"),
]

N_CUADRADO = [16, 25, 36, 49, 64, 100]


def ctx_mean(rng):
    subj, unit, mr, sr = rng.choice(CTX_H)
    return subj, unit, rng.randint(*mr), rng.randint(*sr)


# --------------------------------------------------------------------------- hipótesis
TAIL_TXT = {"right": "cola derecha (prueba unilateral)", "left": "cola izquierda (prueba unilateral)",
            "two": "dos colas (prueba bilateral)"}


def h1_words(tail: str, subj: str, mu0, unit: str) -> str:
    if tail == "right":
        return f"{subj} ha aumentado respecto a {g(mu0)} {unit}"
    if tail == "left":
        return f"{subj} ha disminuido respecto a {g(mu0)} {unit}"
    return f"{subj} es diferente de {g(mu0)} {unit}"


def sospecha(tail: str, subj: str, mu0, unit: str) -> str:
    if tail == "right":
        return f"Se sospecha que {subj} ha aumentado respecto al valor histórico de {g(mu0)} {unit}."
    if tail == "left":
        return f"Se sospecha que {subj} ha disminuido respecto al valor histórico de {g(mu0)} {unit}."
    return f"Se quiere comprobar si {subj} es diferente del valor histórico de {g(mu0)} {unit}."


def hyp_latex(tail: str, sym: str, v) -> str:
    v = g(v, 4)
    if tail == "right":
        return rf"H_0:{sym}\leq {v}\qquad H_1:{sym}>{v}"
    if tail == "left":
        return rf"H_0:{sym}\geq {v}\qquad H_1:{sym}<{v}"
    return rf"H_0:{sym}={v}\qquad H_1:{sym}\neq {v}"


def hyp_plain(tail: str, sym: str, v) -> str:
    v = g(v, 4)
    return {"right": f"H0: {sym} <= {v} vs H1: {sym} > {v}",
            "left": f"H0: {sym} >= {v} vs H1: {sym} < {v}",
            "two": f"H0: {sym} = {v} vs H1: {sym} != {v}"}[tail]


def crit_of(tail: str, alpha: float, dist: str = "z", gl: int | None = None) -> float:
    a = alpha / 2 if tail == "two" else alpha
    return zcrit(a) if dist == "z" else tcrit(a, gl)


def crit_steps(tail: str, alpha: float, sym: str = "z", gl: int | None = None) -> tuple[list[Step], float]:
    """Paso del valor crítico (z o t) con su explicación."""
    c = crit_of(tail, alpha, "z" if sym == "z" else "t", gl)
    sub = f"{sym}_{{{g(alpha / 2, 4)}}}" if tail == "two" else f"{sym}_{{{g(alpha, 4)}}}"
    if sym == "t":
        sub = sub[:-1] + rf",\,{gl}}}"
    if tail == "two":
        txt = (f"Con α = {g(alpha, 4)} en dos colas, cada cola tiene {g(alpha / 2, 4)} de área. "
               f"Se busca el valor crítico que deja {g(alpha / 2, 4)} a la derecha.")
        m = rf"{sub}={c:.3f}\qquad\Rightarrow\qquad \pm {c:.3f}"
    else:
        lado = "derecha" if tail == "right" else "izquierda"
        sgn = "" if tail == "right" else "-"
        txt = (f"Con α = {g(alpha, 4)} en una cola ({lado}), el valor crítico deja {g(alpha, 4)} de área en esa cola.")
        m = rf"{sub}={c:.3f}\qquad\Rightarrow\qquad {sgn}{c:.3f}"
    if sym == "t":
        txt += f" Se usa la tabla t con gl = {gl}."
    return [(txt, m)], c


def decide(tail: str, stat: float, crit: float, sym: str = "z") -> tuple[bool, list[Step]]:
    """Regla de decisión y decisión (compara con el estadístico redondeado a 2 decimales)."""
    s = round(stat, 2)
    if tail == "right":
        rej, reg, cmpl = s > crit, rf"\mathrm{{Rechazar}}\ H_0\ \mathrm{{si}}\ {sym}_c>{crit:.3f}", rf"{s:.2f}>{crit:.3f}"
        cmpl = cmpl if rej else rf"{s:.2f}\leq {crit:.3f}"
    elif tail == "left":
        rej, reg = s < -crit, rf"\mathrm{{Rechazar}}\ H_0\ \mathrm{{si}}\ {sym}_c<-{crit:.3f}"
        cmpl = rf"{s:.2f}<-{crit:.3f}" if rej else rf"{s:.2f}\geq -{crit:.3f}"
    else:
        rej, reg = abs(s) > crit, rf"\mathrm{{Rechazar}}\ H_0\ \mathrm{{si}}\ |{sym}_c|>{crit:.3f}"
        cmpl = rf"|{s:.2f}|>{crit:.3f}" if rej else rf"|{s:.2f}|\leq {crit:.3f}"
    dec = "Se RECHAZA H0" if rej else "NO se rechaza H0"
    why = "el estadístico cae en la región de rechazo" if rej else "el estadístico no cae en la región de rechazo"
    return rej, [("Regla de decisión: se rechaza H0 si el estadístico cae en la región de rechazo.", reg),
                 (f"Se compara el estadístico calculado con el valor crítico. {dec} porque {why}.", cmpl)]


def conclusion(rej: bool, alpha: float, h1_txt: str) -> Step:
    if rej:
        return (f"Conclusión: con α = {g(alpha, 4)}, hay evidencia suficiente para afirmar que {h1_txt}.", None)
    return (f"Conclusión: con α = {g(alpha, 4)}, no hay evidencia suficiente para afirmar que {h1_txt}.", None)


def data_stats(rng, center: float, spread: float, n: int):
    """Datos enteros y sus estadísticos: (datos, media, SS, s)."""
    datos = [max(1, round(rng.gauss(center, spread))) for _ in range(n)]
    xbar = sum(datos) / n
    ss = sum((x - xbar) ** 2 for x in datos)
    return datos, xbar, ss, math.sqrt(ss / (n - 1))

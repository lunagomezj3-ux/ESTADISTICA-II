"""gen_c2.py · Generadores del SEGUNDO CORTE: IC, IC para la media, planteamiento, valor P, regla de decisión, t y proporción."""

from __future__ import annotations

import math

from scipy.stats import norm
from scipy.stats import t as tdist

from pbase import (CTX_P, N_CUADRADO, TAIL_TXT, conclusion, crit_of, crit_steps, ctx_mean, data_stats, decide, g,
                   h1_words, hyp_latex, hyp_plain, mk, phi, sospecha, tcrit, zcrit)

CONF = [0.80, 0.90, 0.95, 0.98, 0.99]


# =========================================================================== IC (conceptos)
def gen_ic_zcrit(rng, nivel):
    conf = rng.choice(CONF)
    a = round(1 - conf, 2)
    z = zcrit(a / 2)
    enun = f"Para construir un intervalo de confianza del {g(conf * 100)}% para una media con sigma conocida, encuentre alfa, alfa/2 y el valor crítico z de alfa/2."
    pasos = [("El nivel de significancia es lo que falta para llegar a 1.", rf"\alpha=1-{g(conf, 2)}={g(a, 2)}"),
             ("El error se reparte en las dos colas de la campana.", rf"\frac{{\alpha}}{{2}}=\frac{{{g(a, 2)}}}{{2}}={g(a / 2, 3)}"),
             ("El área a la izquierda de z de alfa/2 es 1 menos el área de la cola derecha.", rf"\Phi(z)=1-{g(a / 2, 3)}={g(1 - a / 2, 3)}"),
             ("Se busca ese área en el cuerpo de la tabla Z y se lee z.", rf"z_{{\alpha/2}}={z:.3f}")]
    return mk("ic", nivel, enun, pasos, f"alfa = {g(a, 2)}; alfa/2 = {g(a / 2, 3)}; z = {z:.3f}", [r"\alpha=1-\mathrm{confianza}", r"z_{\alpha/2}"])


def gen_ic_interp(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    conf = rng.choice([0.90, 0.95, 0.99])
    lo = mu0 - rng.randint(1, 3)
    hi = lo + rng.randint(3, 6)
    enun = (f"Con base en una muestra, un analista construyó un intervalo de confianza del {g(conf * 100)}% para {subj} y obtuvo ({g(lo)} ; {g(hi)}) {unit}. "
            f"(a) Escriba la interpretación correcta. (b) Un compañero dice: 'hay una probabilidad de {g(conf * 100)}% de que la media verdadera esté entre {g(lo)} y {g(hi)}'. ¿Es correcto?")
    pasos = [("La media poblacional es un valor fijo (aunque desconocido): o está dentro del intervalo calculado o no está. Lo aleatorio es el intervalo, que cambia de muestra en muestra.", None),
             (f"Interpretación correcta: si se repitiera el muestreo muchas veces y se construyera un intervalo con este método cada vez, aproximadamente el {g(conf * 100)}% de esos intervalos contendría la media verdadera.", None),
             (f"Resumen para el contexto: tenemos {g(conf * 100)}% de confianza en que la media de {subj} está entre {g(lo)} y {g(hi)} {unit}.", None),
             ("La frase del compañero no es correcta: habla de probabilidad sobre un intervalo ya calculado, y la media ya es fija.", None)]
    return mk("ic", nivel, enun, pasos, f"Confianza del {g(conf * 100)}% en el método, no probabilidad del intervalo ya calculado; la frase del compañero es incorrecta.")


def gen_ic_elegir(rng, nivel):
    casos = [("la desviación estándar poblacional es conocida (sigma = 12) y n = 40", "z", "Sigma conocida: se usa la normal."),
             ("la desviación estándar poblacional es desconocida; solo se tiene la de la muestra (s = 4.5), n = 15 y la población es aproximadamente normal", "t", "Sigma desconocida y n pequeña: se usa t con n - 1 gl."),
             ("la desviación estándar poblacional es desconocida; se tiene s = 3.1 y n = 12 de una población aproximadamente normal", "t", "Sigma desconocida: se estima con s y se usa t con 11 gl."),
             ("la desviación estándar poblacional es conocida (sigma = 5) y la población es normal con n = 9", "z", "Con sigma conocida y población normal, z sirve incluso con n pequeña.")]
    t, dist, why = rng.choice(casos)
    enun = f"Se quiere construir un intervalo de confianza para una media y {t}. ¿Se debe usar la distribución z o la t de Student? Justifique y escriba la fórmula del intervalo."
    f = r"\bar{x}\pm z_{\alpha/2}\,\frac{\sigma}{\sqrt{n}}" if dist == "z" else r"\bar{x}\pm t_{\alpha/2,\,n-1}\,\frac{s}{\sqrt{n}}"
    pasos = [("Pregunta clave: ¿la desviación estándar que se tiene es la poblacional (sigma) o la de la muestra (s)?", None), (why, None),
             ("Fórmula del intervalo:", f)]
    return mk("ic", nivel, enun, pasos, f"Usar {dist}. {why}", [r"\bar{x}\pm z_{\alpha/2}\frac{\sigma}{\sqrt{n}}", r"\bar{x}\pm t_{\alpha/2,\,n-1}\frac{s}{\sqrt{n}}"])


def gen_ic_margen(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    n = rng.choice(N_CUADRADO)
    conf = rng.choice([0.90, 0.95, 0.99])
    z = zcrit((1 - conf) / 2)
    se = sigma / math.sqrt(n)
    e = z * se
    e4 = z * sigma / math.sqrt(4 * n)
    enun = (f"Con sigma = {g(sigma)} {unit} conocida y una muestra de n = {n} para estimar {subj}, calcule el margen de error con una confianza del {g(conf * 100)}% "
            f"y el ancho total del intervalo. ¿Cuánto vale el margen si la muestra se cuadruplica?")
    pasos = [(f"Valor crítico para {g(conf * 100)}% de confianza.", rf"z_{{\alpha/2}}=z_{{{g((1 - conf) / 2, 3)}}}={z:.3f}"),
             ("Error estándar.", rf"\frac{{\sigma}}{{\sqrt{{n}}}}=\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
             ("Margen de error = valor crítico por error estándar.", rf"E=z_{{\alpha/2}}\frac{{\sigma}}{{\sqrt{{n}}}}={z:.3f}\times{se:.4f}={e:.4f}"),
             ("El ancho del intervalo es el doble del margen (un margen a cada lado).", rf"\mathrm{{Ancho}}=2E=2({e:.4f})={2 * e:.4f}"),
             ("Con 4n datos, la raíz de n se duplica, entonces el margen se reduce a la mitad.", rf"E'={z:.3f}\times\frac{{{g(sigma)}}}{{\sqrt{{{4 * n}}}}}={e4:.4f}")]
    return mk("ic", nivel, enun, pasos, f"E = {e:.4f} {unit}; ancho = {2 * e:.4f}; con 4n el margen es {e4:.4f}", [r"E=z_{\alpha/2}\frac{\sigma}{\sqrt{n}}"])


def gen_ic_n(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    sigma = max(sigma, 3)
    e = rng.choice([1, 2, 0.5, 1.5])
    conf = rng.choice([0.90, 0.95, 0.99])
    z = zcrit((1 - conf) / 2)
    n_raw = (z * sigma / e) ** 2
    n = math.ceil(n_raw)
    enun = (f"Se desea estimar {subj} con un margen de error máximo de {g(e)} {unit}, una confianza del {g(conf * 100)}% y sigma = {g(sigma)} {unit}. "
            f"¿Qué tamaño de muestra se necesita?")
    pasos = [("Se despeja n de la fórmula del margen de error.", r"E=z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\ \Rightarrow\ n=\left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^{2}"),
             ("Valor crítico.", rf"z_{{\alpha/2}}={z:.3f}"),
             ("Se sustituye.", rf"n=\left(\frac{{{z:.3f}\times{g(sigma)}}}{{{g(e)}}}\right)^{{2}}=({z * sigma / e:.4f})^2={n_raw:.4f}"),
             ("Se redondea SIEMPRE hacia arriba, porque con menos datos no se alcanzaría el margen deseado.", rf"n={n}")]
    resp = f"n = {n}"
    if nivel == "Difícil":
        z2 = zcrit(0.005)
        n2 = math.ceil((z2 * sigma / e) ** 2)
        enun += " Compare con el tamaño necesario si la confianza fuera del 99%."
        pasos += [("Con 99% de confianza el valor crítico es mayor, así que se necesita más muestra.", rf"n=\left(\frac{{{z2:.3f}\times{g(sigma)}}}{{{g(e)}}}\right)^{{2}}={(z2 * sigma / e) ** 2:.4f}\ \Rightarrow\ n={n2}")]
        resp += f"; con 99%: n = {n2}"
    return mk("ic", nivel, enun, pasos, resp, [r"n=\left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^{2}"])


# =========================================================================== IC para la media
def _ic_texto(subj, unit, conf, lo, hi):
    return f"Interpretación: con {g(conf * 100)}% de confianza, {subj} está entre {lo:.2f} y {hi:.2f} {unit}."


def gen_ic_z(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    n = rng.choice(N_CUADRADO)
    conf = 0.95 if nivel == "Fácil" else rng.choice([0.90, 0.95, 0.99])
    xbar = round(mu0 + rng.uniform(-1, 1) * sigma / 2, 2)
    z = zcrit((1 - conf) / 2)
    se = sigma / math.sqrt(n)
    e = z * se
    lo, hi = xbar - e, xbar + e
    enun = (f"Para estudiar {subj}, se tomó una muestra de n = {n} observaciones con una media de {g(xbar)} {unit}. Se sabe que la desviación estándar poblacional es {g(sigma)} {unit}. "
            f"Construya un intervalo de confianza del {g(conf * 100)}% para la media poblacional e interprételo.")
    pasos = [("Como sigma es conocida, se usa la distribución normal.", rf"\bar{{x}}\pm z_{{\alpha/2}}\frac{{\sigma}}{{\sqrt{{n}}}}"),
             (f"Valor crítico para {g(conf * 100)}% de confianza (alfa = {g(1 - conf, 2)}).", rf"z_{{\alpha/2}}=z_{{{g((1 - conf) / 2, 3)}}}={z:.3f}"),
             ("Error estándar.", rf"\frac{{\sigma}}{{\sqrt{{n}}}}=\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
             ("Margen de error.", rf"E={z:.3f}\times{se:.4f}={e:.4f}"),
             ("Límites del intervalo: media muestral menos y más el margen.", rf"{g(xbar)}\pm{e:.4f}\ \Rightarrow\ ({lo:.4f}\ ;\ {hi:.4f})"),
             (_ic_texto(subj, unit, conf, lo, hi), None)]
    return mk("ic_media", nivel, enun, pasos, f"IC {g(conf * 100)}%: ({lo:.2f} ; {hi:.2f}) {unit}", [r"\bar{x}\pm z_{\alpha/2}\frac{\sigma}{\sqrt{n}}"])


def gen_ic_t(rng, nivel):
    subj, unit, mu0, s = ctx_mean(rng)
    n = rng.choice([8, 10, 12, 15, 20, 25])
    conf = rng.choice([0.90, 0.95, 0.99])
    xbar = round(mu0 + rng.uniform(-1, 1) * s / 2, 2)
    gl = n - 1
    t = tcrit((1 - conf) / 2, gl)
    se = s / math.sqrt(n)
    e = t * se
    lo, hi = xbar - e, xbar + e
    enun = (f"De una población aproximadamente normal sobre {subj} se tomó una muestra de n = {n}, con media {g(xbar)} {unit} y desviación estándar muestral s = {g(s)} {unit}. "
            f"Construya un intervalo de confianza del {g(conf * 100)}% para la media e interprételo.")
    pasos = [("La desviación estándar poblacional es desconocida (solo se tiene s), por eso se usa la t de Student.", rf"\bar{{x}}\pm t_{{\alpha/2,\,n-1}}\frac{{s}}{{\sqrt{{n}}}}"),
             ("Grados de libertad.", rf"gl=n-1={n}-1={gl}"),
             (f"Valor t: en la tabla t, fila gl = {gl}, con área {g((1 - conf) / 2, 3)} en una cola.", rf"t_{{{g((1 - conf) / 2, 3)},\,{gl}}}={t:.3f}"),
             ("Error estándar.", rf"\frac{{s}}{{\sqrt{{n}}}}=\frac{{{g(s)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
             ("Margen de error.", rf"E={t:.3f}\times{se:.4f}={e:.4f}"),
             ("Límites del intervalo.", rf"{g(xbar)}\pm{e:.4f}\ \Rightarrow\ ({lo:.4f}\ ;\ {hi:.4f})"),
             (_ic_texto(subj, unit, conf, lo, hi), None)]
    return mk("ic_media", nivel, enun, pasos, f"IC {g(conf * 100)}%: ({lo:.2f} ; {hi:.2f}) {unit}", [r"\bar{x}\pm t_{\alpha/2,\,n-1}\frac{s}{\sqrt{n}}", r"gl=n-1"])


def gen_ic_datos(rng, nivel):
    subj, unit, mu0, s0 = ctx_mean(rng)
    n = rng.choice([6, 7, 8])
    datos, xbar, ss, s = data_stats(rng, mu0, max(s0, 3), n)
    conf = rng.choice([0.90, 0.95, 0.99])
    gl = n - 1
    t = tcrit((1 - conf) / 2, gl)
    se = s / math.sqrt(n)
    e = t * se
    lo, hi = xbar - e, xbar + e
    enun = (f"Se registraron {n} mediciones de {subj} ({unit}): {', '.join(map(str, datos))}. Suponga población aproximadamente normal. "
            f"Calcule la media y la desviación estándar muestrales y construya un intervalo de confianza del {g(conf * 100)}% para la media.")
    desv = "; ".join(f"({x}-{xbar:.2f})^2={(x - xbar) ** 2:.4f}" for x in datos)
    pasos = [("Media muestral: suma de los datos dividida entre n.", rf"\bar{{x}}=\frac{{\sum x_i}}{{n}}=\frac{{{sum(datos)}}}{{{n}}}={xbar:.4f}"),
             ("Cuadrados de las desviaciones de cada dato respecto a la media:", None), (desv, None),
             ("Suma de cuadrados.", rf"\sum(x_i-\bar{{x}})^2={ss:.4f}"),
             ("Varianza muestral (se divide entre n - 1) y desviación estándar.", rf"s^2=\frac{{{ss:.4f}}}{{{n}-1}}={ss / (n - 1):.4f}\qquad s=\sqrt{{{ss / (n - 1):.4f}}}={s:.4f}"),
             ("Como se usa s, el intervalo es con t de Student.", rf"gl={gl}\qquad t_{{{g((1 - conf) / 2, 3)},\,{gl}}}={t:.3f}"),
             ("Margen de error.", rf"E=t\frac{{s}}{{\sqrt{{n}}}}={t:.3f}\times\frac{{{s:.4f}}}{{\sqrt{{{n}}}}}={e:.4f}"),
             ("Límites del intervalo.", rf"{xbar:.4f}\pm{e:.4f}\ \Rightarrow\ ({lo:.4f}\ ;\ {hi:.4f})"),
             (_ic_texto(subj, unit, conf, lo, hi), None)]
    return mk("ic_media", nivel, enun, pasos, f"media = {xbar:.2f}; s = {s:.4f}; IC {g(conf * 100)}%: ({lo:.2f} ; {hi:.2f}) {unit}",
              [r"s=\sqrt{\frac{\sum (x_i-\bar{x})^2}{n-1}}", r"\bar{x}\pm t_{\alpha/2,\,n-1}\frac{s}{\sqrt{n}}"])


# =========================================================================== PLANTEAMIENTO
MEAN_CTX = [("la duración media de las baterías de un fabricante", "horas", (18, 30)),
            ("el tiempo medio de atención en una ventanilla", "minutos", (8, 20)),
            ("el rendimiento medio de combustible de un vehículo", "km por galón", (30, 50)),
            ("el contenido medio de una lata de bebida", "mililitros", (330, 355))]

# clave: (H0, H1, cola, plantilla de la frase)
PLANT = {
    "mayor": (r"\leq", ">", "right", "Un investigador quiere comprobar si {s} es mayor que {v}."),
    "menor": (r"\geq", "<", "left", "Un investigador quiere comprobar si {s} es menor que {v}."),
    "dif": ("=", r"\neq", "two", "Un investigador quiere comprobar si {s} es diferente de {v}."),
    "almenos": (r"\geq", "<", "left", "Un fabricante afirma que {s} es al menos {v}. Un auditor sospecha que es menor."),
    "alsumo": (r"\leq", ">", "right", "Una empresa asegura que {s} es a lo sumo {v}. Un cliente sospecha que es mayor."),
    "igual": ("=", r"\neq", "two", "Históricamente {s} ha sido {v}. Se quiere verificar si ha cambiado."),
}
PLAIN = {r"\leq": "<=", r"\geq": ">=", "=": "=", ">": ">", "<": "<", r"\neq": "!="}


def gen_plantea(rng, nivel):
    claves = ["mayor", "menor", "dif"] if nivel == "Fácil" else list(PLANT)
    k = rng.choice(claves)
    h0, h1, tail, tpl = PLANT[k]
    es_prop = nivel != "Fácil" and rng.random() < 0.5
    if es_prop:
        subj, _ = rng.choice(CTX_P)
        v = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 0.8])
        vt, sym, symp, vl = f"{g(v * 100)}%", "p", "p", g(v, 2)
    else:
        subj, unit, (a, b) = rng.choice(MEAN_CTX)
        v = rng.randint(a, b)
        vt, sym, symp, vl = f"{v} {unit}", r"\mu", "mu", str(v)
    frase = tpl.format(s=subj, v=vt)
    comp = {"mayor": "mayor que", "menor": "menor que", "dif": "diferente de", "almenos": "menor que", "alsumo": "mayor que", "igual": "diferente de"}[k]
    h1txt = f"{subj} es {comp} {vt}"
    enun = f"{frase} Plantee las hipótesis nula y alterna."
    if nivel == "Difícil":
        enun = f"{frase} (a) Plantee H0 y H1. (b) Indique si la prueba es de una o de dos colas y de cuál. (c) Describa con palabras el error tipo I y el error tipo II en este contexto."
    pasos = [("Identifica el parámetro: se habla de una " + ("proporción (p)." if es_prop else "media poblacional (mu)."), None),
             ("Identifica qué se quiere demostrar o sospecha: eso va en H1, que usa <, > o diferente de.", rf"H_1:{sym}{h1}{vl}"),
             ("H0 es lo contrario y siempre lleva el signo de igualdad (=, ≤ o ≥).".replace("≤", "menor o igual").replace("≥", "mayor o igual"), rf"H_0:{sym}{h0}{vl}"),
             ("Resultado completo:", hyp_latex_custom(sym, h0, h1, vl))]
    resp = f"H0: {symp} {PLAIN[h0]} {vl} vs H1: {symp} {PLAIN[h1]} {vl}"
    if nivel != "Fácil":
        pasos.append((f"Tipo de prueba: {TAIL_TXT[tail]}, porque H1 usa el signo {PLAIN[h1].replace('!=', 'diferente de')}.", None))
        resp += f"; {TAIL_TXT[tail]}"
    if nivel == "Difícil":
        pasos += [(f"Error tipo I: rechazar H0 cuando es verdadera. Aquí: concluir que {h1txt} cuando en realidad no es así.", None),
                  (f"Error tipo II: no rechazar H0 cuando es falsa. Aquí: no encontrar evidencia de que {h1txt} cuando en realidad sí es así.", None)]
        resp += f"; error I: concluir que {h1txt} sin que sea cierto; error II: no detectar que {h1txt} cuando sí lo es"
    return mk("plant", nivel, enun, pasos, resp, [r"H_0:\mu=\mu_0\ \ \mathrm{vs}\ \ H_1:\mu\neq\mu_0"])


def hyp_latex_custom(sym, h0, h1, v):
    return rf"H_0:{sym}{h0}{v}\qquad H_1:{sym}{h1}{v}"


# =========================================================================== VALOR P
def _p_val(tail, stat, dist="z", gl=None):
    if dist == "z":
        z = round(stat, 2)
        return {"right": 1 - phi(z), "left": phi(z), "two": 2 * (1 - phi(abs(z)))}[tail]
    return {"right": float(tdist.sf(stat, gl)), "left": float(tdist.cdf(stat, gl)), "two": float(2 * tdist.sf(abs(stat), gl))}[tail]


def _p_steps_z(tail, z):
    zr = round(z, 2)
    if tail == "right":
        return (f"Cola derecha: el valor P es el área a la derecha del estadístico.", rf"P=P(Z>{zr:.2f})=1-\Phi({zr:.2f})=1-{phi(zr):.4f}={1 - phi(zr):.4f}")
    if tail == "left":
        return (f"Cola izquierda: el valor P es el área a la izquierda del estadístico.", rf"P=P(Z<{zr:.2f})=\Phi({zr:.2f})={phi(zr):.4f}")
    return ("Dos colas: se toma el área de una cola (la del lado extremo, usando el valor absoluto) y se duplica.",
            rf"P=2\,[1-\Phi(|{zr:.2f}|)]=2\,[1-{phi(abs(zr)):.4f}]=2({1 - phi(abs(zr)):.4f})={2 * (1 - phi(abs(zr))):.4f}")


def _alpha_decision(p, alpha):
    rej = p <= alpha
    return rej, (f"Se compara con alfa: P = {p:.4f} {'<=' if rej else '>'} {g(alpha, 2)}, así que {'SE RECHAZA' if rej else 'NO se rechaza'} H0.",
                 rf"{p:.4f}{r'\leq' if rej else '>'}{g(alpha, 2)}")


def gen_p_z(rng, nivel):
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    z = round(rng.uniform(0.3, 3.0) * (-1 if tail == "left" else 1 if tail == "right" else rng.choice([-1, 1])), 2)
    p = _p_val(tail, z)
    enun = (f"En una prueba Z de {TAIL_TXT[tail]} se obtuvo un estadístico z = {z:.2f}. Calcule el valor P y tome la decisión con alfa = {g(alpha, 2)}.")
    rej, dec = _alpha_decision(p, alpha)
    pasos = [("El valor P depende de la cola de la prueba (la que indica H1).", None), _p_steps_z(tail, z), dec,
             ("Interpretación: el valor P es la probabilidad de obtener un resultado tan extremo o más si H0 fuera verdadera; si es pequeño, los datos contradicen a H0.", None)]
    return mk("pvalor", nivel, enun, pasos, f"P = {p:.4f}; {'se rechaza H0' if rej else 'no se rechaza H0'} con alfa = {g(alpha, 2)}",
              [r"P=1-\Phi(z_c)\ \ (\mathrm{derecha})", r"P=\Phi(z_c)\ \ (\mathrm{izquierda})", r"P=2[1-\Phi(|z_c|)]\ \ (\mathrm{dos\ colas})"])


def _bracket(t, gl):
    """Rango del área de una cola según la tabla t."""
    areas = [0.25, 0.10, 0.05, 0.025, 0.01, 0.005, 0.0005]
    crit = [float(tdist.ppf(1 - a, gl)) for a in areas]
    t = abs(t)
    if t < crit[0]:
        return ">0.25", None
    for i in range(len(areas) - 1):
        if crit[i] <= t < crit[i + 1]:
            return f"entre {areas[i + 1]} y {areas[i]}", (areas[i + 1], areas[i])
    return "<0.0005", None


def gen_p_t(rng, nivel):
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    gl = rng.choice([7, 9, 11, 14, 19, 24])
    t = round(rng.uniform(0.5, 3.4) * (-1 if tail == "left" else 1 if tail == "right" else rng.choice([-1, 1])), 2)
    p = _p_val(tail, t, "t", gl)
    rango, _ = _bracket(t, gl)
    enun = (f"En una prueba t de {TAIL_TXT[tail]} con {gl} grados de libertad se obtuvo t = {t:.2f}. Estime el valor P y decida con alfa = {g(alpha, 2)}.")
    rej, dec = _alpha_decision(p, alpha)
    if tail == "two":
        rango_txt = f"El área de UNA cola está {rango}; en dos colas se duplica."
    else:
        rango_txt = f"El área de la cola está {rango}."
    pasos = [("La tabla t solo da algunos valores críticos; con ella se ubica el valor P en un rango. Con calculadora o software se obtiene el valor exacto.", None),
             (f"En la fila gl = {gl} se ubica |t| = {abs(t):.2f} entre dos valores críticos. {rango_txt}", None),
             ("Valor P exacto (software o calculadora):", {"right": rf"P=P(T_{{{gl}}}>{t:.2f})={p:.4f}", "left": rf"P=P(T_{{{gl}}}<{t:.2f})={p:.4f}",
                                                           "two": rf"P=2\,P(T_{{{gl}}}>|{t:.2f}|)={p:.4f}"}[tail]), dec]
    return mk("pvalor", nivel, enun, pasos, f"P = {p:.4f} (rango en tabla: {rango}); {'se rechaza H0' if rej else 'no se rechaza H0'} con alfa = {g(alpha, 2)}",
              [r"P=P(T_{gl}>t_c)"])


def gen_p_completo(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    tail = rng.choice(["right", "left", "two"])
    n = rng.choice(N_CUADRADO)
    se = sigma / math.sqrt(n)
    zt = rng.uniform(0.8, 3.0) * (1 if tail == "right" else -1 if tail == "left" else rng.choice([-1, 1]))
    xbar = round(mu0 + zt * se, 2)
    z = (xbar - mu0) / se
    p = _p_val(tail, z)
    enun = (f"{sospecha(tail, subj, mu0, unit)} Una muestra de n = {n} dio una media de {g(xbar)} {unit} y se conoce sigma = {g(sigma)} {unit}. "
            f"(a) Calcule el estadístico y el valor P. (b) ¿Con cuáles niveles de significancia (0.10, 0.05, 0.01) se rechaza H0? (c) Interprete el valor P.")
    pasos = [("Hipótesis.", hyp_latex(tail, r"\mu", mu0)),
             ("Error estándar y estadístico Z.", rf"\frac{{\sigma}}{{\sqrt{{n}}}}={se:.4f}\qquad z_c=\frac{{{g(xbar)}-{g(mu0)}}}{{{se:.4f}}}={z:.2f}"),
             _p_steps_z(tail, z),
             ("Regla: se rechaza H0 en todo nivel alfa que sea mayor o igual que el valor P.", None)]
    rech = []
    for a in (0.10, 0.05, 0.01):
        r = p <= a
        if r:
            rech.append(g(a, 2))
        pasos.append((f"alfa = {g(a, 2)}: P = {p:.4f} {'<=' if r else '>'} {g(a, 2)} → {'se rechaza H0' if r else 'no se rechaza H0'}.", None))
    pasos.append((f"Interpretación del valor P: si H0 fuera cierta, la probabilidad de obtener una media muestral tan extrema o más que {g(xbar)} {unit} sería {p:.4f}.", None))
    resp = f"z = {z:.2f}; P = {p:.4f}; se rechaza H0 con alfa = {', '.join(rech) if rech else 'ninguno de los tres niveles'}"
    return mk("pvalor", nivel, enun, pasos, resp, [r"Z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}", r"P=2[1-\Phi(|z_c|)]"])


# =========================================================================== REGLA DE DECISIÓN
def gen_regla_crit(rng, nivel):
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    z = round(rng.uniform(0.4, 3.0) * (-1 if tail == "left" else 1 if tail == "right" else rng.choice([-1, 1])), 2)
    enun = (f"En una prueba Z de {TAIL_TXT[tail]} con alfa = {g(alpha, 2)}, el estadístico calculado fue z = {z:.2f}. "
            f"Encuentre el/los valor(es) crítico(s), describa la región de rechazo y tome la decisión.")
    cs, c = crit_steps(tail, alpha, "z")
    rej, ds = decide(tail, z, c, "z")
    pasos = cs + ds
    return mk("regla", nivel, enun, pasos, f"Valor critico {'+-' if tail == 'two' else ('' if tail == 'right' else '-')}{c:.3f}; {'se rechaza H0' if rej else 'no se rechaza H0'}",
              [r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ z_c\ \mathrm{cae\ en\ la\ región\ crítica}"])


def gen_regla_comp(rng, nivel):
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    z = round(rng.uniform(0.4, 3.0) * (-1 if tail == "left" else 1 if tail == "right" else rng.choice([-1, 1])), 2)
    enun = (f"En una prueba Z de {TAIL_TXT[tail]} con alfa = {g(alpha, 2)}, el estadístico fue z = {z:.2f}. Tome la decisión con los dos métodos "
            f"(valor crítico y valor P) y compruebe que coinciden.")
    cs, c = crit_steps(tail, alpha, "z")
    rej, ds = decide(tail, z, c, "z")
    p = _p_val(tail, z)
    rej2, dec = _alpha_decision(p, alpha)
    pasos = [("Método 1 · Valor crítico.", None)] + cs + ds + [("Método 2 · Valor P.", None), _p_steps_z(tail, z), dec,
                                                                ("Ambos métodos llevan a la misma decisión; el valor P además indica qué tan fuerte es la evidencia.", None)]
    return mk("regla", nivel, enun, pasos, f"Valor critico: {'rechaza' if rej else 'no rechaza'} H0; P = {p:.4f}: {'rechaza' if rej2 else 'no rechaza'} H0 (coinciden)",
              [r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ P\leq\alpha"])


def gen_regla_t(rng, nivel):
    subj, unit, mu0, s = ctx_mean(rng)
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    n = rng.choice([9, 12, 16, 20, 25])
    gl = n - 1
    se = s / math.sqrt(n)
    zt = rng.uniform(0.6, 3.2) * (1 if tail == "right" else -1 if tail == "left" else rng.choice([-1, 1]))
    xbar = round(mu0 + zt * se, 2)
    t = (xbar - mu0) / se
    enun = (f"{sospecha(tail, subj, mu0, unit)} Con n = {n}, la muestra dio media {g(xbar)} {unit} y desviación estándar s = {g(s)} {unit} (población aproximadamente normal). "
            f"Aplique la regla de decisión con alfa = {g(alpha, 2)}, redacte la conclusión e indique qué error podría estar cometiéndose.")
    pasos = [("Hipótesis.", hyp_latex(tail, r"\mu", mu0))]
    cs, c = crit_steps(tail, alpha, "t", gl)
    pasos += cs + [("Estadístico t (sigma desconocida).", rf"t_c=\frac{{\bar{{x}}-\mu_0}}{{s/\sqrt{{n}}}}=\frac{{{g(xbar)}-{g(mu0)}}}{{{g(s)}/\sqrt{{{n}}}}}=\frac{{{g(xbar - mu0, 4)}}}{{{se:.4f}}}={t:.2f}")]
    rej, ds = decide(tail, t, c, "t")
    pasos += ds + [conclusion(rej, alpha, h1_words(tail, subj, mu0, unit))]
    pasos.append(("Error posible: " + ("al rechazar H0 se podría estar cometiendo error tipo I (rechazar una H0 verdadera)." if rej else
                                       "al no rechazar H0 se podría estar cometiendo error tipo II (no detectar un cambio real)."), None))
    return mk("regla", nivel, enun, pasos, f"{hyp_plain(tail, 'mu', mu0)}; t = {t:.2f}; valor critico = {'+-' if tail == 'two' else ('' if tail == 'right' else '-')}{c:.3f}; {'se rechaza H0' if rej else 'no se rechaza H0'}",
              [r"t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}", r"gl=n-1"])


# =========================================================================== PRUEBA DE HIPÓTESIS (t y proporción)
def gen_ph_prop(rng, nivel):
    subj, unidad = rng.choice(CTX_P)
    p0 = rng.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6])
    tail = rng.choice(["right", "left"]) if nivel == "Fácil" else rng.choice(["right", "left", "two"])
    alpha = 0.05 if nivel == "Fácil" else rng.choice([0.05, 0.01])
    n = rng.choice([100, 150, 200, 250, 400])
    se = math.sqrt(p0 * (1 - p0) / n)
    zt = rng.uniform(0.5, 3.0) * (1 if tail == "right" else -1 if tail == "left" else rng.choice([-1, 1]))
    x = max(1, min(n - 1, round(n * (p0 + zt * se))))
    ph = x / n
    z = (ph - p0) / se
    verbo = {"right": "ha aumentado", "left": "ha disminuido", "two": "es diferente"}[tail]
    enun = (f"Históricamente {subj} es {g(p0 * 100)}%. Se sospecha que {verbo} respecto a ese valor. En una muestra aleatoria de {n} {unidad}, {x} cumplieron la característica. "
            f"Pruebe la hipótesis con alfa = {g(alpha, 2)}.")
    pasos = [("Hipótesis sobre la proporción poblacional.", hyp_latex(tail, "p", p0)),
             ("Condiciones para usar la normal: n por p0 y n por (1 - p0) deben ser al menos 5.",
              rf"n\,p_0={n}({g(p0, 2)})={n * p0:.1f}\geq 5\qquad n(1-p_0)={n}({g(1 - p0, 2)})={n * (1 - p0):.1f}\geq 5")]
    cs, c = crit_steps(tail, alpha, "z")
    pasos += [("Nivel de significancia y valor crítico.", None)] + cs
    pasos += [("Proporción muestral.", rf"\hat{{p}}=\frac{{x}}{{n}}=\frac{{{x}}}{{{n}}}={ph:.4f}"),
              ("Error estándar (se calcula con p0, el valor de H0).", rf"\sqrt{{\frac{{p_0(1-p_0)}}{{n}}}}=\sqrt{{\frac{{{g(p0, 2)}({g(1 - p0, 2)})}}{{{n}}}}}={se:.4f}"),
              ("Estadístico Z.", rf"z_c=\frac{{\hat{{p}}-p_0}}{{\sqrt{{p_0(1-p_0)/n}}}}=\frac{{{ph:.4f}-{g(p0, 2)}}}{{{se:.4f}}}={z:.2f}")]
    rej, ds = decide(tail, z, c, "z")
    pasos += ds + [conclusion(rej, alpha, f"{subj} {verbo} respecto a {g(p0 * 100)}%")]
    return mk("ph2", nivel, enun, pasos, f"{hyp_plain(tail, 'p', p0)}; z = {z:.2f}; {'se rechaza H0' if rej else 'no se rechaza H0'}",
              [r"\hat{p}=\frac{x}{n}", r"Z=\frac{\hat{p}-p_0}{\sqrt{p_0(1-p_0)/n}}"])


def gen_ph_t(rng, nivel):
    subj, unit, mu0, s0 = ctx_mean(rng)
    tail = rng.choice(["right", "left", "two"])
    alpha = rng.choice([0.05, 0.01, 0.10])
    if nivel == "Difícil":
        n = rng.choice([6, 7, 8])
        datos, xbar, ss, s = data_stats(rng, mu0 * (1 + rng.choice([-0.05, 0, 0.05])), max(s0, 3), n)
        stats_txt = f"Se registraron {n} mediciones ({unit}): {', '.join(map(str, datos))}."
        previo = [("Estadísticos de la muestra.", rf"\bar{{x}}=\frac{{{sum(datos)}}}{{{n}}}={xbar:.4f}\qquad s=\sqrt{{\frac{{{ss:.4f}}}{{{n}-1}}}}={s:.4f}")]
    else:
        n = rng.choice([9, 12, 16, 20, 25])
        se0 = s0 / math.sqrt(n)
        zt = rng.uniform(0.6, 3.2) * (1 if tail == "right" else -1 if tail == "left" else rng.choice([-1, 1]))
        xbar, s = round(mu0 + zt * se0, 2), s0
        stats_txt = f"Con n = {n}, la muestra dio media {g(xbar)} {unit} y desviación estándar s = {g(s)} {unit}."
        previo = []
    gl = n - 1
    se = s / math.sqrt(n)
    t = (xbar - mu0) / se
    enun = (f"{sospecha(tail, subj, mu0, unit)} {stats_txt} Suponga población aproximadamente normal. Pruebe la hipótesis con alfa = {g(alpha, 2)}.")
    pasos = [("Etapa 1 · Hipótesis.", hyp_latex(tail, r"\mu", mu0))] + previo
    cs, c = crit_steps(tail, alpha, "t", gl)
    pasos += [("Etapa 2 · Como sigma es desconocida se usa t con n - 1 grados de libertad.", rf"gl={n}-1={gl}")] + cs
    pasos += [("Etapa 3 · Estadístico t.", rf"t_c=\frac{{\bar{{x}}-\mu_0}}{{s/\sqrt{{n}}}}=\frac{{{xbar:.4f}-{g(mu0)}}}{{{s:.4f}/\sqrt{{{n}}}}}=\frac{{{xbar - mu0:.4f}}}{{{se:.4f}}}={t:.2f}")]
    rej, ds = decide(tail, t, c, "t")
    pasos += [("Etapas 4 y 5 · Decisión y conclusión.", None)] + ds + [conclusion(rej, alpha, h1_words(tail, subj, mu0, unit))]
    return mk("ph2", nivel, enun, pasos, f"{hyp_plain(tail, 'mu', mu0)}; t = {t:.2f}; valor critico = {'+-' if tail == 'two' else ('' if tail == 'right' else '-')}{c:.3f}; {'se rechaza H0' if rej else 'no se rechaza H0'}",
              [r"t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}", r"gl=n-1"])

"""gen_c1.py · Generadores del PRIMER CORTE: normal, discretas, binomial y prueba de hipótesis (z)."""

from __future__ import annotations

import math

from scipy.stats import binom, norm

from pbase import (CTX_N, N_CUADRADO, crit_steps, ctx_mean, decide, conclusion, g, h1_words, hyp_latex,
                   hyp_plain, mk, phi, sospecha, zcrit, TAIL_TXT)

# =========================================================================== NORMAL
def _ctx_n(rng):
    desc, unit, mr, sr = rng.choice(CTX_N)
    return desc, unit, rng.randint(*mr), rng.randint(*sr)


def gen_normal_prob(rng, nivel):
    desc, unit, mu, sigma = _ctx_n(rng)
    if nivel == "Fácil":
        kind = rng.choice(["lt", "gt"])
        zs = [rng.choice([-1.5, -1, -0.5, 0.5, 1, 1.5, 2])]
    elif nivel == "Medio":
        kind = rng.choice(["lt", "gt", "between"])
        zs = sorted(rng.sample([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2], 2)) if kind == "between" else [rng.choice([-1.5, -1, 0.5, 1, 1.5, 2])]
    else:
        kind = rng.choice(["between", "tails"])
        zs = sorted(rng.sample([round(rng.uniform(-2.4, 2.4), 2) for _ in range(6)], 2))
        if zs[0] == zs[1]:
            zs[1] += 0.5
    xs = [round(mu + z * sigma) if nivel == "Difícil" else mu + z * sigma for z in zs]
    zr = [round((x - mu) / sigma, 2) for x in xs]
    nm = f"{g(mu)}, {g(sigma)}"
    pasos = [(f"Identifica la distribución. X = {desc} (en {unit}) es normal con media {g(mu)} y desviación estándar {g(sigma)}.",
              rf"X\sim N(\mu={g(mu)},\ \sigma={g(sigma)})")]
    for i, (x, z) in enumerate(zip(xs, zr)):
        nombre = "" if len(xs) == 1 else (" inferior" if i == 0 else " superior")
        pasos.append((f"Estandariza el valor{nombre}: restamos la media y dividimos entre la desviación estándar.",
                      rf"z=\frac{{x-\mu}}{{\sigma}}=\frac{{{g(x)}-{g(mu)}}}{{{g(sigma)}}}={z:.2f}"))
    if kind == "lt":
        x = xs[0]
        p = phi(zr[0])
        enun = f"Suponga que {desc} sigue una distribución normal con media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. Calcule la probabilidad de que el valor sea menor que {g(x)} {unit}."
        pasos.append(("La tabla Z entrega directamente el área a la izquierda de z.", rf"P(X<{g(x)})=P(Z<{zr[0]:.2f})=\Phi({zr[0]:.2f})={p:.4f}"))
        resp = f"P(X < {g(x)}) = {p:.4f} (aprox. {p * 100:.2f}%)"
    elif kind == "gt":
        x = xs[0]
        p = 1 - phi(zr[0])
        enun = f"Suponga que {desc} sigue una distribución normal con media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. Calcule la probabilidad de que el valor sea mayor que {g(x)} {unit}."
        pasos.append((f"La tabla da el área a la izquierda; el área a la derecha es su complemento.",
                      rf"P(X>{g(x)})=P(Z>{zr[0]:.2f})=1-\Phi({zr[0]:.2f})=1-{phi(zr[0]):.4f}={p:.4f}"))
        resp = f"P(X > {g(x)}) = {p:.4f} (aprox. {p * 100:.2f}%)"
    elif kind == "between":
        p = phi(zr[1]) - phi(zr[0])
        enun = f"Suponga que {desc} sigue una distribución normal con media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. Calcule la probabilidad de que el valor esté entre {g(xs[0])} y {g(xs[1])} {unit}."
        pasos.append(("Para el área entre dos valores se resta el área acumulada del menor al área acumulada del mayor.",
                      rf"P({g(xs[0])}<X<{g(xs[1])})=\Phi({zr[1]:.2f})-\Phi({zr[0]:.2f})={phi(zr[1]):.4f}-{phi(zr[0]):.4f}={p:.4f}"))
        resp = f"P({g(xs[0])} < X < {g(xs[1])}) = {p:.4f} (aprox. {p * 100:.2f}%)"
    else:
        p = phi(zr[0]) + 1 - phi(zr[1])
        enun = f"Suponga que {desc} sigue una distribución normal con media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. Calcule la probabilidad de que el valor sea menor que {g(xs[0])} o mayor que {g(xs[1])} {unit}."
        pasos.append(("Son dos colas separadas: se suma el área de la cola izquierda y la de la cola derecha.",
                      rf"P(X<{g(xs[0])})+P(X>{g(xs[1])})=\Phi({zr[0]:.2f})+[1-\Phi({zr[1]:.2f})]={phi(zr[0]):.4f}+{1 - phi(zr[1]):.4f}={p:.4f}"))
        resp = f"P(X < {g(xs[0])}) + P(X > {g(xs[1])}) = {p:.4f} (aprox. {p * 100:.2f}%)"
    pasos.append(("Interpretación: esa proporción de la población cumple la condición pedida.", None))
    fs = [r"Z=\frac{X-\mu}{\sigma}", r"P(Z>z)=1-\Phi(z)", r"P(a<X<b)=\Phi(z_b)-\Phi(z_a)"]
    return mk("normal", nivel, enun, pasos, resp, fs)


def gen_normal_inv(rng, nivel):
    desc, unit, mu, sigma = _ctx_n(rng)
    zt = {0.80: 0.84, 0.75: 0.67, 0.90: 1.28, 0.975: 1.96, 0.99: 2.33, 0.25: -0.67, 0.10: -1.28, 0.60: 0.25}
    area = rng.choice(list(zt))
    z = zt[area]
    x = mu + z * sigma
    base = f"Suponga que {desc} sigue una distribución normal con media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}."
    if nivel == "Difícil" and area >= 0.75:
        sup = round((1 - area) * 100, 1)
        enun = f"{base} Un programa premia al {g(sup)}% con los valores más altos. ¿Desde qué valor se obtiene el premio?"
        pasos = [("El {0}% superior deja {1} de área a su derecha, así que el área a su izquierda es 1 menos ese valor.".format(g(sup), g(1 - area, 3)),
                  rf"\mathrm{{Area\ izquierda}}=1-{g(1 - area, 3)}={g(area, 3)}")]
    else:
        enun = f"{base} Encuentre el valor x tal que la probabilidad de estar por debajo de x sea {g(area, 3)}."
        pasos = [(f"Se conoce el área a la izquierda: {g(area, 3)}.", rf"P(X<x)={g(area, 3)}")]
    pasos += [("Se busca en el cuerpo de la tabla Z el área más cercana y se lee el z correspondiente.", rf"\Phi(z)={g(area, 3)}\ \Rightarrow\ z={z:.2f}"),
              ("Se 'des-estandariza' con x = media + z por desviación estándar.", rf"x=\mu+z\,\sigma={g(mu)}+({z:.2f})({g(sigma)})={g(x, 2)}"),
              ("Comprobación: el valor está por encima de la media si z es positivo y por debajo si es negativo.", None)]
    return mk("normal", nivel, enun, pasos, f"x = {g(x, 2)} {unit}", [r"x=\mu+z\,\sigma"])


def gen_normal_se(rng, nivel):
    desc, unit, mu, sigma = _ctx_n(rng)
    n = rng.choice(N_CUADRADO)
    se = sigma / math.sqrt(n)
    enun = (f"{desc[0].upper() + desc[1:]} en una población tiene media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. "
            f"Se toman muestras aleatorias de tamaño n = {n}. (a) ¿Cuál es la media y el error estándar de la media muestral? "
            f"(b) ¿Qué le pasa al error estándar si el tamaño de muestra se cuadruplica?")
    se4 = sigma / math.sqrt(4 * n)
    pasos = [("La media de todas las medias muestrales coincide con la media poblacional.", rf"\mu_{{\bar{{x}}}}=\mu={g(mu)}"),
             ("El error estándar es la desviación estándar de la media muestral: la desviación poblacional dividida entre la raíz del tamaño de muestra.",
              rf"\sigma_{{\bar{{x}}}}=\frac{{\sigma}}{{\sqrt{{n}}}}=\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
             ("Con muestra 4 veces mayor, la raíz de n se duplica, entonces el error estándar se reduce a la mitad.",
              rf"\frac{{{g(sigma)}}}{{\sqrt{{{4 * n}}}}}={se4:.4f}"),
             ("Idea clave: parámetro = valor de la población (mu, sigma); estadístico = valor de la muestra (x barra, s). Más datos, promedios más estables.", None)]
    return mk("normal", nivel, enun, pasos, f"Media = {g(mu)}; error estándar = {se:.4f}; con 4n queda {se4:.4f} (la mitad).",
              [r"\sigma_{\bar{x}}=\frac{\sigma}{\sqrt{n}}"])


def gen_normal_xbar(rng, nivel):
    desc, unit, mu, sigma = _ctx_n(rng)
    n = rng.choice([25, 36, 49, 64] if nivel == "Difícil" else [16, 25, 36])
    se = sigma / math.sqrt(n)
    k = round(rng.uniform(-2.4, 2.4), 1)
    a = round(mu + k * se, 2)
    z = round((a - mu) / se, 2)
    kind = rng.choice(["gt", "lt"])
    tlc = nivel == "Difícil"
    forma = ("No se conoce la forma de la distribución poblacional" if tlc else f"La población es normal")
    enun = (f"{desc[0].upper() + desc[1:]} tiene media {g(mu)} {unit} y desviación estándar {g(sigma)} {unit}. {forma}. "
            f"Se toma una muestra aleatoria de n = {n}. ¿Cuál es la probabilidad de que la media muestral sea "
            f"{'mayor' if kind == 'gt' else 'menor'} que {g(a)} {unit}?")
    p = 1 - phi(z) if kind == "gt" else phi(z)
    t1 = (f"Como n = {n} es mayor o igual a 30, el Teorema del Límite Central garantiza que la media muestral es aproximadamente normal."
          if tlc and n >= 30 else
          ("Aunque no se conoce la forma, n es grande; con n = 25 se acepta la aproximación normal solo con cautela."
           if tlc else "Como la población es normal, la media muestral también es normal para cualquier n."))
    pasos = [(t1, rf"\bar{{x}}\sim N\left(\mu,\ \frac{{\sigma}}{{\sqrt{{n}}}}\right)"),
             ("Calcula el error estándar.", rf"\sigma_{{\bar{{x}}}}=\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
             ("Estandariza usando la media y el error estándar (no la desviación de un solo dato).",
              rf"z=\frac{{\bar{{x}}-\mu}}{{\sigma/\sqrt{{n}}}}=\frac{{{g(a)}-{g(mu)}}}{{{se:.4f}}}={z:.2f}")]
    if kind == "gt":
        pasos.append(("Área a la derecha = 1 menos el área a la izquierda.", rf"P(\bar{{x}}>{g(a)})=1-\Phi({z:.2f})={p:.4f}"))
        resp = f"P(media muestral > {g(a)}) = {p:.4f}"
    else:
        pasos.append(("Área a la izquierda directamente de la tabla.", rf"P(\bar{{x}}<{g(a)})=\Phi({z:.2f})={p:.4f}"))
        resp = f"P(media muestral < {g(a)}) = {p:.4f}"
    return mk("normal", nivel, enun, pasos, resp, [r"Z=\frac{\bar{x}-\mu}{\sigma/\sqrt{n}}", r"P(Z>z)=1-\Phi(z)"])


# =========================================================================== DISCRETAS
def _probs(rng, m):
    cuts = sorted(rng.sample(range(1, 20), m - 1))
    return [(b - a) / 20 for a, b in zip([0] + cuts, cuts + [20])]


def _tabla(xs, ps, falta=None, lab="X"):
    fila_p = ["k" if i == falta else f"{p:.2f}" for i, p in enumerate(ps)]
    return [[lab] + [g(x) for x in xs], ["p(x)"] + fila_p]


def gen_disc_esperanza(rng, nivel):
    xs = rng.choice([[0, 1, 2, 3], [1, 2, 3, 4], [0, 1, 2, 3, 4]])
    ps = _probs(rng, len(xs))
    ex = sum(x * p for x, p in zip(xs, ps))
    a = xs[len(xs) // 2]
    pa = sum(p for x, p in zip(xs, ps) if x >= a)
    enun = (f"La variable aleatoria X (número de servicios solicitados por un cliente) tiene la distribución de probabilidad de la tabla. "
            f"(a) Verifique que es una distribución válida. (b) Calcule E(X). (c) Calcule P(X >= {g(a)}).")
    terms = "+".join(f"({g(x)})({p:.2f})" for x, p in zip(xs, ps))
    pasos = [("Una distribución es válida si todas las probabilidades están entre 0 y 1 y suman 1.",
              rf"\sum p(x)={'+'.join(f'{p:.2f}' for p in ps)}={sum(ps):.2f}"),
             ("La esperanza es el promedio ponderado: cada valor por su probabilidad, sumado.", rf"E(X)=\sum x\,p(x)={terms}"),
             ("Se suman los productos.", rf"E(X)={ex:.2f}"),
             (f"P(X >= {g(a)}) suma las probabilidades de los valores desde {g(a)} en adelante.",
              rf"P(X\geq {g(a)})={'+'.join(f'{p:.2f}' for x, p in zip(xs, ps) if x >= a)}={pa:.2f}")]
    return mk("discretas", nivel, enun, pasos, f"Es válida (suma 1). E(X) = {ex:.2f}. P(X >= {g(a)}) = {pa:.2f}",
              [r"\sum p(x)=1", r"E(X)=\sum x\cdot p(x)"], tabla=_tabla(xs, ps))


def gen_disc_k(rng, nivel):
    xs = rng.choice([[0, 1, 2, 3], [1, 2, 3, 4, 5], [0, 1, 2, 3, 4]])
    ps = _probs(rng, len(xs))
    i = rng.randrange(len(xs))
    otros = sum(p for j, p in enumerate(ps) if j != i)
    ex = sum(x * p for x, p in zip(xs, ps))
    ex2 = sum(x * x * p for x, p in zip(xs, ps))
    var = ex2 - ex ** 2
    medio = nivel == "Medio"
    enun = (f"X es una variable aleatoria discreta con la distribución de la tabla. Halle el valor de k, "
            + ("y luego calcule E(X), V(X) y la desviación estándar." if medio else "y luego calcule P(X <= " + g(xs[1]) + ")."))
    pasos = [("Las probabilidades deben sumar 1, así que k es lo que falta para llegar a 1.",
              rf"k=1-({'+'.join(f'{p:.2f}' for j, p in enumerate(ps) if j != i)})=1-{otros:.2f}={ps[i]:.2f}")]
    if medio:
        pasos += [("Esperanza: cada valor por su probabilidad.", rf"E(X)=\sum x\,p(x)={'+'.join(f'({g(x)})({p:.2f})' for x, p in zip(xs, ps))}={ex:.2f}"),
                  ("Para la varianza se necesita primero E(X al cuadrado).", rf"E(X^2)=\sum x^2\,p(x)={'+'.join(f'({g(x)})^2({p:.2f})' for x, p in zip(xs, ps))}={ex2:.2f}"),
                  ("Varianza = E(X al cuadrado) menos el cuadrado de la media.", rf"V(X)=E(X^2)-\mu^2={ex2:.2f}-({ex:.2f})^2={var:.4f}"),
                  ("La desviación estándar es la raíz de la varianza (mismas unidades que X).", rf"\sigma=\sqrt{{{var:.4f}}}={math.sqrt(var):.4f}")]
        resp = f"k = {ps[i]:.2f}; E(X) = {ex:.2f}; V(X) = {var:.4f}; desviacion estandar = {math.sqrt(var):.4f}"
    else:
        lim = xs[1]
        pl = sum(p for x, p in zip(xs, ps) if x <= lim)
        pasos.append((f"P(X <= {g(lim)}) suma las probabilidades de los valores hasta {g(lim)}.",
                      rf"P(X\leq {g(lim)})={'+'.join(f'{p:.2f}' for x, p in zip(xs, ps) if x <= lim)}={pl:.2f}"))
        resp = f"k = {ps[i]:.2f}; P(X <= {g(lim)}) = {pl:.2f}"
    return mk("discretas", nivel, enun, pasos, resp, [r"\sum p(x)=1", r"E(X)=\sum x\,p(x)", r"V(X)=E(X^2)-\mu^2"],
              tabla=_tabla(xs, ps, falta=i))


def gen_disc_lineal(rng, nivel):
    xs = rng.choice([[-1, 0, 1, 2, 3], [0, 1, 2, 3, 4], [10, 20, 30, 40]])
    ps = _probs(rng, len(xs))
    i = rng.randrange(len(xs))
    otros = sum(p for j, p in enumerate(ps) if j != i)
    ex = sum(x * p for x, p in zip(xs, ps))
    ex2 = sum(x * x * p for x, p in zip(xs, ps))
    var = ex2 - ex ** 2
    a, b = rng.choice([2, 3, 4, 5]), rng.choice([-5, -2, 3, 10])
    ey, vy = a * ex + b, a * a * var
    enun = (f"X es una variable aleatoria discreta con la distribución de la tabla. (a) Halle k. (b) Calcule E(X), V(X) y la desviación estándar. "
            f"(c) Si Y = {a}X {'+' if b > 0 else '-'} {abs(b)}, calcule E(Y) y V(Y).")
    pasos = [("Las probabilidades suman 1.", rf"k=1-{otros:.2f}={ps[i]:.2f}"),
             ("Esperanza de X.", rf"E(X)=\sum x\,p(x)={ex:.4f}"),
             ("Se calcula E(X al cuadrado).", rf"E(X^2)=\sum x^2\,p(x)={ex2:.4f}"),
             ("Varianza y desviación estándar de X.", rf"V(X)={ex2:.4f}-({ex:.4f})^2={var:.4f}\qquad \sigma={math.sqrt(var):.4f}"),
             ("Para Y = aX + b la esperanza se transforma igual que los datos.", rf"E(Y)={a}E(X){'+' if b > 0 else '-'}{abs(b)}={a}({ex:.4f}){'+' if b > 0 else '-'}{abs(b)}={ey:.4f}"),
             ("La varianza solo cambia con el factor a al cuadrado: sumar la constante b no altera la dispersión.", rf"V(Y)=a^2\,V(X)={a}^2({var:.4f})={vy:.4f}")]
    return mk("discretas", nivel, enun, pasos,
              f"k = {ps[i]:.2f}; E(X) = {ex:.4f}; V(X) = {var:.4f}; sigma = {math.sqrt(var):.4f}; E(Y) = {ey:.4f}; V(Y) = {vy:.4f}",
              [r"E(aX+b)=aE(X)+b", r"V(aX+b)=a^2\,V(X)"], tabla=_tabla(xs, ps, falta=i))


# =========================================================================== BINOMIAL
CTX_B = [
    ("Cada pieza de una fábrica sale defectuosa con probabilidad {p}. Se inspeccionan {n} piezas.", "piezas defectuosas"),
    ("La probabilidad de que un cliente pague con tarjeta es {p}. Llegan {n} clientes a una caja.", "clientes que pagan con tarjeta"),
    ("Un estudiante acierta cada pregunta de un quiz con probabilidad {p}. El quiz tiene {n} preguntas.", "preguntas acertadas"),
    ("La probabilidad de que un paquete llegue a tiempo es {p}. Se envían {n} paquetes.", "paquetes que llegan a tiempo"),
]


def _bin_ctx(rng, n, p):
    txt, exito = rng.choice(CTX_B)
    return txt.format(p=g(p, 2), n=n), exito


def _bin_term(n, k, p):
    return (rf"P(X={k})=\binom{{{n}}}{{{k}}}({g(p, 2)})^{{{k}}}({g(1 - p, 2)})^{{{n - k}}}={binom.pmf(k, n, p):.4f}")


def gen_bin_exact(rng, nivel):
    n = rng.randint(5, 10)
    p = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    k = rng.randint(1, n - 1)
    ctx, exito = _bin_ctx(rng, n, p)
    c, pk, qk = math.comb(n, k), p ** k, (1 - p) ** (n - k)
    enun = f"{ctx} Sea X el número de {exito}. ¿Cuál es la probabilidad de que X sea exactamente {k}?"
    pasos = [("Se verifican las condiciones binomiales: n ensayos fijos, dos resultados, probabilidad constante e independencia.",
              rf"X\sim B(n={n},\ p={g(p, 2)})"),
             ("Se escribe la fórmula de la binomial con k éxitos.", rf"P(X=k)=\binom{{n}}{{k}}\,p^{{k}}(1-p)^{{n-k}}"),
             (f"Se calcula el número de combinaciones: formas de elegir cuáles {k} de los {n} ensayos son éxito.",
              rf"\binom{{{n}}}{{{k}}}=\frac{{{n}!}}{{{k}!\,{n - k}!}}={c}"),
             ("Se calculan las potencias.", rf"p^{{k}}=({g(p, 2)})^{{{k}}}={pk:.6f}\qquad (1-p)^{{n-k}}=({g(1 - p, 2)})^{{{n - k}}}={qk:.6f}"),
             ("Se multiplican las tres partes.", rf"P(X={k})={c}\times{pk:.6f}\times{qk:.6f}={binom.pmf(k, n, p):.4f}")]
    return mk("binomial", nivel, enun, pasos, f"P(X = {k}) = {binom.pmf(k, n, p):.4f}",
              [r"P(X=k)=\binom{n}{k}\,p^{k}(1-p)^{n-k}"])


def gen_bin_cum(rng, nivel):
    n = rng.randint(6, 10)
    p = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ctx, exito = _bin_ctx(rng, n, p)
    kind = rng.choice(["max", "min", "between"])
    if kind == "max":
        k = rng.randint(1, 3)
        ks, txt, expr, plain = list(range(0, k + 1)), f"a lo sumo {k}", rf"P(X\leq {k})", f"P(X <= {k})"
    elif kind == "min":
        k = rng.randint(n - 2, n)
        ks, txt, expr, plain = list(range(k, n + 1)), f"al menos {k}", rf"P(X\geq {k})", f"P(X >= {k})"
    else:
        a = rng.randint(1, 3)
        b = a + 2
        ks, txt, expr, plain = list(range(a, b + 1)), f"entre {a} y {b} (inclusive)", rf"P({a}\leq X\leq {b})", f"P({a} <= X <= {b})"
    total = sum(binom.pmf(i, n, p) for i in ks)
    enun = f"{ctx} Sea X el número de {exito}. ¿Cuál es la probabilidad de que haya {txt}?"
    pasos = [("Se identifica el modelo y se traduce la frase a una desigualdad.", rf"X\sim B({n},\ {g(p, 2)})\qquad \mathrm{{Pedido:}}\ {expr}"),
             (f"La probabilidad pedida es la suma de las probabilidades exactas de X = {', '.join(map(str, ks))}.", None)]
    for i in ks:
        pasos.append((f"Término para X = {i}:", _bin_term(n, i, p)))
    if len(ks) == 1:
        pasos.append(("Solo hay un término, así que ese es el resultado.", rf"{expr}={total:.4f}"))
    else:
        pasos.append(("Se suman los términos (pequeñas diferencias de redondeo en el cuarto decimal son normales).",
                      rf"{expr}={'+'.join(f'{binom.pmf(i, n, p):.4f}' for i in ks)}={total:.4f}"))
    return mk("binomial", nivel, enun, pasos, f"{plain} = {total:.4f}",
              [r"P(X=k)=\binom{n}{k}\,p^{k}(1-p)^{n-k}"])


def gen_bin_hard(rng, nivel):
    n = rng.randint(10, 15)
    p = rng.choice([0.1, 0.2, 0.25, 0.3, 0.4])
    ctx, exito = _bin_ctx(rng, n, p)
    k = rng.randint(2, 3)
    mean, var = n * p, n * p * (1 - p)
    comp = sum(binom.pmf(i, n, p) for i in range(k))
    ans = 1 - comp
    enun = (f"{ctx} Sea X el número de {exito}. (a) Calcule el número esperado de {exito} y la desviación estándar de X. "
            f"(b) Calcule la probabilidad de que haya al menos {k}.")
    pasos = [("Se define el modelo.", rf"X\sim B({n},\ {g(p, 2)})"),
             ("Media de una binomial: n por p.", rf"E(X)=np={n}({g(p, 2)})={mean:.2f}"),
             ("Varianza: n por p por q; la desviación estándar es su raíz.", rf"V(X)=np(1-p)={n}({g(p, 2)})({g(1 - p, 2)})={var:.4f}\qquad \sigma=\sqrt{{{var:.4f}}}={math.sqrt(var):.4f}"),
             (f"Para (b), sumar desde {k} hasta {n} sería largo; es más corto usar el complemento.", rf"P(X\geq {k})=1-P(X\leq {k - 1})")]
    for i in range(k):
        pasos.append((f"Término para X = {i}:", _bin_term(n, i, p)))
    pasos.append(("Se suman los términos y se restan de 1.", rf"P(X\geq {k})=1-({'+'.join(f'{binom.pmf(i, n, p):.4f}' for i in range(k))})=1-{comp:.4f}={ans:.4f}"))
    return mk("binomial", nivel, enun, pasos,
              f"E(X) = {mean:.2f}; sigma = {math.sqrt(var):.4f}; P(X >= {k}) = {ans:.4f}",
              [r"E(X)=np", r"V(X)=np(1-p)", r"P(X\geq k)=1-P(X\leq k-1)"])


# =========================================================================== PRUEBA DE HIPÓTESIS (z, corte 1)
def gen_ph1_errores(rng, nivel):
    subj, unit, mu0, _ = ctx_mean(rng)
    casos = [("Se rechaza H0 y en realidad H0 era verdadera.", "Error tipo I",
              "Se rechazó una hipótesis que era cierta: es el error que controla el nivel de significancia (alfa)."),
             ("No se rechaza H0 y en realidad H0 era falsa.", "Error tipo II",
              "No se detectó un cambio que sí existía: su probabilidad es beta."),
             ("Se rechaza H0 y en realidad H0 era falsa.", "Decisión correcta (con probabilidad 1 - beta, la potencia)",
              "Se detectó un cambio real."),
             ("No se rechaza H0 y en realidad H0 era verdadera.", "Decisión correcta (con probabilidad 1 - alfa)",
              "No se encontró evidencia de cambio y realmente no lo había.")]
    caso = rng.choice(casos)
    enun = (f"Se prueba H0: {subj} es {g(mu0)} {unit} (no ha cambiado) contra H1: ha cambiado. "
            f"Al terminar el estudio ocurre lo siguiente: {caso[0]} Clasifique este resultado.")
    pasos = [("Hay dos realidades posibles (H0 verdadera o falsa) y dos decisiones posibles (rechazar o no rechazar H0): cuatro combinaciones.",
              r"\alpha=P(\mathrm{rechazar}\ H_0\mid H_0\ \mathrm{verdadera})\qquad \beta=P(\mathrm{no\ rechazar}\ H_0\mid H_0\ \mathrm{falsa})"),
             (f"Se ubica el caso descrito: {caso[0]}", None),
             (caso[2], None)]
    return mk("ph1", nivel, enun, pasos, caso[1], [r"\alpha=P(\mathrm{error\ tipo\ I})", r"\beta=P(\mathrm{error\ tipo\ II})"])


def gen_ph1_z(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    tails = ["right", "left"] if nivel == "Fácil" else ["right", "left", "two"]
    tail = rng.choice(tails)
    alpha = 0.05 if nivel == "Fácil" else rng.choice([0.05, 0.01, 0.10])
    n = rng.choice(N_CUADRADO)
    se = sigma / math.sqrt(n)
    if tail == "two":
        zt = rng.choice([-1, 1]) * rng.uniform(0.3, 3.0)
    else:
        zt = (1 if tail == "right" else -1) * rng.uniform(-0.5, 3.0)
    xbar = round(mu0 + zt * se, 2)
    z = (xbar - mu0) / se
    enun = (f"{sospecha(tail, subj, mu0, unit)} Una muestra aleatoria de n = {n} observaciones dio una media de {g(xbar)} {unit}. "
            f"Se sabe que la desviación estándar poblacional es {g(sigma)} {unit}. Pruebe la hipótesis con un nivel de significancia de {g(alpha, 2)}.")
    pasos = [("Etapa 1 · Hipótesis. Lo que se sospecha va en H1; H0 lleva la igualdad.", hyp_latex(tail, r"\mu", mu0)),
             (f"La prueba es de {TAIL_TXT[tail]} porque H1 usa el signo {'>' if tail == 'right' else '<' if tail == 'left' else 'diferente de'}.", None)]
    cs, c = crit_steps(tail, alpha, "z")
    pasos += [("Etapa 2 · Nivel de significancia y valor crítico.", None)] + cs
    pasos += [("Etapa 3 · Estadístico de prueba. Como se conoce sigma, se usa Z. Primero el error estándar:", rf"\frac{{\sigma}}{{\sqrt{{n}}}}=\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}={se:.4f}"),
              ("Ahora el estadístico:", rf"z_c=\frac{{\bar{{x}}-\mu_0}}{{\sigma/\sqrt{{n}}}}=\frac{{{g(xbar)}-{g(mu0)}}}{{{se:.4f}}}={z:.2f}"),
              ("Etapa 4 · Regla de decisión y decisión.", None)]
    rej, ds = decide(tail, z, c, "z")
    pasos += ds + [("Etapa 5 · " + conclusion(rej, alpha, h1_words(tail, subj, mu0, unit))[0], None)]
    resp = f"{hyp_plain(tail, 'mu', mu0)}; z = {z:.2f}; valor critico = {'+-' if tail == 'two' else ('' if tail == 'right' else '-')}{c:.3f}; {'se rechaza H0' if rej else 'no se rechaza H0'}"
    return mk("ph1", nivel, enun, pasos, resp, [r"Z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}", r"z_{\alpha}\ \mathrm{o}\ z_{\alpha/2}"])


def gen_ph1_beta(rng, nivel):
    subj, unit, mu0, sigma = ctx_mean(rng)
    n = rng.choice([25, 36, 49, 64])
    alpha = rng.choice([0.05, 0.01])
    se = sigma / math.sqrt(n)
    mu1 = round(mu0 + rng.choice([0.5, 1.0, 1.5]) * se, 1)
    zc = zcrit(alpha)
    c = round(mu0 + zc * se, 2)
    zb = round((c - mu1) / se, 2)
    beta = phi(zb)
    enun = (f"Se prueba H0: {subj} es {g(mu0)} {unit} contra H1: es mayor que {g(mu0)} {unit}, con sigma = {g(sigma)} {unit}, "
            f"n = {n} y alfa = {g(alpha, 2)}. (a) Halle el valor de la media muestral a partir del cual se rechaza H0. "
            f"(b) Si en realidad la media es {g(mu1)} {unit}, calcule la probabilidad de error tipo II (beta) y la potencia.")
    pasos = [("Se busca el valor crítico z que deja alfa en la cola derecha.", rf"z_{{{g(alpha, 2)}}}={zc:.3f}"),
             ("Se pasa el valor crítico a la escala de la media muestral: x barra crítica = mu0 + z por error estándar.",
              rf"\bar{{x}}_c=\mu_0+z_{{\alpha}}\frac{{\sigma}}{{\sqrt{{n}}}}={g(mu0)}+{zc:.3f}\left(\frac{{{g(sigma)}}}{{\sqrt{{{n}}}}}\right)={c:.2f}"),
             ("Se rechaza H0 cuando la media muestral supera ese valor. El error tipo II ocurre cuando NO se rechaza aunque la media real sea mayor, es decir, cuando la media muestral es menor o igual a ese valor.",
              rf"\beta=P(\bar{{x}}\leq {c:.2f}\mid \mu={g(mu1)})"),
             ("Se estandariza usando la media real.", rf"z=\frac{{{c:.2f}-{g(mu1)}}}{{{se:.4f}}}={zb:.2f}"),
             ("Se lee el área a la izquierda en la tabla Z.", rf"\beta=\Phi({zb:.2f})={beta:.4f}"),
             ("La potencia es la probabilidad de detectar el cambio real.", rf"1-\beta=1-{beta:.4f}={1 - beta:.4f}")]
    return mk("ph1", nivel, enun, pasos, f"x barra critica = {c:.2f}; beta = {beta:.4f}; potencia = {1 - beta:.4f}",
              [r"\bar{x}_c=\mu_0+z_{\alpha}\frac{\sigma}{\sqrt{n}}", r"\beta=P(\bar{x}\leq \bar{x}_c\mid \mu=\mu_1)"])

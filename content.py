"""
content.py · Temas, teoría y fórmulas del simulador de Estadística 2
--------------------------------------------------------------------
Para agregar o editar un tema basta con modificar el diccionario TOPICS.
Cada fórmula es (nombre, LaTeX, explicación corta). El LaTeX se dibuja en la app
con KaTeX y en el PDF con matplotlib (mathtext): evita \\text{} y usa \\mathrm{}.
"""

from __future__ import annotations

NIVELES = ["Fácil", "Medio", "Difícil"]

TOPICS: dict[str, dict] = {
    # ------------------------------------------------------------------ PRIMER CORTE
    "normal": {
        "corte": 1, "icono": "🔔", "nombre": "Repaso de la distribución normal (población y muestra)",
        "resumen": (
            "La **población** es el conjunto completo de interés y la **muestra** es una parte de ella. "
            "Un número calculado con la población es un **parámetro** (μ, σ); calculado con la muestra es un "
            "**estadístico** (x̄, s). Si X es normal, se **estandariza** para usar la tabla Z. "
            "Además, la media muestral x̄ tiene su propia distribución: su centro es μ y su dispersión (el "
            "**error estándar**) es σ/√n. Por el **Teorema del Límite Central**, con n grande (n ≥ 30) x̄ es "
            "aproximadamente normal aunque la población no lo sea."),
        "formulas": [
            ("Estandarización", r"Z=\frac{X-\mu}{\sigma}", "Convierte cualquier normal en la normal estándar N(0, 1)."),
            ("Complemento", r"P(Z>z)=1-P(Z\leq z)", "La tabla Z da áreas a la izquierda."),
            ("Entre dos valores", r"P(a<X<b)=\Phi(z_b)-\Phi(z_a)", "Se resta el área de la izquierda."),
            ("Valor a partir de un área", r"x=\mu+z\,\sigma", "Se busca z en la tabla y se 'des-estandariza'."),
            ("Error estándar de la media", r"\sigma_{\bar{x}}=\frac{\sigma}{\sqrt{n}}", "Es la desviación estándar de x̄."),
            ("Z para la media muestral", r"Z=\frac{\bar{x}-\mu}{\sigma/\sqrt{n}}", "Se usa cuando se pregunta por un promedio de n datos."),
        ],
        "tips": ["Dibuja la campana y sombrea el área que te piden antes de calcular.",
                 "Si preguntan por un **promedio de n datos**, divide σ entre √n.",
                 "z negativo = valor por debajo de la media; positivo = por encima."],
    },
    "discretas": {
        "corte": 1, "icono": "🎲", "nombre": "Distribuciones de probabilidad discreta",
        "resumen": (
            "Una variable aleatoria **discreta** toma valores contables. Su distribución es una tabla con cada "
            "valor x y su probabilidad p(x). Debe cumplir: 0 ≤ p(x) ≤ 1 y la suma de todas las p(x) es 1. "
            "La **esperanza** E(X) es el promedio ponderado (el valor esperado a largo plazo) y la **varianza** mide "
            "qué tan dispersos están los valores alrededor de E(X)."),
        "formulas": [
            ("Condición de probabilidad", r"\sum p(x)=1", "Todas las probabilidades suman 1."),
            ("Esperanza", r"E(X)=\mu=\sum x\cdot p(x)", "Cada valor multiplicado por su probabilidad."),
            ("Varianza (forma corta)", r"V(X)=E(X^2)-\mu^2", r"con E(X^2)=\sum x^2\,p(x)"),
            ("Desviación estándar", r"\sigma=\sqrt{V(X)}", "Está en las mismas unidades de X."),
            ("Transformación lineal", r"E(aX+b)=aE(X)+b \qquad V(aX+b)=a^2\,V(X)", "La constante b no cambia la varianza."),
        ],
        "tips": ["Si falta una probabilidad, se obtiene como 1 menos la suma de las demás.",
                 "Para P(X ≥ a) suma las probabilidades de los valores desde a en adelante.",
                 "La varianza nunca es negativa: si te da negativa, revisa E(X²)."],
    },
    "binomial": {
        "corte": 1, "icono": "🪙", "nombre": "Distribución binomial",
        "resumen": (
            "Cuenta los **éxitos** en n ensayos cuando: (1) hay un número fijo n de ensayos, (2) cada ensayo tiene solo "
            "dos resultados (éxito/fracaso), (3) la probabilidad de éxito p es la misma en todos, y (4) los ensayos son "
            "independientes. Se escribe X ~ B(n, p)."),
        "formulas": [
            ("Probabilidad exacta", r"P(X=k)=\binom{n}{k}\,p^{k}\,(1-p)^{n-k}", "k = número de éxitos."),
            ("Combinaciones", r"\binom{n}{k}=\frac{n!}{k!\,(n-k)!}", "Formas de elegir cuáles k ensayos son éxito."),
            ("Media", r"E(X)=n\,p", "Éxitos esperados."),
            ("Varianza", r"V(X)=n\,p\,(1-p)", "Dispersión del número de éxitos."),
            ("Complemento", r"P(X\geq k)=1-P(X\leq k-1)", "Ahorra términos cuando k es pequeño."),
        ],
        "tips": ["Define primero qué es 'éxito' (lo que te piden contar), aunque sea algo malo.",
                 "'Al menos' = ≥ ; 'a lo sumo' = ≤ ; 'exactamente' = =.",
                 "Para 'al menos 1' usa 1 − P(X = 0)."],
    },
    "ph1": {
        "corte": 1, "icono": "⚖️", "nombre": "Prueba de hipótesis (introducción: media con σ conocida)",
        "resumen": (
            "Una prueba de hipótesis decide, con datos de una muestra, si hay evidencia suficiente contra una afirmación "
            "sobre la población (H₀). Se fija un **nivel de significancia α** (probabilidad máxima de cometer el "
            "**error tipo I**), se calcula un **estadístico de prueba** y se compara con el/los **valores críticos**. "
            "Si el estadístico cae en la **región de rechazo**, se rechaza H₀."),
        "formulas": [
            ("Estadístico Z (σ conocida)", r"Z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}", "μ₀ es el valor de H₀."),
            ("Error tipo I", r"\alpha=P(\mathrm{rechazar}\ H_0\mid H_0\ \mathrm{verdadera})", "Rechazar algo que era cierto."),
            ("Error tipo II", r"\beta=P(\mathrm{no\ rechazar}\ H_0\mid H_0\ \mathrm{falsa})", "No detectar un cambio que sí existe."),
            ("Potencia", r"1-\beta", "Probabilidad de detectar un cambio real."),
        ],
        "tips": ["Nunca se 'acepta' H₀: se dice 'no hay evidencia suficiente para rechazarla'.",
                 "Menor α = más difícil rechazar H₀ = más riesgo de error tipo II.",
                 "Sigue siempre las 5 etapas: hipótesis, α, estadístico, regla y conclusión."],
    },
    # ------------------------------------------------------------------ SEGUNDO CORTE
    "ic": {
        "corte": 2, "icono": "📏", "nombre": "Intervalos de confianza (conceptos, margen de error y tamaño de muestra)",
        "resumen": (
            "Un **intervalo de confianza** es un rango de valores plausibles para un parámetro. El **nivel de confianza** "
            "(1 − α) indica el porcentaje de intervalos construidos con este método que contendrían al parámetro verdadero "
            "si se repitiera el muestreo muchas veces. **No** es la probabilidad de que el parámetro esté en un intervalo ya calculado."),
        "formulas": [
            ("Nivel de significancia", r"\alpha=1-\mathrm{confianza}", "Ej.: 95% de confianza → α = 0.05."),
            ("Valor crítico", r"z_{\alpha/2}", "Deja α/2 de área en cada cola (95% → 1.960)."),
            ("Margen de error (σ conocida)", r"E=z_{\alpha/2}\,\frac{\sigma}{\sqrt{n}}", "Mitad del ancho del intervalo."),
            ("Tamaño de muestra", r"n=\left(\frac{z_{\alpha/2}\,\sigma}{E}\right)^{2}", "Siempre se redondea hacia arriba."),
        ],
        "tips": ["Más confianza → intervalo más ancho. Más n → intervalo más angosto.",
                 "Para reducir el margen a la mitad necesitas **cuatro veces** la muestra.",
                 "Nunca digas 'hay 95% de probabilidad de que μ esté entre a y b'."],
    },
    "ic_media": {
        "corte": 2, "icono": "🎯", "nombre": "Intervalos de confianza para la media",
        "resumen": (
            "Si σ es **conocida** se usa la distribución normal (z). Si σ es **desconocida** se estima con la desviación "
            "estándar muestral s y se usa la distribución **t de Student** con n − 1 grados de libertad (más ancha que la "
            "normal para compensar la incertidumbre extra)."),
        "formulas": [
            ("IC con σ conocida", r"\bar{x}\pm z_{\alpha/2}\,\frac{\sigma}{\sqrt{n}}", "Distribución normal."),
            ("IC con σ desconocida", r"\bar{x}\pm t_{\alpha/2,\,n-1}\,\frac{s}{\sqrt{n}}", "Distribución t de Student."),
            ("Grados de libertad", r"gl=n-1", "Para una sola media."),
            ("Desviación estándar muestral", r"s=\sqrt{\frac{\sum (x_i-\bar{x})^2}{n-1}}", "Se divide entre n − 1."),
        ],
        "tips": ["Pregunta clave: ¿te dan σ (poblacional) o s (de la muestra)?",
                 "El valor t se busca con gl = n − 1 y el área α/2 en una cola.",
                 "Interpreta siempre con el contexto y las unidades."],
    },
    "plant": {
        "corte": 2, "icono": "✍️", "nombre": "Planteamiento de hipótesis",
        "resumen": (
            "Se formulan dos hipótesis opuestas: **H₀** (nula) siempre lleva el signo de igualdad (=, ≤ o ≥) y **H₁** "
            "(alterna) lleva <, > o ≠. Lo que el investigador quiere **demostrar** o sospecha va en **H₁**. "
            "El signo de H₁ define la prueba: > cola derecha, < cola izquierda, ≠ dos colas."),
        "formulas": [
            ("Prueba de dos colas", r"H_0:\mu=\mu_0 \qquad H_1:\mu\neq\mu_0", "Busca cualquier diferencia."),
            ("Cola derecha", r"H_0:\mu\leq\mu_0 \qquad H_1:\mu>\mu_0", "Busca un aumento."),
            ("Cola izquierda", r"H_0:\mu\geq\mu_0 \qquad H_1:\mu<\mu_0", "Busca una disminución."),
            ("Proporción", r"H_0:p=p_0 \qquad H_1:p\neq p_0", "Mismo esquema con p."),
        ],
        "tips": ["'Más de', 'mayor', 'aumentó' → H₁ con >.  'Menos de', 'disminuyó' → H₁ con <.",
                 "'Al menos' y 'a lo sumo' son afirmaciones con igualdad → van en H₀.",
                 "Las hipótesis hablan de parámetros (μ, p), nunca de x̄ ni de p̂."],
    },
    "pvalor": {
        "corte": 2, "icono": "🧪", "nombre": "Valor P (P-value)",
        "resumen": (
            "El **valor P** es la probabilidad de obtener un resultado tan extremo o más que el observado **si H₀ fuera verdadera**. "
            "Un valor P pequeño indica que los datos son poco compatibles con H₀. Se compara con α: si P ≤ α se rechaza H₀."),
        "formulas": [
            ("Cola derecha", r"P=P(Z>z_c)=1-\Phi(z_c)", "z_c = estadístico calculado."),
            ("Cola izquierda", r"P=P(Z<z_c)=\Phi(z_c)", ""),
            ("Dos colas", r"P=2\,P(Z>|z_c|)=2\,[1-\Phi(|z_c|)]", "Se duplica el área de una cola."),
            ("Con t de Student", r"P=P(T_{gl}>t_c)", "Igual, usando la distribución t con sus gl."),
        ],
        "tips": ["El valor P **no** es la probabilidad de que H₀ sea cierta.",
                 "Compara siempre contra α, que se fija **antes** de ver los datos.",
                 "En dos colas no olvides multiplicar por 2."],
    },
    "regla": {
        "corte": 2, "icono": "🚦", "nombre": "Regla de decisión",
        "resumen": (
            "Hay dos formas equivalentes de decidir: (1) **valor crítico**: se rechaza H₀ si el estadístico cae en la región de "
            "rechazo; (2) **valor P**: se rechaza H₀ si P ≤ α. Ambas dan siempre la misma conclusión. Después se redacta la "
            "conclusión en el contexto del problema."),
        "formulas": [
            ("Cola derecha", r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ z_c>z_{\alpha}", ""),
            ("Cola izquierda", r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ z_c<-z_{\alpha}", ""),
            ("Dos colas", r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ |z_c|>z_{\alpha/2}", ""),
            ("Con valor P", r"\mathrm{Rechazar}\ H_0\ \mathrm{si}\ P\leq\alpha", ""),
        ],
        "tips": ["Al rechazar H₀ puedes estar cometiendo error tipo I; al no rechazar, error tipo II.",
                 "Redacta: 'Con α = …, hay (o no hay) evidencia suficiente para afirmar que …'.",
                 "En dos colas, α se reparte mitad y mitad."],
    },
    "ph2": {
        "corte": 2, "icono": "🔬", "nombre": "Prueba de hipótesis (media con σ desconocida y proporción)",
        "resumen": (
            "Cuando σ es desconocida se usa el estadístico **t** con n − 1 grados de libertad. Para una **proporción** se "
            "usa Z, verificando que n·p₀ ≥ 5 y n·(1 − p₀) ≥ 5. El procedimiento es el mismo de cinco etapas: hipótesis, α, "
            "estadístico, regla de decisión y conclusión."),
        "formulas": [
            ("Estadístico t", r"t=\frac{\bar{x}-\mu_0}{s/\sqrt{n}}", "gl = n − 1."),
            ("Proporción muestral", r"\hat{p}=\frac{x}{n}", "x = éxitos observados."),
            ("Estadístico Z para p", r"Z=\frac{\hat{p}-p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}", "El error estándar usa p₀, no p̂."),
            ("Condición de normalidad", r"n\,p_0\geq 5 \quad\mathrm{y}\quad n\,(1-p_0)\geq 5", "Para aproximar con la normal."),
        ],
        "tips": ["Con t, el valor crítico depende de los grados de libertad.",
                 "En proporciones, el error estándar se calcula con p₀ (el valor de H₀).",
                 "Verifica las condiciones antes de aplicar la prueba."],
    },
}

CORTES = {1: "Primer corte", 2: "Segundo corte"}


def topic_ids(corte: int | None = None) -> list[str]:
    return [k for k, v in TOPICS.items() if corte is None or v["corte"] == corte]


def label(tid: str) -> str:
    t = TOPICS[tid]
    return f"{t['icono']} {CORTES[t['corte']]} · {t['nombre']}"


# ---------------------------------------------------------------------------
# Material de apoyo: descripción breve, estrategia paso a paso y errores comunes por tema
# ---------------------------------------------------------------------------
_EXTRA = {
    "normal": {
        "breve": "Estandarizar, leer la tabla Z y entender la media muestral.",
        "estrategia": ["Identifica si preguntan por un dato individual (usa σ) o por un promedio de n datos (usa σ/√n).",
                       "Dibuja la campana y sombrea el área que piden.",
                       "Estandariza: z = (x − μ)/σ.",
                       "Busca Φ(z) en la tabla (área a la izquierda) y ajusta: complemento o resta.",
                       "Escribe la respuesta como probabilidad y como porcentaje."],
        "errores": ["Dividir entre σ en vez de σ/√n cuando se habla de la media muestral.",
                    "Olvidar el complemento en «mayor que».",
                    "Leer la tabla con un z negativo como si fuera positivo."]},
    "discretas": {
        "breve": "Tablas de probabilidad, esperanza, varianza y transformaciones lineales.",
        "estrategia": ["Revisa que las p(x) sumen 1 (despeja k si falta una).",
                       "Arma columnas: x, p(x), x·p(x) y x²·p(x).",
                       "Suma cada columna: E(X) y E(X²).",
                       "Varianza = E(X²) − μ².",
                       "Si hay Y = aX + b, usa las reglas de transformación en lugar de recalcular todo."],
        "errores": ["Usar x² en la esperanza o x en la varianza.",
                    "Olvidar elevar la media al cuadrado en la varianza.",
                    "Sumar la constante b a la varianza."]},
    "binomial": {
        "breve": "Contar éxitos en n ensayos: probabilidades exactas, acumuladas y parámetros.",
        "estrategia": ["Verifica las 4 condiciones y define qué es «éxito».",
                       "Anota n, p, q = 1 − p y k.",
                       "Traduce la frase: exactamente (=), al menos (≥), a lo sumo (≤).",
                       "Aplica la fórmula término a término o usa el complemento si es más corto.",
                       "Revisa que la respuesta esté entre 0 y 1."],
        "errores": ["Confundir «al menos» con «más de».",
                    "Poner p en lugar de q en el exponente n − k.",
                    "Olvidar el número combinatorio."]},
    "ph1": {
        "breve": "Las 5 etapas de una prueba, errores tipo I y II y prueba z para la media.",
        "estrategia": ["Plantea H0 y H1 con el parámetro (μ).",
                       "Fija α y busca el valor crítico según la cola.",
                       "Calcula el estadístico Z = (x̄ − μ₀)/(σ/√n).",
                       "Compara con la región de rechazo.",
                       "Concluye en palabras, con el contexto del problema."],
        "errores": ["Escribir las hipótesis con x̄ en lugar de μ.",
                    "Decir «se acepta H0» en vez de «no se rechaza H0».",
                    "Usar el valor crítico de dos colas en una prueba de una cola."]},
    "ic": {
        "breve": "Confianza, valor crítico, margen de error y tamaño de muestra.",
        "estrategia": ["Convierte la confianza en α y busca z de α/2.",
                       "Calcula el error estándar σ/√n.",
                       "Multiplica para obtener el margen de error E.",
                       "Para el tamaño de muestra despeja n = (zσ/E)² y redondea hacia arriba.",
                       "Interpreta con las unidades del problema."],
        "errores": ["Usar el z de una cola en un intervalo (se necesita α/2).",
                    "Redondear n hacia abajo.",
                    "Interpretarlo como «probabilidad de que μ esté en el intervalo»."]},
    "ic_media": {
        "breve": "Intervalo para μ con z (σ conocida) o con t (σ desconocida).",
        "estrategia": ["Pregúntate: ¿me dan σ o s? Eso decide entre z y t.",
                       "Si es t, calcula gl = n − 1.",
                       "Busca el valor crítico con área α/2 en una cola.",
                       "Calcula E y los límites x̄ ± E.",
                       "Interpreta el intervalo en el contexto."],
        "errores": ["Usar n en lugar de n − 1 en s o en los grados de libertad.",
                    "Usar z teniendo solo s con muestra pequeña.",
                    "Olvidar que el intervalo lleva ± (dos límites)."]},
    "plant": {
        "breve": "Traducir una frase a H0 y H1 y decidir la cola.",
        "estrategia": ["Identifica el parámetro: μ (media) o p (proporción).",
                       "Subraya lo que se quiere demostrar: va en H1.",
                       "Asigna el signo: más/mayor → >, menos/menor → <, diferente/cambió → ≠.",
                       "H0 es lo contrario y lleva la igualdad.",
                       "El signo de H1 te dice la cola."],
        "errores": ["Poner en H1 la afirmación «al menos» del fabricante (lleva igualdad: va en H0).",
                    "Escribir x̄ o p̂ en las hipótesis.",
                    "Usar ≥ o ≤ en H1."]},
    "pvalor": {
        "breve": "Calcular el valor P por cola y compararlo con α.",
        "estrategia": ["Calcula el estadístico de prueba.",
                       "Identifica la cola de H1.",
                       "Área: derecha 1 − Φ(z); izquierda Φ(z); dos colas 2 × el área de una cola.",
                       "Compara: P ≤ α → se rechaza H0.",
                       "Redacta la conclusión en contexto."],
        "errores": ["Olvidar duplicar en dos colas.",
                    "Usar Φ(z) directo en cola derecha.",
                    "Creer que P es la probabilidad de que H0 sea cierta."]},
    "regla": {
        "breve": "Decidir con valor crítico o con valor P y redactar la conclusión.",
        "estrategia": ["Define la cola y α.",
                       "Obtén el valor crítico (z o t).",
                       "Dibuja la región de rechazo.",
                       "Ubica el estadístico: ¿cae dentro de la región?",
                       "Concluye en contexto y menciona el error posible (I o II)."],
        "errores": ["Olvidar el signo negativo del valor crítico en cola izquierda.",
                    "Usar z de α en vez de z de α/2 en dos colas.",
                    "Terminar sin conclusión en palabras."]},
    "ph2": {
        "breve": "Prueba t para la media (σ desconocida) y prueba Z para una proporción.",
        "estrategia": ["Plantea hipótesis y fija α.",
                       "Elige t (σ desconocida) o Z (proporción) y verifica las condiciones.",
                       "Valor crítico (con gl = n − 1 si es t).",
                       "Calcula el estadístico.",
                       "Decide y concluye en contexto."],
        "errores": ["Usar p̂ en el error estándar de la prueba de proporción (se usa p₀).",
                    "Usar gl = n en lugar de n − 1.",
                    "No verificar n·p₀ ≥ 5 y n·(1 − p₀) ≥ 5."]},
}
for _k, _v in _EXTRA.items():
    TOPICS[_k].update(_v)

# Consejos por apartado de la app
TIPS_APRENDER = [
    "Empieza por **un tema**, lee el resumen y mira el ejemplo resuelto **antes** de intentar los talleres.",
    "Pulsa **«Otro ejemplo»** varias veces: ver el mismo método con otros números es lo que fija la idea.",
    "Tapa la solución con la mano, resuelve el ejemplo en papel y luego compara paso a paso.",
    "Anota en una hoja tu propio **formulario** con las fórmulas del tema y cuándo se usa cada una.",
    "Si dudas entre dos métodos (z o t, una o dos colas), revisa la sección «Ideas para no perderte».",
]
TIPS_TALLER = [
    "Elige pocos temas y nivel **Fácil** al comenzar; sube a Medio y Difícil cuando ya no mires las fórmulas.",
    "Resuelve en papel **sin abrir los resultados**; escribe cada paso aunque parezca obvio.",
    "Al comparar, no mires solo la respuesta final: revisa **dónde** se separó tu procedimiento del paso a paso.",
    "Repite el mismo taller con su **código** unos días después para medir tu avance.",
    "Anota los errores que más repites; la sección de «Errores comunes» de cada tema te ayuda a detectarlos.",
]
TIPS_EXAMEN = [
    "Simula las condiciones reales: sin fórmulas de ayuda, con calculadora y tablas Z y t.",
    "Lee todo el examen primero y empieza por los ejercicios que mejor dominas.",
    "En hipótesis, escribe siempre las **5 etapas**; la conclusión en palabras suele valer puntos.",
    "Reserva los últimos minutos para revisar signos, colas y redondeos.",
    "Al terminar, descarga el solucionario y corrige tú mismo con el puntaje de cada ejercicio.",
]
TIPS_FORMULARIO = [
    "Úsalo como **consulta rápida**, no como reemplazo del paso a paso: entender de dónde sale cada fórmula pesa más.",
    "Antes de elegir una fórmula, responde: ¿qué parámetro? ¿σ conocida o s? ¿cuántas colas?",
    "Memoriza los valores z más frecuentes (1.645, 1.960, 2.326, 2.576).",
]
GUIA_DECISION = [
    ["Si el problema dice...", "Entonces usa..."],
    ["Un dato individual de una normal", "Z = (x − μ)/σ"],
    ["Promedio de n datos, σ conocida", "Z = (x̄ − μ)/(σ/√n)"],
    ["Promedio de n datos, solo s", "t con n − 1 grados de libertad"],
    ["Proporción de la muestra", "Z con error estándar √(p₀q₀/n)"],
    ["Número de éxitos en n ensayos", "Binomial"],
    ["«Mayor / aumentó» en H1", "Cola derecha"],
    ["«Menor / disminuyó» en H1", "Cola izquierda"],
    ["«Diferente / cambió» en H1", "Dos colas (α/2 en cada una)"],
]


def tip_for(tid: str, i: int) -> str:
    t = TOPICS[tid]["tips"]
    return t[i % len(t)]


def error_for(tid: str, i: int) -> str:
    e = TOPICS[tid]["errores"]
    return e[i % len(e)]


NIVEL_TIPS = {
    "Fácil": "Es un ejercicio directo: identifica los datos, aplica la fórmula una sola vez y revisa las unidades.",
    "Medio": "Combina dos ideas (por ejemplo estandarizar y usar el complemento). Ve por partes y no saltes pasos.",
    "Difícil": "Requiere varios pasos encadenados. Haz un esquema de lo que te piden, resuelve cada parte por separado y verifica la coherencia al final.",
}


def consejo_detallado(p: dict, idx: int) -> dict:
    """Material del botón «Ver consejo»: explica cómo pensar el ejercicio sin dar la respuesta."""
    t = TOPICS[p["tema"]]
    return {"tema": t["nombre"], "idea": tip_for(p["tema"], idx), "resumen": t["resumen"],
            "inicio": t["estrategia"], "formulas": p["formulas"][:3], "error": error_for(p["tema"], idx),
            "nivel": NIVEL_TIPS[p["nivel"]]}

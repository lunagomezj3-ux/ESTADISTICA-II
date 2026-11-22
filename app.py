"""
app.py · Simulador de Estadística 2 (tema Jinshi)
-------------------------------------------------
Aprende (teoría + fórmulas + ejemplo resuelto paso a paso), genera talleres y exámenes aleatorios por tema y nivel,
descárgalos en PDF y revisa los resultados cuando quieras. No se cargan datos: todo se genera dentro de la app.

Ejecutar:  streamlit run app.py
"""

from __future__ import annotations

import random
from html import escape

import streamlit as st

import content as ct
import pdf_export as pe
import problems as pr
import theme

st.set_page_config(page_title="Simulador de Estadística 2", page_icon="❖", layout="wide")
st.markdown(theme.css(), unsafe_allow_html=True)
st.markdown("<style>.katex{color:#2B1B3D;font-size:1.08em}</style>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------- utilidades de interfaz
def md_table(rows: list[list[str]]) -> str:
    head = "| " + " | ".join(rows[0]) + " |\n|" + "---|" * len(rows[0]) + "\n"
    return head + "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])


def box(kind: str, title: str, text: str) -> None:
    st.markdown(f'<div class="{kind}-box"><b>{title}</b> {escape(text, quote=False)}</div>', unsafe_allow_html=True)


def tips_expander(titulo: str, tips: list[str], expanded: bool = False) -> None:
    with st.expander(titulo, expanded=expanded):
        for t in tips:
            st.markdown(f"- {t}")


def show_problem(p: dict, idx: int, *, solucion: bool, formulas: bool, puntos: float | None = None,
                 tip: bool = False) -> None:
    t = ct.TOPICS[p["tema"]]
    pts = f" · {puntos:g} pts" if puntos else ""
    st.markdown(f"#### Ejercicio {idx}")
    st.caption(f"{t['icono']} {t['nombre']} · Nivel {p['nivel']}{pts}")
    st.markdown(p["enunciado"])
    if p.get("tabla"):
        st.markdown(md_table(p["tabla"]))
    if formulas and p["formulas"]:
        with st.container(border=True):
            st.markdown("**📐 Fórmulas de ayuda**")
            for f in p["formulas"]:
                st.latex(f)
    if tip:
        box("tip", "💡 Tip para resolverlo:", ct.tip_for(p["tema"], idx - 1))
    if solucion:
        with st.container(border=True):
            st.markdown("**✅ Solución paso a paso**")
            for k, (txt, m) in enumerate(p["pasos"], 1):
                st.markdown(f'<span class="step-n">{k}</span>{escape(txt, quote=False)}', unsafe_allow_html=True)
                if m:
                    st.latex(m)
            st.success(f"**Respuesta:** {p['respuesta']}")
        box("err", "⚠️ Error común en este tema:", ct.error_for(p["tema"], idx - 1))
    st.divider()


# ----------------------------------------------------------------------------- selector de temas
def set_topics(prefix: str, ids: list[str]) -> None:
    for tid in ct.TOPICS:
        st.session_state[f"{prefix}_chk_{tid}"] = tid in ids


def topic_picker(prefix: str) -> list[str]:
    """Tarjetas por corte con casillas: uno, varios o todos los temas, con atajos y resumen de la selección."""
    first = ct.topic_ids()[0]
    for tid in ct.TOPICS:
        st.session_state.setdefault(f"{prefix}_chk_{tid}", tid == first)

    st.markdown('<div class="pick-title">🧭 Elige tus temas (uno, varios o todos)</div>', unsafe_allow_html=True)
    b = st.columns(4)
    b[0].button("✦ Primer corte", key=f"{prefix}_b1", on_click=set_topics, args=(prefix, ct.topic_ids(1)), use_container_width=True)
    b[1].button("✦ Segundo corte", key=f"{prefix}_b2", on_click=set_topics, args=(prefix, ct.topic_ids(2)), use_container_width=True)
    b[2].button("❖ Todos", key=f"{prefix}_b3", on_click=set_topics, args=(prefix, ct.topic_ids()), use_container_width=True)
    b[3].button("↺ Limpiar", key=f"{prefix}_b4", on_click=set_topics, args=(prefix, []), use_container_width=True)

    cols = st.columns(2)
    for col, corte in zip(cols, (1, 2)):
        with col:
            ids = ct.topic_ids(corte)
            n_sel = sum(st.session_state[f"{prefix}_chk_{tid}"] for tid in ids)
            st.markdown(f'<div class="corte-head">{ct.CORTES[corte]}<small>{n_sel}/{len(ids)} elegidos</small></div>',
                        unsafe_allow_html=True)
            for tid in ids:
                t = ct.TOPICS[tid]
                with st.container(border=True):
                    st.checkbox(f"{t['icono']} **{t['nombre']}**", key=f"{prefix}_chk_{tid}")
                    st.caption(t["breve"])

    sel = [tid for tid in ct.topic_ids() if st.session_state[f"{prefix}_chk_{tid}"]]
    if sel:
        chips = "".join(f'<span class="sel-chip">{t["icono"]} {escape(t["nombre"].split(" (")[0])}</span>' for t in (ct.TOPICS[i] for i in sel))
        st.markdown(f'<div class="sel-bar"><b>{len(sel)} de {len(ct.TOPICS)} temas</b> seleccionados<br>{chips}</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="sel-bar">Aún no has elegido ningún tema: marca al menos uno para continuar.</div>',
                    unsafe_allow_html=True)
    return sel


def new_seed() -> int:
    return random.randint(10000, 99999)


# ----------------------------------------------------------------------------- barra lateral y cabecera
with st.sidebar:
    st.markdown(theme.sidebar_brand_html(), unsafe_allow_html=True)
    st.markdown("")
    with st.expander("¿Cómo se usa?", expanded=True):
        st.markdown(
            "1. **📚 Aprender**: elige temas y estudia fórmulas con un ejemplo resuelto.\n"
            "2. **📝 Taller**: genera ejercicios aleatorios por tema y nivel.\n"
            "3. **🎓 Examen**: igual, pero sin fórmulas de ayuda y con puntaje.\n"
            "4. Resuelve en papel, descarga el PDF y pulsa **Ver resultados** para comparar tu procedimiento.")
    with st.expander("💡 Consejos de estudio"):
        st.markdown(
            "- Estudiar poco **cada día** rinde más que mucho la víspera.\n"
            "- Entiende el *porqué* de cada fórmula antes de memorizarla.\n"
            "- Corrige tus errores y anótalos: los verás repetirse hasta que los domines.")
    st.caption("Los ejercicios son aleatorios; el **código** del taller permite repetirlo exactamente.")

st.markdown(theme.hero_html(), unsafe_allow_html=True)
if theme.univalle_uri():
    st.markdown(theme.univalle_fixed_html(), unsafe_allow_html=True)

tab_aprender, tab_taller, tab_examen, tab_formulas = st.tabs(["📚 Aprender", "📝 Taller", "🎓 Examen", "📐 Formulario"])


# ----------------------------------------------------------------------------- 1 · APRENDER
with tab_aprender:
    st.markdown("### 📚 Elige qué quieres entender mejor")
    tips_expander("💡 Cómo sacarle provecho a esta pestaña", ct.TIPS_APRENDER)
    temas = topic_picker("ap")
    nivel_ej = st.select_slider("Nivel del ejemplo resuelto", ct.NIVELES, value="Medio", key="ap_nivel")
    if not temas:
        st.info("Selecciona al menos un tema para ver la teoría, las fórmulas y un ejemplo paso a paso.")
    for tid in [t for t in ct.topic_ids() if t in temas]:
        t = ct.TOPICS[tid]
        with st.expander(ct.label(tid), expanded=len(temas) == 1):
            st.markdown(t["resumen"])
            st.markdown("##### Fórmulas")
            for nombre, latex, nota in t["formulas"]:
                st.markdown(f"**{nombre}**")
                st.latex(latex)
                if nota:
                    st.caption(nota)
            st.markdown("##### 🧩 Cómo resolver un problema de este tema")
            for k, paso in enumerate(t["estrategia"], 1):
                st.markdown(f'<span class="step-n">{k}</span>{escape(paso, quote=False)}', unsafe_allow_html=True)
            st.markdown("##### 💡 Ideas para no perderte")
            for tip in t["tips"]:
                st.markdown(f"- {tip}")
            st.markdown("##### ⚠️ Errores comunes")
            for e in t["errores"]:
                st.markdown(f'<div class="err-box">{escape(e, quote=False)}</div>', unsafe_allow_html=True)
            st.markdown("##### ✍️ Ejemplo resuelto")
            sk = f"ej_{tid}"
            st.session_state.setdefault(sk, new_seed())
            st.button("🔄 Otro ejemplo", key=f"btn_{sk}", on_click=lambda k=sk: st.session_state.update({k: new_seed()}))
            ej = pr.make_one(tid, nivel_ej, random.Random(f"{st.session_state[sk]}-{nivel_ej}"))
            show_problem(ej, 1, solucion=True, formulas=False)


# ----------------------------------------------------------------------------- 2 y 3 · TALLER / EXAMEN
def workshop(kind: str) -> None:
    es_ex = kind == "examen"
    nombre = "examen" if es_ex else "taller"
    st.markdown(f"### {'🎓 Examen' if es_ex else '📝 Taller'} aleatorio")
    st.caption("Aquí **no se responde**: solo se muestran los ejercicios. Resuélvelos en papel y luego pulsa "
               "**Ver resultados** para comparar con el procedimiento y la solución.")
    tips_expander("💡 Consejos para resolver tu " + nombre, ct.TIPS_EXAMEN if es_ex else ct.TIPS_TALLER)
    temas = topic_picker(kind)
    c1, c2, c3 = st.columns(3)
    n = c1.slider("Número de ejercicios", 1, 20, 6, key=f"{kind}_n")
    nivel = c2.selectbox("Nivel", pr.NIVELES_UI, index=1, key=f"{kind}_nivel",
                         help="«Mixto» combina fácil, medio y difícil.")
    code_in = c3.text_input("Código (opcional)", key=f"{kind}_code", placeholder="Para repetir un " + nombre)
    ayuda = False
    if not es_ex:
        ayuda = st.checkbox("Mostrar fórmulas de ayuda y un tip en cada ejercicio", value=True, key=f"{kind}_ayuda")
    if temas and n < len(temas):
        st.warning(f"Elegiste {len(temas)} temas y {n} ejercicios: no todos los temas tendrán ejercicio. "
                   "Sube el número de ejercicios para cubrirlos todos.")

    if st.button(f"🎲 Generar {nombre}", type="primary", disabled=not temas, key=f"{kind}_gen"):
        seed = int(code_in) if code_in.strip().isdigit() else new_seed()
        with st.spinner("Creando ejercicios y PDF…"):
            ps = pr.generate_set(temas, n, nivel, seed)
            kw = dict(nivel=nivel, codigo=str(seed), examen=es_ex)
            titulo = "Examen" if es_ex else "Taller de práctica"
            st.session_state[f"{kind}_set"] = {
                "problems": ps, "seed": seed, "ayuda": ayuda, "show": False,
                "pdf_q": pe.build_pdf(titulo, ps, solucion=False, formulas=ayuda, **kw),
                "pdf_s": pe.build_pdf(titulo + " (solucionario)", ps, solucion=True, formulas=False, **kw)}

    data = st.session_state.get(f"{kind}_set")
    if not data:
        st.info("Elige los temas, el número de ejercicios y el nivel; luego pulsa **Generar**.")
        return

    st.divider()
    st.markdown(f"**Código:** `{data['seed']}` · {len(data['problems'])} ejercicios")

    def toggle() -> None:
        data["show"] = not data["show"]

    b1, b2, b3 = st.columns(3)
    b1.download_button(f"📄 Descargar {nombre} (PDF)", data["pdf_q"], f"{nombre}_estadistica2_{data['seed']}.pdf",
                       "application/pdf", type="primary", key=f"{kind}_dl_q", use_container_width=True)
    b2.download_button("🔑 Descargar solucionario (PDF)", data["pdf_s"], f"solucionario_{nombre}_{data['seed']}.pdf",
                       "application/pdf", key=f"{kind}_dl_s", use_container_width=True)
    b3.button("🙈 Ocultar resultados" if data["show"] else "👁️ Ver resultados y procedimiento",
              on_click=toggle, key=f"{kind}_toggle", use_container_width=True)
    if data["show"]:
        box("tip", "💡 Cómo comparar:", "revisa primero dónde se separa tu procedimiento del paso a paso; "
            "si solo falló un redondeo, tu método está bien.")
    st.markdown("")
    pts = round(5 / len(data["problems"]), 2) if es_ex else None
    for i, p in enumerate(data["problems"], 1):
        show_problem(p, i, solucion=data["show"], formulas=data["ayuda"] and not es_ex, puntos=pts,
                     tip=(data["ayuda"] and not es_ex))


with tab_taller:
    workshop("taller")
with tab_examen:
    workshop("examen")


# ----------------------------------------------------------------------------- 4 · FORMULARIO
with tab_formulas:
    st.markdown("### 📐 Formulario rápido")
    tips_expander("💡 Cómo usar el formulario", ct.TIPS_FORMULARIO)
    st.markdown("#### 🧭 ¿Qué herramienta uso?")
    st.markdown(md_table(ct.GUIA_DECISION))
    for corte, nom in ct.CORTES.items():
        st.markdown(f"#### {nom}")
        for tid in ct.topic_ids(corte):
            t = ct.TOPICS[tid]
            with st.expander(f"{t['icono']} {t['nombre']}"):
                for nombre, latex, nota in t["formulas"]:
                    st.markdown(f"**{nombre}**")
                    st.latex(latex)
                    if nota:
                        st.caption(nota)
    st.markdown("#### Valores críticos z frecuentes")
    st.markdown(md_table([["Confianza", "80%", "90%", "95%", "98%", "99%"],
                          ["z de alfa/2 (dos colas)", "1.282", "1.645", "1.960", "2.326", "2.576"],
                          ["z de alfa (una cola)", "0.842", "1.282", "1.645", "2.054", "2.326"]]))

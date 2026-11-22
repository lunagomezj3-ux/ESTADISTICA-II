"""
theme.py · Identidad visual del Simulador de Estadística 2
-------------------------------------
Tema inspirado en Jinshi (壬氏), de «Los diarios de la boticaria»: oro imperial, púrpura de corte y bermellón sobre papel de arroz.
Todo el color vive aquí: para cambiar la paleta basta con editar el diccionario C.

Logo: si existe assets/logo.png (o .jpg/.webp/.svg) se usa ese archivo; si no, se usa
LOGO_URL (imagen en línea). Si la URL no carga, se muestra el emblema floral incluido.
"""

from __future__ import annotations

import base64
from pathlib import Path

C = {
    "bg": "#FAF5EA", "surface": "#FFFFFF", "surface2": "#F3EAD7", "border": "#D9C49A",
    "tx": "#111111", "muted": "#2E2838",
    "a1": "#C9962A",   # oro imperial
    "a2": "#E8C25A",   # oro claro (adorno del cabello)
    "pur": "#5B2E8C", "pur2": "#4B2A6B", "ink": "#2B1B3D", "red": "#B5342B",   # púrpura de corte, tinta, bermellón del palacio
    "ok": "#4CAF7A", "warn": "#E8A020", "bad": "#B5342B",
}
PALETA = [C["pur"], C["a1"], C["red"], "#8E6BBF", "#E8C25A", "#2B1B3D", "#6BBF8A"]
AUTORA = "Jinshi Ka Zuigetsu"

NOMBRE = "ESTADÍSTICA 2"
SIGNIFICADO = "Estudia con la elegancia de la corte imperial"
LOGO_URL = "https://static.wikia.nocookie.net/asia/images/6/6e/Jinshi.jpg/revision/latest?cb=20260122233611&path-prefix=es"

# Emblema floral de respaldo (se usa solo si no hay assets/logo.* y la URL no carga)
_LOGO_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'>
<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#F6E3A1'/><stop offset='1' stop-color='#C9962A'/></linearGradient>
<linearGradient id='b' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#4B2A6B'/><stop offset='1' stop-color='#2B1B3D'/></linearGradient></defs>
<rect width='120' height='120' rx='28' fill='url(#b)'/><rect x='6' y='6' width='108' height='108' rx='23' fill='none' stroke='url(#g)' stroke-width='2.5'/>
<g stroke='url(#g)' stroke-width='3' stroke-linecap='round' fill='none'><line x1='60' y1='13' x2='60' y2='24'/><circle cx='60' cy='30' r='5' fill='#B5342B' stroke='url(#g)'/></g>
<text x='60' y='88' text-anchor='middle' font-size='56' font-weight='700' fill='url(#g)' font-family='Noto Serif CJK JP, Noto Serif JP, Yu Mincho, MS Mincho, serif'>壬</text>
<circle cx='28' cy='100' r='3' fill='#E8C25A'/><circle cx='92' cy='100' r='3' fill='#E8C25A'/></svg>"""


TIP_ICON_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0_e-nP3rAcLjNSPg1E6XkdCMvMjLCB-ESswaCJN_JtFNK2tpc4rp2xzw&s=10"

_TIP_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'><circle cx='60' cy='60' r='56' fill='#F6E3A1' stroke='#C9962A' stroke-width='6'/>
<path d='M60 26c-14 0-24 10-24 23 0 9 5 15 10 20 3 3 4 6 4 10h20c0-4 1-7 4-10 5-5 10-11 10-20 0-13-10-23-24-23z' fill='#E8C25A' stroke='#2B1B3D' stroke-width='3'/>
<rect x='48' y='84' width='24' height='8' rx='3' fill='#2B1B3D'/></svg>"""


def tip_icon_uri() -> str:
    """Icono del botón de consejos: assets/tip_icon.(png|jpg|jpeg|webp|svg) si existe; si no, TIP_ICON_URL."""
    base = Path(__file__).parent / "assets"
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"),
                      ("webp", "image/webp"), ("svg", "image/svg+xml")):
        f = base / f"tip_icon.{ext}"
        if f.exists():
            return f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return TIP_ICON_URL


def tip_icon_html(px: int = 72) -> str:
    fb = "data:image/svg+xml;base64," + base64.b64encode(_TIP_SVG.encode()).decode()
    return (f'<img class="tip-icon" src="{tip_icon_uri()}" alt="consejo" width="{px}" height="{px}" referrerpolicy="no-referrer" '
            f'onerror="this.onerror=null;this.src=\'{fb}\'">')


def _fallback_uri() -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(_LOGO_SVG.encode()).decode()


def logo_uri() -> str:
    """Logo: archivo propio en assets/ si existe; si no, la imagen en línea (LOGO_URL)."""
    base = Path(__file__).parent / "assets"
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"),
                      ("webp", "image/webp"), ("svg", "image/svg+xml")):
        f = base / f"logo.{ext}"
        if f.exists():
            return f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return LOGO_URL or _fallback_uri()


def _logo_img() -> str:
    return (f'<img src="{logo_uri()}" alt="logo" referrerpolicy="no-referrer" '
            f'onerror="this.onerror=null;this.src=\'{_fallback_uri()}\'">')


UNIVALLE_NOMBRE = "Universidad del Valle"
UNIVALLE_ROJO = "#B3122B"


def univalle_uri() -> str | None:
    """Logo de Univalle: assets/logo_univalle.(png|jpg|jpeg|webp|svg). None si no existe."""
    base = Path(__file__).parent / "assets"
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"),
                      ("webp", "image/webp"), ("svg", "image/svg+xml")):
        f = base / f"logo_univalle.{ext}"
        if f.exists():
            return f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return None


def univalle_badge_html() -> str:
    """Insignia de Univalle: usa el archivo si existe; si no, un rótulo de texto en rojo institucional."""
    uri = univalle_uri()
    if uri:
        return f'<span class="uv-badge"><img src="{uri}" alt="Universidad del Valle"></span>'
    return ('<span class="uv-badge"><span class="uv-word"><small>UNIVERSIDAD</small>'
            '<b>DEL VALLE</b></span></span>')


def univalle_fixed_html() -> str:
    """Insignia fija en la esquina inferior derecha: aparece en TODAS las pestañas."""
    return f'<div class="uv-fixed">{univalle_badge_html()}</div>'


def _significado_html() -> str:
    return SIGNIFICADO


def _base_css() -> str:
    c = C
    return f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');
:root {{ color-scheme: light; }}
html, body, .stApp {{ font-family:'Inter',sans-serif; color:{c['tx']}; }}
.stApp {{ background:
  radial-gradient(900px 520px at 6% -10%, rgba(201,150,42,.20), transparent 60%),
  radial-gradient(800px 460px at 100% 0%, rgba(91,46,140,.16), transparent 55%),
  radial-gradient(700px 420px at 50% 115%, rgba(181,52,43,.07), transparent 60%), {c['bg']}; }}
header[data-testid="stHeader"] {{ background:transparent; }}
footer {{ visibility:hidden; }}
.block-container {{ padding-top:2.2rem; max-width:1300px; }}
h1,h2,h3,h4,h5 {{ font-family:'Sora',sans-serif; color:{c['tx']} !important; letter-spacing:-.01em; }}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] td, [data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] strong, [data-testid="stWidgetLabel"] *, label *
  {{ color:{c['tx']}; }}
[data-testid="stCaptionContainer"] *, .stCaption {{ color:{c['muted']} !important; }}
[data-testid="stMarkdownContainer"] code {{ background:{c['surface2']}; color:#5B2E8C; border-radius:6px; }}
hr {{ border-color:{c['border']} !important; }}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#F3EAD7,#E9DDBF); border-right:1px solid {c['border']}; }}
section[data-testid="stSidebar"] * {{ color:{c['tx']}; }}
.sb-brand {{ display:flex; align-items:center; gap:12px; margin:4px 0 6px; }}
.sb-brand img {{ width:50px; height:50px; border-radius:14px; object-fit:cover; background:#fff;
  box-shadow:0 4px 14px rgba(201,150,42,.28); }}
.sb-brand b {{ font-family:'Sora'; font-size:1.25rem; letter-spacing:.08em; display:block; line-height:1.1;
  color:#5B2E8C; }}
.sb-brand small {{ color:{c['muted']}; font-size:.62rem; letter-spacing:.04em; line-height:1.25; display:block; margin-top:3px; }}
.sb-author {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:12px; padding:9px 12px;
  font-size:.82rem; color:{c['muted']}; }}
.sb-author b {{ color:{c['tx']}; }}

/* ---------- inputs ---------- */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {{
  background:{c['surface']} !important; border-color:{c['border']} !important; border-radius:10px !important; }}
input, textarea {{ color:{c['tx']} !important; -webkit-text-fill-color:{c['tx']} !important; }}
[data-baseweb="select"] * {{ color:{c['tx']} !important; }}
[data-baseweb="popover"] *, ul[role="listbox"] {{ background:{c['surface']}; color:{c['tx']}; }}
li[role="option"]:hover, li[aria-selected="true"] {{ background:{c['surface2']} !important; }}
[data-testid="stFileUploaderDropzone"] {{ background:{c['surface']}; border:1.5px dashed {c['a1']}; border-radius:14px; }}
[data-testid="stFileUploaderDropzone"] * {{ color:{c['muted']} !important; }}
[data-testid="stFileUploaderDropzone"] button {{ background:{c['surface2']}; border:1px solid {c['border']}; }}
[data-testid="stFileUploaderDropzone"] button * {{ color:{c['tx']} !important; }}

/* ---------- botones ---------- */
.stButton > button, .stDownloadButton > button, .stLinkButton a {{
  background:{c['surface']}; color:{c['tx']}; border:1px solid {c['border']}; border-radius:10px;
  font-weight:600; transition:all .15s; }}
.stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton a:hover {{
  border-color:{c['a1']}; color:#5B2E8C; transform:translateY(-1px); }}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {{
  background:linear-gradient(120deg,{c['a1']},{c['a2']}); border:0; color:#2B1B3D !important;
  box-shadow:0 6px 20px rgba(201,150,42,.32); }}
.stButton > button[kind="primary"] *, .stDownloadButton > button[kind="primary"] * {{ color:#2B1B3D !important; }}
section[data-testid="stSidebar"] .stButton > button {{ width:100%; }}

/* ---------- pestañas en forma de píldora ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap:6px; background:{c['surface']}; padding:6px; border-radius:14px;
  border:1px solid {c['border']}; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display:none; }}
.stTabs [data-baseweb="tab"] {{ background:transparent; border-radius:10px; padding:8px 16px; height:auto; }}
.stTabs [data-baseweb="tab"] p {{ color:{c['muted']}; font-weight:600; font-size:.9rem; }}
.stTabs [aria-selected="true"] {{ background:linear-gradient(120deg,rgba(201,150,42,.28),rgba(232,194,90,.32)) !important; }}
.stTabs [aria-selected="true"] p {{ color:{c['tx']} !important; }}

/* ---------- componentes ---------- */
[data-testid="stExpander"] {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:14px; }}
[data-testid="stExpander"] summary * {{ color:{c['tx']} !important; }}
[data-testid="stAlert"] {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:12px; }}
[data-testid="stAlert"] * {{ color:{c['tx']} !important; }}
[data-testid="stDataFrame"] {{ border:1px solid {c['border']}; border-radius:12px; overflow:hidden; }}
[data-testid="stForm"] {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:14px; }}

/* ---------- BARRA SUPERIOR: botones visibles y ubicables ---------- */
header[data-testid="stHeader"] {{ background:rgba(250,245,234,.94) !important; backdrop-filter:blur(8px);
  border-bottom:1px solid {c['border']}; }}
header[data-testid="stHeader"] button, [data-testid="stToolbar"] button,
[data-testid="stSidebarCollapseButton"] button, [data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] button, [data-testid="collapsedControl"] button {{
  background:{c['surface']} !important; color:{c['tx']} !important; border:1.5px solid {c['border']} !important;
  border-radius:10px !important; box-shadow:0 2px 8px rgba(201,150,42,.15); opacity:1 !important; }}
header[data-testid="stHeader"] button:hover, [data-testid="stToolbar"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover, [data-testid="stExpandSidebarButton"]:hover {{
  border-color:{c['a1']} !important; background:{c['surface2']} !important; color:#4B2A6B !important; }}
header[data-testid="stHeader"] svg, [data-testid="stToolbar"] svg, [data-testid="stSidebarCollapseButton"] svg,
[data-testid="stExpandSidebarButton"] svg, [data-testid="stSidebarCollapsedControl"] svg
  {{ fill:currentColor !important; color:inherit !important; opacity:1 !important; }}
[data-testid="stIconMaterial"], [data-testid="stHeader"] span, [data-testid="stStatusWidget"] * {{ color:{c['tx']} !important; }}
[data-testid="stAppDeployButton"], .stDeployButton {{ display:none !important; }}
[data-testid="stMainMenuPopover"], [data-testid="stMainMenuPopover"] * , [data-baseweb="menu"], [data-baseweb="menu"] *
  {{ background:{c['surface']} !important; color:{c['tx']} !important; }}
[data-testid="stMainMenuPopover"] li:hover, [data-baseweb="menu"] li:hover {{ background:{c['surface2']} !important; }}
[data-testid="stExpander"] svg, [data-baseweb="select"] svg, [data-testid="stNumberInput"] button svg
  {{ fill:{c['tx']} !important; color:{c['tx']} !important; }}
[data-testid="stNumberInput"] button {{ background:{c['surface2']} !important; border-color:{c['border']} !important; }}

/* ---------- LEGIBILIDAD: fondos claros forzados (evita cajas oscuras con letra oscura) ---------- */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
[data-baseweb="textarea"] textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] > div,
[data-baseweb="base-input"] {{ background:{c['surface']} !important; color:{c['tx']} !important;
  -webkit-text-fill-color:{c['tx']} !important; }}
textarea::placeholder, input::placeholder {{ color:{c['muted']} !important; -webkit-text-fill-color:{c['muted']} !important;
  opacity:1 !important; }}
[data-testid="stAlert"], [data-testid="stAlert"] > div, [data-testid="stAlertContainer"] {{
  background:{c['surface']} !important; color:{c['tx']} !important; border-radius:12px; }}
[data-testid="stAlert"] p, [data-testid="stAlert"] span, [data-testid="stAlert"] div {{ color:{c['tx']} !important; }}
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]), [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) > div
  {{ background:#E9F7EE !important; border-left:5px solid {c['ok']} !important; }}
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]), [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) > div
  {{ background:#FFF4DB !important; border-left:5px solid {c['warn']} !important; }}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]), [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) > div
  {{ background:#EFE6F7 !important; border-left:5px solid {c['a1']} !important; }}
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]), [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) > div
  {{ background:#FDE8E8 !important; border-left:5px solid {c['bad']} !important; }}
[data-testid="stCode"] pre, [data-testid="stCode"] code, pre {{ background:{c['surface2']} !important; color:{c['tx']} !important; }}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {{ background:{c['surface']} !important; }}
[data-testid="stMetric"] * {{ color:{c['tx']} !important; }}
.card .ico {{ position:absolute; right:14px; top:14px; font-size:1.5rem; width:38px; height:38px; display:grid;
  place-items:center; border-radius:12px; background:linear-gradient(135deg,rgba(201,150,42,.16),rgba(232,194,90,.24)); }}
.card .val {{ padding-right:34px; }}

/* ---------- Univalle (todas las páginas) ---------- */
.uv-badge {{ display:inline-flex; align-items:center; background:#fff; border:1px solid {c['border']};
  border-radius:12px; padding:5px 12px; box-shadow:0 4px 14px rgba(179,18,43,.12); }}
.uv-badge img {{ height:34px; width:auto; display:block; }}
.uv-word {{ display:flex; flex-direction:column; line-height:1; border-left:4px solid {UNIVALLE_ROJO};
  padding-left:8px; font-family:'Sora',sans-serif; }}
.uv-word small {{ font-size:.58rem; letter-spacing:.2em; color:{UNIVALLE_ROJO}; font-weight:600; }}
.uv-word b {{ font-size:1.02rem; color:{UNIVALLE_ROJO}; font-weight:800; letter-spacing:.04em; margin-top:2px; }}
.uv-fixed {{ position:fixed; right:18px; bottom:14px; z-index:9999; }}

/* ---------- Guía paso a paso ---------- */
.g-route {{ display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 18px; }}
.g-chip {{ background:linear-gradient(120deg,rgba(201,150,42,.16),rgba(91,46,140,.16)); border:1px solid {c['border']};
  border-radius:999px; padding:6px 14px; font-size:.82rem; font-weight:600; color:{c['tx']}; }}
.g-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:16px; margin-bottom:22px; }}
.g-step {{ background:linear-gradient(180deg,{c['surface']},{c['surface2']}); border:1px solid {c['border']};
  border-radius:18px; padding:16px 18px; position:relative; overflow:hidden; }}
.g-step::before {{ content:''; position:absolute; left:0; top:0; bottom:0; width:5px;
  background:linear-gradient(180deg,{c['a1']},{c['a2']}); }}
.g-head {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
.g-n {{ display:inline-grid; place-items:center; min-width:30px; height:30px; border-radius:10px; font-weight:800;
  background:linear-gradient(120deg,{c['a1']},{c['a2']}); color:#2B1B3D; }}
.g-ico {{ font-size:1.5rem; }}
.g-title {{ font-family:'Sora',sans-serif; font-weight:700; font-size:1.02rem; color:{c['tx']}; line-height:1.2; }}
.g-where {{ display:inline-block; margin-top:3px; font-size:.7rem; font-weight:600; padding:2px 9px; border-radius:999px;
  background:rgba(201,150,42,.12); color:#4B2A6B; }}
.g-step ul {{ margin:8px 0 10px 18px; padding:0; color:{c['tx']}; font-size:.9rem; }}
.g-step li {{ margin-bottom:4px; }}
.g-tip {{ background:#FFF4DB; border-radius:10px; padding:7px 11px; font-size:.82rem; color:{c['tx']}; }}
.g-faq {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:12px; padding:10px 14px; margin-bottom:8px; }}
.g-faq summary {{ cursor:pointer; font-weight:600; color:{c['tx']}; }}
.g-faq p {{ margin:8px 0 0; color:{c['muted']}; }}

/* ---------- PROMPTS / AGENTE: selector y cuadro de texto siempre claros (nunca negros) ---------- */
textarea, input, select {{ color-scheme:light !important; }}
[data-testid="stTextArea"], [data-testid="stTextArea"] > div, [data-testid="stTextAreaRootElement"],
[data-testid="stTextArea"] [data-baseweb="textarea"], [data-testid="stTextArea"] [data-baseweb="base-input"] {{
  background:{c['surface']} !important; border-color:{c['border']} !important; }}
[data-testid="stTextArea"] textarea {{ background:{c['surface']} !important; color:{c['tx']} !important;
  -webkit-text-fill-color:{c['tx']} !important; caret-color:{c['a1']} !important; font-size:.92rem; line-height:1.5; }}
[data-testid="stTextArea"] textarea:focus {{ box-shadow:0 0 0 2px rgba(201,150,42,.35) !important; }}
[data-testid="stSelectbox"] [data-baseweb="select"], [data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] div, [data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] input {{ background:{c['surface']} !important; color:{c['tx']} !important;
  -webkit-text-fill-color:{c['tx']} !important; }}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{ border:1.5px solid {c['border']} !important; }}
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li, ul[role="listbox"], li[role="option"], [data-baseweb="menu"] {{
  background:{c['surface']} !important; color:{c['tx']} !important; border-color:{c['border']} !important; }}
li[role="option"] * {{ color:{c['tx']} !important; background:transparent !important; }}
li[role="option"]:hover, li[aria-selected="true"] {{ background:{c['surface2']} !important; }}
[data-testid="stRadio"] label, [data-testid="stRadio"] label * {{ color:{c['tx']} !important; }}
[data-testid="stForm"] {{ background:{c['surface']} !important; }}
.r-top .r-pct {{ margin-left:auto; text-align:right; font-family:'Sora',sans-serif; font-weight:800; font-size:2rem;
  color:#4B2A6B; line-height:1; }}
.r-top .r-pct small {{ display:block; font-size:.62rem; letter-spacing:.08em; text-transform:uppercase; color:{c['muted']}; font-weight:600; }}
.r-row {{ grid-template-columns:minmax(150px,1.2fr) 2fr 56px; }}
.r-row em {{ text-align:right; color:{c['tx']}; font-weight:700; }}

/* ---------- Informe gerencial y simulador de rol ---------- */
.v-area {{ background:{c['surface']}; border:1px solid {c['border']}; border-radius:14px; padding:10px 14px; margin-bottom:8px; }}
.scn {{ background:linear-gradient(120deg,rgba(201,150,42,.12),rgba(232,194,90,.18)); border:1px solid {c['border']};
  border-left:5px solid {c['a1']}; border-radius:14px; padding:12px 16px; margin:10px 0 14px; color:{c['tx']}; }}
.r-card {{ background:linear-gradient(180deg,{c['surface']},{c['surface2']}); border:1px solid {c['border']};
  border-radius:20px; padding:20px 24px; margin:14px 0; position:relative; overflow:hidden; }}
.r-card::before {{ content:''; position:absolute; left:0; right:0; top:0; height:5px;
  background:linear-gradient(90deg,{c['a1']},{c['a2']}); }}
.r-card p, .r-card li {{ color:{c['tx']}; margin:6px 0; }}
.r-top {{ display:flex; align-items:center; gap:14px; margin-bottom:6px; }}
.r-ico {{ font-size:2.2rem; width:62px; height:62px; display:grid; place-items:center; border-radius:18px;
  background:linear-gradient(135deg,rgba(201,150,42,.2),rgba(232,194,90,.3)); }}
.r-top small {{ color:{c['muted']}; text-transform:uppercase; letter-spacing:.1em; font-size:.68rem; font-weight:600; }}
.r-name {{ font-family:'Sora',sans-serif; font-weight:800; font-size:1.35rem; color:#4B2A6B; line-height:1.15; }}
.r-bars {{ margin-top:14px; }}
.r-row {{ display:grid; grid-template-columns:minmax(150px,1.2fr) 2fr 52px; gap:10px; align-items:center; margin-top:7px;
  font-size:.85rem; color:{c['tx']}; }}
.r-row em {{ font-style:normal; color:{c['muted']}; font-weight:600; font-size:.78rem; }}
.r-track {{ background:{c['surface2']}; border:1px solid {c['border']}; border-radius:999px; height:12px; overflow:hidden; }}
.r-fill {{ height:100%; background:linear-gradient(90deg,{c['a1']},{c['a2']}); border-radius:999px; }}
@media (max-width:640px) {{ .r-row {{ grid-template-columns:1fr; }} }}

.hero {{ position:relative; overflow:hidden; display:flex; align-items:center; gap:24px; padding:26px 30px;
  border-radius:22px; margin-bottom:18px; border:1px solid {c['border']};
  background:linear-gradient(135deg,rgba(201,150,42,.18),rgba(232,194,90,.20) 55%,rgba(255,255,255,.75)); }}
.hero::after {{ content:'✿'; position:absolute; right:34px; top:-38px; font-size:12rem; line-height:1;
  color:rgba(201,150,42,.34); pointer-events:none; }}
.hero::before {{ content:'❀'; position:absolute; right:230px; bottom:-40px; font-size:6rem; line-height:1;
  color:rgba(232,194,90,.40); pointer-events:none; }}
.hero > * {{ position:relative; z-index:1; }}
.hero img {{ width:96px; height:96px; border-radius:22px; box-shadow:0 10px 28px rgba(201,150,42,.38);
  object-fit:cover; background:#fff; flex-shrink:0; }}
.hero h1 {{ margin:0; font-size:2.2rem; font-weight:800; padding:0; line-height:1.05; letter-spacing:.06em;
  background:linear-gradient(90deg,#4B2A6B,{c['a1']} 50%,#C9962A); -webkit-background-clip:text;
  background-clip:text; -webkit-text-fill-color:transparent; }}
.hero .meaning {{ margin:4px 0 8px; font-family:'Sora'; font-size:1.02rem; font-weight:500; color:{c['tx']}; }}
.hero .meaning .acr, .sb-brand .acr {{ color:#5B2E8C; font-weight:800; }}
.hero p {{ margin:0 0 10px; color:{c['muted']}; max-width:760px; }}
.chip {{ display:inline-block; font-size:.74rem; font-weight:600; padding:4px 11px; margin:0 6px 4px 0;
  border-radius:999px; border:1px solid {c['border']}; background:rgba(255,255,255,.8); color:{c['tx']}; }}
.chip.author {{ border-color:{c['a1']}; color:#4B2A6B; }}

.card {{ background:linear-gradient(180deg,{c['surface']},{c['surface2']}); border:1px solid {c['border']};
  border-radius:16px; padding:15px 18px; height:100%; position:relative; overflow:hidden; }}
.card::before {{ content:''; position:absolute; left:0; top:0; right:0; height:4px;
  background:linear-gradient(90deg,{c['a1']},{c['a2']}); }}
.card .lbl {{ color:{c['muted']}; font-size:.7rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; }}
.card .val {{ font-family:'Sora'; font-size:1.65rem; font-weight:700; color:{c['tx']}; margin:2px 0; }}
.card .sub {{ color:{c['muted']}; font-size:.78rem; }}

.agent {{ display:flex; gap:12px; align-items:center; background:{c['surface']}; border:1px solid {c['border']};
  border-radius:14px; padding:12px 16px; margin-bottom:8px; color:{c['tx']}; }}
.agent .dot {{ width:12px; height:12px; border-radius:50%; background:{c['border']}; flex-shrink:0; }}
.agent.done .dot {{ background:{c['ok']}; box-shadow:0 0 10px {c['ok']}; }}
.agent.ai .dot {{ background:{c['a1']}; box-shadow:0 0 10px {c['a1']}; }}
.agent small {{ color:{c['muted']}; }}

[class*="st-key-report"] {{ background:{c['surface']}; border:1px solid {c['border']}; border-left:4px solid {c['a1']};
  border-radius:16px; padding:10px 26px; }}
.step-n {{ display:inline-grid; place-items:center; width:26px; height:26px; border-radius:8px;
  background:linear-gradient(120deg,{c['a1']},{c['a2']}); color:#2B1B3D; font-weight:800; font-size:.8rem; margin-right:8px; }}
@media (max-width:640px) {{ .hero {{ flex-direction:column; align-items:flex-start; padding:18px; }}
  .hero h1 {{ font-size:1.8rem; }} }}
</style>"""


EXTRA_CSS = """
/* ===== Jinshi · corte imperial ===== */
.stApp [data-testid="stSidebar"] { border-right:2px solid #C9962A; }
.hero { background:linear-gradient(135deg,#FFFBEF 0%,#F8EBC8 60%,#EFD58B 100%) !important; border:2px solid #C9962A !important;
  box-shadow:0 14px 38px rgba(91,46,140,.22) !important; }
.hero::after { content:'❖' !important; color:rgba(91,46,140,.12) !important; }
.hero::before { content:'✦' !important; color:rgba(201,150,42,.30) !important; }
.hero img, .sb-brand img { object-fit:cover; object-position:center top; border:3px solid #C9962A; }
.hero img { box-shadow:0 10px 28px rgba(91,46,140,.35) !important; }
.hero h1 { color:#111111 !important; -webkit-text-fill-color:#111111 !important; background:none !important;
  text-shadow:0 2px 0 rgba(232,194,90,.7); }
.hero .meaning { color:#111111 !important; font-weight:600 !important; }
.hero p { color:#111111 !important; }
.hero .chip { background:#FFFFFF !important; color:#111111 !important; border:1px solid #C9962A !important; }
.hero .chip.author { background:#F6E3A1 !important; color:#111111 !important; border-color:#C9962A !important; font-weight:700 !important; }
.sb-brand b, .sb-brand small, .sb-author, .sb-author b { color:#111111 !important; }
h3, h4 { border-left:4px solid #C9962A; padding-left:10px; }

/* ---------- selector de temas ---------- */
.pick-title { font-family:'Sora',sans-serif; font-weight:700; font-size:1.05rem; color:#4B2A6B; margin:.2rem 0 .4rem; }
.corte-head { display:flex; align-items:center; gap:8px; font-family:'Sora',sans-serif; font-weight:700; color:#111111;
  background:linear-gradient(120deg,#F6E3A1,#E8C25A); border-radius:12px; padding:8px 14px; margin:6px 0 8px;
  border-bottom:3px solid #5B2E8C; }
.corte-head small { margin-left:auto; color:#111111; font-weight:700; }
[data-testid="stVerticalBlockBorderWrapper"] { transition:all .15s ease; }
[data-testid="stVerticalBlockBorderWrapper"]:has(input[type="checkbox"]:checked) {
  border-color:#C9962A !important; background:linear-gradient(180deg,#FFFBEF,#F8EBC8) !important;
  box-shadow:0 4px 16px rgba(201,150,42,.30) !important; }
.sel-bar { background:#EFE6F7; border:1px dashed #5B2E8C; border-radius:12px; padding:8px 12px; margin:8px 0 12px; color:#111111; }
.sel-bar b { color:#5B2E8C; }
.sel-chip { display:inline-block; background:#F6E3A1; color:#111111; border:1px solid #C9962A; border-radius:999px; padding:2px 10px; margin:2px 4px 2px 0; font-size:.78rem; font-weight:600; }

/* ---------- consejos ---------- */
.tip-box { background:linear-gradient(180deg,#FFFBEF,#FBF0D2); border:1px solid #E8C25A; border-left:5px solid #C9962A;
  border-radius:12px; padding:9px 14px; margin:8px 0; color:#111111; font-size:.93rem; }
.tip-box b { color:#111111; }
.err-box { background:#FBEDEA; border:1px solid #E3B3AD; border-left:5px solid #B5342B; border-radius:12px; padding:9px 14px; margin:8px 0;
  color:#111111; font-size:.93rem; }
.err-box b { color:#111111; }
.step-n { background:linear-gradient(120deg,#C9962A,#E8C25A) !important; color:#2B1B3D !important; }
/* ---------- consejo (popover con icono) ---------- */
.tip-head { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
.tip-head b { font-family:'Sora',sans-serif; font-size:1.05rem; color:#111111; }
.tip-head small { display:block; color:#2E2838; }
.tip-icon { border-radius:50%; object-fit:cover; border:3px solid #C9962A; box-shadow:0 4px 14px rgba(91,46,140,.35); }
[data-testid="stPopover"] button { background:linear-gradient(120deg,#E8C25A,#C9962A) !important; color:#111111 !important;
  border:0 !important; font-weight:700 !important; }
[data-testid="stPopoverBody"], [data-testid="stPopoverBody"] * { color:#111111; }
[data-testid="stSidebar"] *, [data-testid="stTabs"] button p { color:#111111; }
"""


def css() -> str:
    return _base_css().replace("</style>", EXTRA_CSS + "</style>")


def hero_html() -> str:
    return (f'<div class="hero">{_logo_img()}'
            f'<div><h1>{NOMBRE}</h1>'
            f'<div class="meaning">{_significado_html()}</div>'
            '<p>Elige tus temas, estudia las fórmulas con ejemplos paso a paso y genera talleres o '
            'exámenes aleatorios que puedes descargar en PDF.</p>'
            f'<span class="chip author">❖ Por {AUTORA}</span>'
            '<span class="chip">Tema: Jinshi (壬氏) · Los diarios de la boticaria</span>'
            '<span class="chip">Primer y segundo corte</span></div></div>')


def sidebar_brand_html() -> str:
    return (f'<div class="sb-brand">{_logo_img()}<div><b>{NOMBRE}</b>'
            f'<small>{_significado_html()}</small></div></div>'
            f'<div class="sb-author">Autor · <b>{AUTORA}</b></div>')


def style_fig(fig, h: int = 380):
    """Plotly cálido y transparente: se ve bien sobre el fondo crema."""
    fig.update_layout(
        template="plotly_white", colorway=PALETA, height=h, margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["tx"], family="Inter"), title_font=dict(family="Sora", size=15, color=C["tx"]),
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(gridcolor="#E9DDBF", zerolinecolor=C["border"]),
        yaxis=dict(gridcolor="#E9DDBF", zerolinecolor=C["border"]))
    return fig

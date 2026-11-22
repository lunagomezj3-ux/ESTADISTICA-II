"""
pdf_export.py · PDF de talleres y exámenes
------------------------------------------
Dibuja el enunciado, las tablas, las fórmulas (LaTeX → imagen con matplotlib mathtext) y, si se pide,
la solución paso a paso. Usa solo fuentes estándar del PDF: las letras griegas del texto se escriben
con su nombre (alfa, mu, sigma) y los emojis se quitan.
"""

from __future__ import annotations

import io
import re
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape as xesc

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.lib.utils import ImageReader  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, Image, KeepTogether, PageBreak,  # noqa: E402
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

import content as ct  # noqa: E402
import theme  # noqa: E402

WINE, ROSE, PEACH = colors.HexColor("#8E2347"), colors.HexColor("#F2668B"), colors.HexColor("#FFA94D")
TX, MUTED = colors.HexColor("#4A2B2B"), colors.HexColor("#7A5750")
BORDER, SOFT, OKBG = colors.HexColor("#E6BC9F"), colors.HexColor("#FFF1E4"), colors.HexColor("#E9F7EE")

_MAP = {"α": "alfa", "β": "beta", "μ": "mu", "σ": "sigma", "→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≠": "!=",
        "✿": "", "❀": "", "✓": "", "·": "-"}
DPI = 220


def clean(t: str) -> str:
    for a, b in _MAP.items():
        t = t.replace(a, b)
    return re.sub(r"[ \t]{2,}", " ", t.encode("cp1252", "ignore").decode("cp1252"))


def _inline(t: str) -> str:
    t = xesc(clean(t))
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


@lru_cache(maxsize=4096)
def _math_png(latex: str, size: float = 12.5) -> bytes:
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, f"${latex}$", fontsize=size, color="#4A2B2B")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, bbox_inches="tight", pad_inches=0.04, transparent=True)
    plt.close(fig)
    return buf.getvalue()


def math_flowable(latex: str, max_w: float):
    """Imagen de la fórmula; si no se puede dibujar, el LaTeX queda como texto."""
    try:
        png = _math_png(latex)
        w_px, h_px = ImageReader(io.BytesIO(png)).getSize()
        w, h = w_px * 72 / DPI, h_px * 72 / DPI
        if w > max_w:
            h, w = h * max_w / w, max_w
        im = Image(io.BytesIO(png), width=w, height=h)
        im.hAlign = "CENTER"
        return im
    except Exception:  # noqa: BLE001
        return Paragraph(xesc(clean(latex)), ParagraphStyle("raw", fontName="Courier", fontSize=8, textColor=TX))


def _styles():
    b = dict(fontName="Helvetica", textColor=TX, fontSize=10, leading=14.5)
    return {
        "p": ParagraphStyle("p", spaceAfter=4, **b),
        "step": ParagraphStyle("step", leftIndent=10, spaceAfter=2, **b),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=WINE, spaceBefore=10, spaceAfter=3, keepWithNext=1),
        "tag": ParagraphStyle("tag", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=3),
        "sol": ParagraphStyle("sol", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ROSE, spaceBefore=4, spaceAfter=2),
        "ans": ParagraphStyle("ans", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=TX),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=TX, alignment=1),
        "head": ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.white, alignment=1),
    }


def _tabla(rows, st):
    data = [[Paragraph(xesc(clean(c)), st["head"] if j == 0 else st["cell"]) for c in r] for j, r in enumerate(rows)]
    # primera fila = encabezado visual (valores de x); la segunda trae las probabilidades
    t = Table(data, hAlign="CENTER")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), WINE), ("BACKGROUND", (0, 1), (0, -1), SOFT),
                           ("GRID", (0, 0), (-1, -1), 0.5, BORDER), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    return t


def _logo() -> Path | None:
    for ext in ("png", "jpg", "jpeg"):
        f = Path(__file__).parent / "assets" / f"logo_univalle.{ext}"
        if f.exists():
            return f
    return None


def problem_flowables(i, p, st, width, *, solucion, formulas, puntos=None):
    t = ct.TOPICS[p["tema"]]
    pts = f" · {puntos:g} pts" if puntos else ""
    out = [Paragraph(f"Ejercicio {i}", st["h"]),
           Paragraph(xesc(clean(f"{t['nombre']} · Nivel {p['nivel']}{pts}")), st["tag"]),
           Paragraph(_inline(p["enunciado"]), st["p"])]
    if p.get("tabla"):
        out += [Spacer(1, 3), _tabla(p["tabla"], st), Spacer(1, 4)]
    if formulas and p["formulas"]:
        out.append(Paragraph("Fórmulas de ayuda", st["sol"]))
        out += [math_flowable(f, width - 20) for f in p["formulas"]]
    if solucion:
        out.append(Paragraph("Solución paso a paso", st["sol"]))
        for k, (txt, m) in enumerate(p["pasos"], 1):
            blk = [Paragraph(_inline(f"**Paso {k}.** {txt}"), st["step"])]
            if m:
                blk.append(math_flowable(m, width - 20))
            out.append(KeepTogether(blk))
        box = Table([[Paragraph(_inline("Respuesta: " + p["respuesta"]), st["ans"])]], colWidths=[width])
        box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), OKBG), ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#4CAF7A")),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        out += [Spacer(1, 4), box]
    else:
        out.append(Spacer(1, 3.6 * cm))   # espacio para resolver a mano
    out.append(HRFlowable(width="100%", thickness=0.6, color=BORDER, spaceBefore=6, spaceAfter=2))
    return out


def build_pdf(titulo: str, problems: list[dict], *, solucion=False, formulas=False, examen=False,
              nivel="", codigo="", autora=theme.AUTORA) -> bytes:
    buf = io.BytesIO()
    W, H = letter
    L = R = 2 * cm
    logo = _logo()

    def deco(c, doc):
        c.saveState()
        c.setFillColor(ROSE); c.rect(0, H - 0.45 * cm, W * 0.6, 0.45 * cm, stroke=0, fill=1)
        c.setFillColor(PEACH); c.rect(W * 0.6, H - 0.45 * cm, W * 0.4, 0.45 * cm, stroke=0, fill=1)
        if logo:
            try:
                c.drawImage(str(logo), W - R - 3.2 * cm, H - 1.75 * cm, width=3.2 * cm, height=1.1 * cm,
                            preserveAspectRatio=True, anchor="ne", mask="auto")
            except Exception:  # noqa: BLE001
                pass
        c.setStrokeColor(BORDER); c.setLineWidth(0.6); c.line(L, 1.5 * cm, W - R, 1.5 * cm)
        c.setFont("Helvetica", 8); c.setFillColor(MUTED)
        c.drawString(L, 1.0 * cm, clean(f"Simulador Estadistica 2 - {autora} - Codigo {codigo}"))
        c.drawRightString(W - R, 1.0 * cm, f"Pagina {doc.page}")
        c.restoreState()

    doc = BaseDocTemplate(buf, pagesize=letter, leftMargin=L, rightMargin=R, topMargin=2.2 * cm, bottomMargin=2.0 * cm,
                          title=clean(titulo), author=clean(autora))
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(L, 2.0 * cm, W - L - R, H - 4.2 * cm, id="f", leftPadding=0,
                                                              rightPadding=0, topPadding=0, bottomPadding=0)], onPage=deco)])
    st = _styles()
    width = W - L - R
    tema_nombres = []
    for p in problems:
        n = ct.TOPICS[p["tema"]]["nombre"]
        if n not in tema_nombres:
            tema_nombres.append(n)
    story = [Paragraph("ESTADISTICA 2", ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=WINE)),
             Paragraph(xesc(clean(titulo)), ParagraphStyle("tt", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=TX, spaceAfter=6))]
    meta = [("Temas", "; ".join(tema_nombres)), ("Nivel", nivel), ("Ejercicios", str(len(problems))),
            ("Codigo", codigo), ("Fecha", datetime.now().strftime("%d/%m/%Y %H:%M"))]
    if examen and not solucion:
        meta += [("Nombre", "_" * 38), ("Tiempo sugerido", f"{max(30, 12 * len(problems))} minutos")]
    mt = Table([[Paragraph(f"<b>{xesc(clean(k))}</b>", st["tag"]), Paragraph(xesc(clean(v)), st["tag"])] for k, v in meta if v],
               colWidths=[3.2 * cm, width - 3.2 * cm])
    mt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SOFT), ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                            ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [mt, Spacer(1, 6)]
    if examen and not solucion:
        story.append(Paragraph("Resuelva cada ejercicio mostrando el procedimiento. Puede usar calculadora y tablas Z y t.", st["tag"]))
    pts = round(5 / len(problems), 2) if examen and problems else None
    for i, p in enumerate(problems, 1):
        story += problem_flowables(i, p, st, width, solucion=solucion, formulas=formulas, puntos=pts)
    doc.build(story)
    return buf.getvalue()

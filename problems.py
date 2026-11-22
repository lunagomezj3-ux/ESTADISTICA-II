"""
problems.py · Registro de generadores y armado de talleres / exámenes
---------------------------------------------------------------------
Los ejercicios son aleatorios pero reproducibles: la misma semilla (código) da el mismo taller.
"""

from __future__ import annotations

import random

import content as ct
import gen_c1 as c1
import gen_c2 as c2

REGISTRY: dict[str, dict[str, list]] = {
    "normal": {"Fácil": [c1.gen_normal_prob, c1.gen_normal_se],
               "Medio": [c1.gen_normal_prob, c1.gen_normal_inv, c1.gen_normal_xbar],
               "Difícil": [c1.gen_normal_prob, c1.gen_normal_inv, c1.gen_normal_xbar]},
    "discretas": {"Fácil": [c1.gen_disc_esperanza, c1.gen_disc_k], "Medio": [c1.gen_disc_k], "Difícil": [c1.gen_disc_lineal]},
    "binomial": {"Fácil": [c1.gen_bin_exact], "Medio": [c1.gen_bin_cum, c1.gen_bin_exact], "Difícil": [c1.gen_bin_hard, c1.gen_bin_cum]},
    "ph1": {"Fácil": [c1.gen_ph1_errores, c1.gen_ph1_z], "Medio": [c1.gen_ph1_z], "Difícil": [c1.gen_ph1_z, c1.gen_ph1_beta]},
    "ic": {"Fácil": [c2.gen_ic_zcrit, c2.gen_ic_interp, c2.gen_ic_elegir], "Medio": [c2.gen_ic_margen, c2.gen_ic_n],
           "Difícil": [c2.gen_ic_n, c2.gen_ic_margen]},
    "ic_media": {"Fácil": [c2.gen_ic_z], "Medio": [c2.gen_ic_z, c2.gen_ic_t], "Difícil": [c2.gen_ic_t, c2.gen_ic_datos]},
    "plant": {n: [c2.gen_plantea] for n in ct.NIVELES},
    "pvalor": {"Fácil": [c2.gen_p_z], "Medio": [c2.gen_p_t, c2.gen_p_z], "Difícil": [c2.gen_p_completo, c2.gen_p_t]},
    "regla": {"Fácil": [c2.gen_regla_crit], "Medio": [c2.gen_regla_comp], "Difícil": [c2.gen_regla_t]},
    "ph2": {"Fácil": [c2.gen_ph_prop], "Medio": [c2.gen_ph_prop, c2.gen_ph_t], "Difícil": [c2.gen_ph_t, c2.gen_ph_prop]},
}

NIVELES_UI = ct.NIVELES + ["Mixto"]


def make_one(tema: str, nivel: str, rng: random.Random) -> dict:
    gen = rng.choice(REGISTRY[tema][nivel])
    return gen(rng, nivel)


def _clave(p: dict) -> str:
    """Identifica un ejercicio: el enunciado y, si la hay, su tabla de datos."""
    return p["enunciado"] + repr(p.get("tabla"))


def generate_set(temas: list[str], n: int, nivel: str, seed: int) -> list[dict]:
    """n ejercicios repartidos de forma equitativa entre los temas elegidos, ordenados según el programa."""
    rng = random.Random(seed)
    temas = list(temas)
    orden = rng.sample(temas, len(temas))          # qué temas quedan con un ejercicio extra si n no es múltiplo
    asignados = [orden[i % len(orden)] for i in range(n)]
    out, vistos = [], set()
    for tema in asignados:
        for _ in range(25):                        # evita enunciados repetidos
            niv = rng.choice(ct.NIVELES) if nivel == "Mixto" else nivel
            p = make_one(tema, niv, rng)
            if _clave(p) not in vistos:
                break
        vistos.add(_clave(p))
        out.append(p)
    prog = {t: i for i, t in enumerate(ct.TOPICS)}
    out.sort(key=lambda p: prog[p["tema"]])
    return out

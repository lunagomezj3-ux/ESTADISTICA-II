# Simulador de Estadística 2

App Streamlit para aprender, practicar y evaluarte (sin cargar datos).

## Temas
**Primer corte:** normal (población y muestra), distribuciones discretas, binomial, prueba de hipótesis (z).
**Segundo corte:** intervalos de confianza, IC para la media, planteamiento de hipótesis, valor P, regla de decisión,
prueba de hipótesis (t y proporción).

## Pestañas
- **Aprender**: teoría, fórmulas y un ejemplo resuelto paso a paso (botón «Otro ejemplo»).
- **Taller / Examen**: eliges temas, cantidad, nivel (fácil, medio, difícil, mixto); solo se muestran las preguntas.
  «Ver resultados» despliega procedimiento, fórmula y respuesta. PDF del taller y solucionario descargables.
- **Formulario**: todas las fórmulas juntas.

## Instalación
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Archivos
```
app.py        Interfaz
content.py    Temas, teoría y fórmulas (editable)
pbase.py      Utilidades comunes (contextos, pasos de hipótesis)
gen_c1.py     Generadores del primer corte
gen_c2.py     Generadores del segundo corte
problems.py   Registro por tema/nivel y armado de talleres
pdf_export.py PDF con fórmulas (matplotlib) y soluciones
theme.py      Colores y estilos
```
Para agregar un tipo de ejercicio: escribe `gen_xxx(rng, nivel)` que devuelva `mk(...)` y añádelo a `REGISTRY` en `problems.py`.

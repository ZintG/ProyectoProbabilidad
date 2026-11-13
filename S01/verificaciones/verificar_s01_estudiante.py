"""Verificación de S01 para el paquete del estudiante (v0.9).

Sustituye, en este paquete, a verificar_s01_v05.py, que exige material
docente (s01_docente.tex, sol01.pdf, solej01.pdf) y por eso falla aquí.
Conserva sus aserciones numéricas y comprueba que NO haya soluciones.

Uso (desde sesiones/S01):  python3 verificaciones/verificar_s01_estudiante.py [--estricto]
Con --estricto, la ausencia de los PDF de estudiante enlazados es un error;
sin él, se informa como PENDIENTE.
"""
import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # sesiones/S01
PROY = ROOT.parents[1]                              # raíz del proyecto
ESTRICTO = "--estricto" in sys.argv

# 1. Experimento didáctico: mismas aserciones numéricas que v0.5
subprocess.run([sys.executable, str(ROOT / "codigo" / "experimento_s01.py")],
               check=True, capture_output=True, text=True)
r = list(csv.DictReader((ROOT / "experimentos" / "resultados_python.csv").open(encoding="utf-8")))
j = json.loads((ROOT / "experimentos" / "resumen_python.json").read_text(encoding="utf-8"))
assert len(r) == j["n_prueba"] == 6
assert all(int(v["caracteres"]) > 0 and float(v["bpc_general"]) > 0 and float(v["bpc_tecnico"]) > 0 for v in r)
assert math.isclose(sum(float(v["delta_bpc"]) for v in r) / 6, j["delta_promedio_bpc"], abs_tol=1e-8)
assert math.isclose(j["delta_promedio_bpc"], -0.54024842, abs_tol=1e-8)
assert all(math.isclose(g, e, abs_tol=1e-8)
           for g, e in zip(j["ic_percentil_bootstrap_pareado_95"], [-0.66770598, -0.42038147]))
assert j["datos"] == "SINTETICOS_CREADOS_PARA_ENSENAR"

# 2. Fuentes de estudiante presentes
for f in ("contenido_libro.tex", "p01.tex", "s01_integrada.tex", "labmat01.tex", "labcomp01.tex",
          "t01.tex", "reportes/reporte_s01.tex", "reportes/reporte_ejemplo_ejecutado.tex"):
    assert (ROOT / f).exists(), f

# 3. Ninguna solución en el paquete del estudiante
prohibidos = [p for pat in ("sol*.tex", "sol*.pdf", "solej*", "*docente*", "*solucionario*")
              for p in PROY.rglob(pat)
              if "fuentes_historicas" not in p.parts and "fuentes_integradas_v0_7" not in p.parts]
assert not prohibidos, f"Material docente en el paquete: {prohibidos}"

# 4. PDF enlazados desde la presentación interactiva (decisión 3-A)
faltan = [f"{d.relative_to(PROY)}/{n}.pdf"
          for d in (PROY / "presentaciones" / "pdf", ROOT / "pdf")
          for n in ("s01_integrada", "labcomp01", "t01", "reporte_ejemplo_ejecutado")
          if not (d / f"{n}.pdf").exists() or (d / f"{n}.pdf").stat().st_size < 4000]
if faltan:
    msg = f"PDF de estudiante ausentes: {faltan}"
    if ESTRICTO:
        raise AssertionError(msg)
    print("PENDIENTE:", msg)

print("S01 v0.9 (estudiante): experimento, intervalo bootstrap, fuentes y ausencia de soluciones verificados")

"""Control de calidad técnica (Regla 7) para una sesión del libro.

Uso, desde la raíz del proyecto:
    python3 sesiones/S01/verificaciones/control_latex.py S01

Comprueba, sin modificar nada:
  1. caracteres de control y tabulaciones (escapes perdidos: «\\t» -> TAB);
  2. remisiones residuales a estructuras retiradas («suplemento», «parte II», «la guía»);
  3. referencias y citas sin resolver en libro.log (si existe);
  4. enlaces de la presentación interactiva (.Rmd y .html) a archivos inexistentes.
Devuelve código 1 si encuentra algún problema. Reutilizable en S02-S12.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SES = sys.argv[1] if len(sys.argv) > 1 else "S01"
NUM = SES[1:]

# Módulos que entran en los PDF empaquetados (labcompXX, tXX, sXX_integrada).
_EMPAQ = [ROOT / f"sesiones/{SES}/{n}.tex" for n in (f"labcomp{NUM}", f"t{NUM}", f"s{NUM}_integrada")]
_MODS = sorted({ROOT / f"sesiones/{SES}" / (m + ".tex")
                for f in _EMPAQ if f.exists()
                for m in re.findall(r"\\input\{(modulos/[^}]+)\}", f.read_text(encoding="utf-8"))})
ARCHIVOS_TEX = [
    ROOT / f"sesiones/{SES}/contenido_libro.tex",
    ROOT / f"sesiones/{SES}/p{NUM}.tex",
    *_MODS,
]
PRESENTACIONES = [
    ROOT / f"presentaciones/{SES}/p{NUM}_interactiva.Rmd",
    ROOT / f"presentaciones/{SES}/p{NUM}_interactiva.html",
    ROOT / f"sesiones/{SES}/presentacion/p{NUM}_interactiva.Rmd",
    ROOT / f"sesiones/{SES}/presentacion/p{NUM}_interactiva.html",
]
RESIDUALES = [
    (r"\bel suplemento\b|\bdel suplemento\b|\bal suplemento\b", "remisión a «el suplemento»"),
    (r"\bparte (I|II|III|IV)\b", "remisión a «parte …»"),
    (r"\bsiguiente parte\b", "remisión a «la siguiente parte»"),
    (r"\b(la|esta|en la) guía\b", "remisión a «la guía»"),
]
CONTROL = re.compile(r"[\x00-\x08\x09\x0b-\x1f⇥�]")

problemas = []


def rel(p):
    return p.relative_to(ROOT)


for f in ARCHIVOS_TEX + PRESENTACIONES:
    if not f.exists():
        continue
    es_tex = f.suffix == ".tex"
    for i, linea in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        if CONTROL.search(linea):
            problemas.append(f"[control]   {rel(f)}:{i}: {linea.strip()[:80]!r}")
        if es_tex and not linea.lstrip().startswith("%"):
            for patron, nombre in RESIDUALES:
                if re.search(patron, linea, flags=re.IGNORECASE):
                    problemas.append(f"[residual]  {rel(f)}:{i}: {nombre}")

log = ROOT / "libro.log"
if log.exists():
    texto = log.read_text(encoding="latin-1")
    for m in sorted(set(re.findall(r"(?:Reference|Citation) `[^']+' on page \d+ undefined", texto))):
        problemas.append(f"[sin_res.]  libro.log: {m}")

for f in PRESENTACIONES:
    if not f.exists():
        continue
    texto = f.read_text(encoding="utf-8", errors="replace")
    enlaces = re.findall(r"\]\(([^)#\s]+)\)", texto) + re.findall(r'(?:href|src)="([^"#]+)"', texto)
    for e in sorted(set(enlaces)):
        if re.match(r"^(https?:|mailto:|data:|javascript:)", e):
            continue
        if not (f.parent / e).exists():
            problemas.append(f"[enlace]    {rel(f)}: {e}")

print(f"control_latex {SES}: {len(problemas)} problema(s)")
for p in problemas:
    print("  " + p)
sys.exit(1 if problemas else 0)

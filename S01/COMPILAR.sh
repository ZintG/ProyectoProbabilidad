#!/usr/bin/env bash
# S01 v0.9: compila los PDF del paquete del estudiante (sin soluciones) y los
# copia a sesiones/S01/pdf/ y a presentaciones/pdf/, donde los enlazan las dos
# copias de la presentación interactiva.
#   s01_integrada            texto de la sesión tal como entra al libro (con complementos)
#   labcomp01, t01           laboratorio computacional y taller (módulos)
#   reporte_ejemplo_ejecutado  informe de ejemplo
# labmat01 y sup01 ya no se empaquetan: su contenido está en s01_integrada.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p _build pdf ../../presentaciones/pdf
BIB=bibtex
compilar () {  # $1 nombre
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=_build "$1.tex" >/dev/null
  if grep -q '\\bibdata' "_build/$1.aux"; then
    (cd _build && BIBINPUTS='..:../../../bibliografia:' BSTINPUTS='../bib:..:' "$BIB" "$1" >/dev/null)
  fi
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=_build "$1.tex" >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=_build "$1.tex" >/dev/null
  if grep -qE "Reference .* undefined|Citation .* undefined" "_build/$1.log"; then
    echo "AVISO: referencias o citas sin resolver en $1"; exit 3
  fi
  cp "_build/$1.pdf" "pdf/$1.pdf"
  cp "_build/$1.pdf" "../../presentaciones/pdf/$1.pdf"
}
for name in s01_integrada labcomp01 t01; do compilar "$name"; done
(cd reportes && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../_build reporte_ejemplo_ejecutado.tex >/dev/null \
  && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=../_build reporte_ejemplo_ejecutado.tex >/dev/null)
cp _build/reporte_ejemplo_ejecutado.pdf pdf/ && cp _build/reporte_ejemplo_ejecutado.pdf ../../presentaciones/pdf/
echo 'S01 v0.9: PDF de estudiante actualizados en pdf/ y en presentaciones/pdf/'

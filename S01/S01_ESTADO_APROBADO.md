# S01 — Índice de versión única vigente, v1.0 (17 de octubre de 2026)

**Versión de referencia docente para la producción del curso:** S01 v1.0, que consolida la guía modular v0.5 y la presentación interactiva v0.3 corregida. Las versiones anteriores quedan como historial y **no forman parte del material vigente**.

| Uso | Archivo vigente | Estado |
|---|---|---|
| Volumen de estudiante | `s01_integrada.tex` / `pdf/s01_integrada.pdf` | Referencia aprobada con experimentos separados |
| Edición docente y soluciones | `s01_docente.tex` / `pdf/s01_docente.pdf` | Acceso docente |
| Laboratorio matemático | `labmat01.tex` | Incluido en ambos volúmenes |
| Laboratorio computacional e IC10 | `labcomp01.tex`; `codigo/experimento_s01.py`; `codigo/ic10_tokenizadores.py` | Python verificado |
| Complementos R | `codigo/experimento_s01.R`; `codigo/ic10_tokenizadores.R` | Pendiente equivalencia numérica |
| Presentación dinámica principal | `presentacion/p01_interactiva.Rmd` y `.html` | Rmd v0.3 compiló según confirmación docente; cambios v1.0 pendientes de render nativo; HTML incluye experimento IC10 |
| Guion docente | `presentacion/GUION_DOCENTE_S01.md` | Unificado con `docencia/PLAN_S01_FINAL.md` |
| Taller y ejercicios | `t01.tex`, `ej01.tex` y sus soluciones en la edición docente | Cinco actividades y reporte |
| Suplemento matemático | `sup01.tex` | Consulta autónoma |
| Plantilla y ejemplo de reporte | `reportes/reporte_s01.tex`, `reportes/reporte_ejemplo_ejecutado.tex` | Comparación de predictor y de tokenizador |
| Bibliografía | `bib/s01_referencias.bib`, `BIBLIOGRAFIA_S01.md` | Maestra y listado contextual |
| Beamer | `p01.tex` | Respaldo histórico, no proyección principal |

**Compilación LaTeX:** dos pasadas `pdflatex`, `bibtex` y dos más de `pdflatex` (desde raíz). Código: `python codigo/experimento_s01.py && python codigo/ic10_tokenizadores.py`. `Rscript` solo donde exista. `presentacion/p01_interactiva.html` funciona estático con archivos vecinos; para modificar el contenido fuente, renderizar su Rmd en un entorno con R Markdown.

**Aceptación académica:** A01 cumple experimento de tokenizador didáctico; A02 paquete único; A03 plan docente único; A04 diferencias documentadas para arbitraje; A05 equivalencia R/Python acotada, pendiente ensayo numérico; A06 bibliografía maestra y navegación sujetas a mantenimiento ordinario. **No se declara validación presencial, certificación R ni aprobación institucional del cambio de programa.**

# Validación y cierre S01 v1.0

Fecha: 17 de octubre de 2026.

## Documentos compilados
| PDF | Páginas | Entradas de navegación | SHA-256 (prefijo) |
|---|---:|---:|---|
| `s01_integrada.pdf` | 61 | 90 | `c017dd8f696304ed88` |
| `s01_docente.pdf` | 66 | 92 | `53579d4c763ee799e3` |
| `labcomp01.pdf` | 12 | 16 | `2c8a9fbe4bc66d53ec` |
| `labmat01.pdf` | 10 | 18 | `d70c1dc39f5831f645` |
| `sup01.pdf` | 15 | 35 | `156fdd0c55553d3d9d` |
| `t01.pdf` | 3 | 1 | `57c138e79522157f6e` |
| `ej01.pdf` | 2 | 2 | `61b3a4a40a3d758989` |
| `reporte_ejemplo_ejecutado.pdf` | 2 | 6 | `97683848fb909bd22c` |
| `reporte_s01.pdf` | 2 | 7 | `b94d9d8df5fa3a33c1` |

## Evidencia automatizada
- Python: `codigo/experimento_s01.py`, `codigo/ic10_tokenizadores.py`, `verificaciones/verificar_s01.py`, `verificaciones/verificar_s01_v05.py` ejecutados. Tablas y JSON generados. La validación es local, sobre datos sintéticos.
- IC10 BPE: 35 palabras reservadas en seis documentos; BPE general 148 tokens, BPE técnico 127, con 20 fusiones cada uno; salida reproducida por Python.
- HTML: 19 pestañas con 19 paneles; panel 5.4 interactuó correctamente en Chromium mediante carga controlada de HTML, sin errores de JavaScript. La navegación a archivos `file://`/HTTP directos en Chromium fue restringida por el entorno de pruebas.
- R Markdown: el docente confirmó que el `.Rmd` anterior v0.3 compila en su equipo; el cambio v1.0 requiere verificación nativa; no se efectuó recompilación nativa con R en este entorno.
- R: implementación paralela escrita. `Rscript` no disponible; equivalencia numérica con Python no certificada. `verificaciones/comparar_r_python.py` devolverá PENDIENTE hasta que existan ambos CSV de R.
- PDF: inspección visual de portada, índice, laboratorio IC10 y bibliografía; no se observaron recortes en las páginas revisadas.
- Entrega curricular: diferencias con el Programa v0.4 documentadas para su arbitraje; no se asegura aprobación institucional.

## Criterios de cierre
- A01: implementado un experimento que cambia realmente tokenizador, con los límites científicos explicados.
- A02: paquete principal único e índice `S01_ESTADO_APROBADO.md`; histórico separado de documentos vigentes.
- A03: plan docente único; hora final dedicada a laboratorio, reporte e investigación. Tiempo pendiente de ensayo docente.
- A04: diferencias curriculares consignadas en `DIFERENCIAS_PROGRAMA_V04.md`, pendientes de arbitraje formal.
- A05: acotación explícita: Rmd compilado según confirmación docente, Python verificado, R pendiente; verificador de equivalencia disponible.
- A06: bibliografía maestra de S01, lista de diez referencias y navegación comprobada; mantenimiento editorial ordinario.

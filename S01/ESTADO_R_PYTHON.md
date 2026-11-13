# S01 v1.0 — Estado verificable de R / Python

**Python:** ejecutados `codigo/experimento_s01.py`, `codigo/ic10_tokenizadores.py`, `verificaciones/verificar_s01.py` y `verificaciones/verificar_s01_v05.py`. Resultados por documento en `experimentos/resultados_python.csv` y `experimentos/resultados_ic10_tokenizacion.csv`.

**R:** implementaciones paralelas `codigo/experimento_s01.R`, `codigo/ic10_tokenizadores.R`, y fuentes de representación. No se ejecutaron en el entorno de generación por ausencia de `Rscript`. El docente confirmó por separado que `p01_interactiva.Rmd` compila en su equipo; **la compilación del Rmd no certifica la coincidencia numérica de los programas R/Python**.

**Cómo certificar la paridad numérica en el equipo del docente** (desde la raíz S01):

```bash
python codigo/experimento_s01.py
python codigo/ic10_tokenizadores.py
Rscript codigo/experimento_s01.R
Rscript codigo/ic10_tokenizadores.R
python verificaciones/comparar_r_python.py
```

La comprobación compara por ID los resultados BPC y los conteos BPE y exige desviación máxima `<= 2e-6`. Las tablas de BPE deben coincidir exactamente en tokens, palabras y IDs. Registrar R/Python, sesión/locale, fecha, logs y diferencias. **Hasta ejecutar estos comandos y conservar evidencia, el estado es: Python verificado, R pendiente.**

Para HTML: widgets JavaScript ejecutan controles; resultados sintéticos fueron precalculados con Python; no hay motor R/Python remoto en el navegador.


## Actualización v0.9 (31-10-2026)

**R ejecutado en el entorno de revisión** (R 4.3.3, 2024-02-29) con `LC_ALL=C.UTF-8`:

- `codigo/experimento_s01.R`: Δ BPC = −0.5402484; IC bootstrap pareado enumerado = [−0.667706, −0.4203815].
- `codigo/ic10_tokenizadores.R`: tokens BPE general = 148, técnico = 127.
- `verificaciones/comparar_r_python.py`: «concordancia por documento; desviaciones máximas BPC=0, BPE=0».

**Correcciones necesarias para ejecutar R** (no cambian ningún número): `write.csv(..., encoding='UTF-8')` → `write.csv(..., fileEncoding='UTF-8')` en `experimento_s01.R` (l. 57) e `ic10_tokenizadores.R` (l. 67); el argumento `encoding` no existe en `write.csv` y detenía ambos programas.

**Requisito de configuración regional:** con `LC_CTYPE=POSIX`, `ic10_tokenizadores.R` segmenta mal los caracteres acentuados (149/152 tokens en lugar de 148/127, con advertencias). Ejecutar R con una configuración UTF-8.

Salidas incorporadas al paquete: `experimentos/resultados_R.csv` y `experimentos/resultados_ic10_R.csv`.
**Estado: Python verificado; R verificado (paridad exacta) en configuración UTF-8.**

# Informe de Investigación Git y Análisis Exhaustivo de Modificaciones Post-Pull

**Autor:** Agente Explorer Git (Teamwork)  
**Fecha de análisis:** 2026-11-20  
**Repositorio:** `/home/simon/Documentos/UC-Probabilidad`  
**Rama activa:** `main` (sincronizada con `origin/main` en el commit `3c88bbf`)  
**Rango de actualización analizado:** `394f4c2..3c88bbf` (Último `git pull`)

---

## 1. Resumen Ejecutivo

El 20 de noviembre de 2026 a las 17:46:17 -0400 se ejecutó una operación de actualización (`git pull origin main: Fast-forward`) que avanzó la rama local `main` desde el commit `394f4c2` (Semana 2: modelos de n-gramas, ceros en validación y calibración de $\alpha$) hasta el commit `3c88bbf` (docs: cierra el checklist de seguridad y actualiza la entrega final).

Esta actualización incorporó un total de **9 commits consecutivos**, todos realizados por el usuario `enrique13valerocastillo-beep`, que abarcan la culminación íntegra de la **Semana 3** (Fases 4, 5 y 6, más verificación interna de resultados) y la totalidad de la **Semana 4** (redacción del reporte técnico formal en LaTeX de 14 páginas, formalización de las 11 preguntas de discusión, suite de reproducibilidad en un solo comando `codigo/main.py`, congelamiento de métricas y empaquetado final).

### Estadísticas Consolidadas del Pull (`394f4c2..3c88bbf`):
- **Commits incorporados:** 9 commits.
- **Archivos impactados:** 37 archivos en total.
  - **Archivos nuevos añadidos:** 30
  - **Archivos modificados:** 4
  - **Archivos renombrados / reubicados:** 3 (traslados directos sin cambio de contenido, similitud 100%)
  - **Archivos eliminados:** 0
- **Balance de líneas:** +3 798 adiciones / -39 eliminaciones (más múltiples archivos binarios correspondientes a figuras vectoriales PDF/PNG, reporte compilado PDF y el paquete de entrega ZIP).
- **Estado del árbol de trabajo actual:** Completamente limpio; no existen cambios pendientes ni archivos bajo seguimiento modificados. La única ruta sin seguimiento (`untracked`) es el directorio de metadatos de agentes `.agents/`.

---

## 2. Historial de Git, Reflog y Sincronización Remota

### 2.1 Inspección del Reflog Local
La inspección del reflog mediante `git reflog --date=iso` reveló la cronología exacta de las operaciones de actualización en el clon local:

| Entrada de Reflog | Fecha y Hora (ISO) | Operación | Desde Commit | Hasta Commit | Contexto |
|---|---|---|---|---|---|
| `HEAD@{0}` | 2026-11-20 17:46:17 -0400 | `pull origin main: Fast-forward` | `394f4c2` | `3c88bbf` | **Último pull (objeto de este análisis)**: Semanas 3 y 4 completadas |
| `HEAD@{1}` | 2026-11-15 21:33:58 -0400 | `pull origin main: Fast-forward` | `ef6c322` | `394f4c2` | Pull previo: Incorporación de la Semana 2 |
| `HEAD@{2}` | 2026-11-14 17:48:34 -0400 | `pull origin main: Fast-forward` | `7d5b37c` | `ef6c322` | Pull inicial: Subida de archivos base |
| `HEAD@{3}` | 2026-11-12 22:52:26 -0400 | `commit` | `11c5234` | `7d5b37c` | Local: ignorar copia_conversacion.md |
| `HEAD@{4}` | 2026-11-12 22:47:51 -0400 | `commit` | `053c36b` | `11c5234` | Local: Decisión 8 sobre Git |
| `HEAD@{5}` | 2026-11-12 22:47:02 -0400 | `commit (initial)` | — | `053c36b` | Inicialización del repositorio (Fase 0) |

### 2.2 Estado Remoto y Árbol de Trabajo
- **Remoto configurado:** `origin -> https://github.com/ZintG/ProyectoProbabilidad.git` (fetch & push).
- **Alineación de ramas:** `main` local y `origin/main` apuntan exactamente al mismo commit (`3c88bbfa64b54fda0a89802924a02cf4902dee39`).
- **Estado de `git status`:**
  ```text
  En la rama main
  Tu rama está actualizada con 'origin/main'.
  Archivos sin seguimiento:
    .agents/
  no hay nada agregado al commit pero hay archivos sin seguimiento presentes
  ```
  No hay cambios locales desincronizados ni conflictos pendientes.

---

## 3. Cronología y Detalle de los 9 Commits Incorporados

A continuación se detalla cada uno de los commits transferidos en el pull, ordenados cronológicamente:

### Commit 1: `c457adf`
- **Fecha:** Miércoles 18 de noviembre de 2026, 23:52:10 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo@gmail.com>`
- **Mensaje:** `Semana 3: Fase 4 (T3, Gibbs, F3/F4 log) y Fase 5 (pi, muestras, F5)`
- **Archivos modificados/añadidos:** 17 archivos (+1 624 / -23 líneas).
- **Aportes clave:**
  - `codigo/fase1.py`: Script para extracción de frecuencias marginales, cálculo de entropía empírica y teórica máxima, y generación de la gráfica F1 y tabla T1.
  - `codigo/fase4.py`: Script de evaluación oficial única sobre el bloque de prueba (`datos/prueba.txt`), cálculo de BPC/perplejidad para $n \in \{1,\ldots,5\}$, comprobación de la Desigualdad de Gibbs para unigramas, y generación de F3 (BPC vs $n$) y F4 (convergencia LLN en escala logarítmica). Incorpora salvaguardas `--validar` y `--solo-f4`.
  - `codigo/fase5.py`: Simulación de texto (300 caracteres, semilla 2026, prefijo `"habia "`), construcción de la matriz de transición estocástica positiva $27 \times 27$ del bigrama suavizado, convergencia de distribución estacionaria $\pi$ por método de potencias y generación de F5.
  - `tablas/T3_evaluacion_prueba.csv`, `tablas/T3_gibbs.csv`, `tablas/T5_muestras.csv`.
  - `figuras/F3_bpc_n.*`, `figuras/F4_promedio_acumulado.*`, `figuras/F5_pi_unigramas.*`.
  - `notas_importantes/Preguntas_del_proyecto.md` y `.txt`: Banco inicial de preguntas conceptuales y de defensa.
  - `decisiones_informe.md`: Registro de secciones 13 (Fase 4) y 14 (Fase 5).
  - `resumen_revision_1.md`: Adición del criterio formal de selección de $\alpha^*$.

### Commit 2: `8eff616`
- **Fecha:** Jueves 19 de noviembre de 2026, 09:42:29 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo@gmail.com>`
- **Mensaje:** `Semana 3 cerrada: Fase 6 (bootstrap, T4) y revision interna`
- **Archivos modificados/añadidos:** 13 archivos (+1 069 / -61 líneas).
- **Aportes clave:**
  - `codigo/fase6.py`: Implementación del Bootstrap por bloques contiguos (16 bloques: 15 de 2 000 caracteres + 1 final de 1 579 caracteres; $B = 10\,000$ remuestreos percentiles al 95 %, semilla 2026) para contrastar $n=5$ vs $n=4$.
  - `codigo/verificar_todo.py`: Suite exhaustiva de verificación que reconstruye los modelos y recalcula independientemente 127 cifras contra las tablas del repositorio.
  - `tablas/T4_bootstrap.csv`, `tablas/T4_deltas_bloques.csv`, `tablas/verificacion_resultados.csv`.
  - `figuras/bootstrap_delta.*`: Histograma complementario no numerado del bootstrap de $\Delta_j$.
  - `revision_resultados.md`: Acta técnica de la revisión interna (127/127 pruebas OK).
  - `resumen_revision_2.md`: Documento de síntesis y consolidación de la Semana 3.
  - `decisiones_informe.md`: Sección 15 (Fase 6) y Sección 16 (Revisión interna).
  - `notas_importantes/Preguntas_del_proyecto.md` y `.txt`: Finalización de las 11 respuestas de discusión teórica.

### Commit 3: `611da9b`
- **Fecha:** Jueves 19 de noviembre de 2026, 10:24:26 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `Reorganiza F1 y T1 en figuras/ y tablas/`
- **Archivos modificados/añadidos:** 4 archivos (+3 líneas en `.gitignore`, 3 renames).
- **Aportes clave:**
  - Traslado ordenado de entregables desde la raíz del proyecto hacia sus respectivas carpetas modulares:
    - `F1_frecuencias.pdf` $\to$ `figuras/F1_frecuencias.pdf`
    - `F1_frecuencias.png` $\to$ `figuras/F1_frecuencias.png`
    - `T1_particiones.csv` $\to$ `tablas/T1_particiones.csv`
  - `.gitignore`: Se añade `/resumen_proyecto_probabilidad.pdf` para prevenir colisiones en la raíz.

### Commit 4: `ae1325a`
- **Fecha:** Jueves 19 de noviembre de 2026, 21:19:35 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `Agrega traspaso de la Semana 4`
- **Archivos modificados/añadidos:** 1 archivo (`notas_importantes/traspaso_semana4.md`, +82 líneas).
- **Aportes clave:**
  - Documento de continuidad operacional para transferir el contexto del proyecto a los integrantes encargados de redactar el informe en la Semana 4 sin requerir lectura de historiales previos.

### Commit 5: `bd7357f`
- **Fecha:** Viernes 20 de noviembre de 2026, 08:17:22 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `docs(reporte): agrega reporte técnico en LaTeX y PDF de la Tarea 1`
- **Archivos modificados/añadidos:** 5 archivos (+695 / -1 líneas).
- **Aportes clave:**
  - `reporte/reporte.tex` y `reporte/reporte.pdf`: Redacción y compilación completa del reporte técnico oficial de 14 páginas de cuerpo, organizado en 8 secciones obligatorias más portada y 3 anexos.
  - `codigo/fase4.py`: Ajuste menor de formateo numérico (`.4g`) para presentar BPC con 4 cifras significativas en la leyenda de F4, y regeneración de `figuras/F4_promedio_acumulado.*`.

### Commit 6: `253d7d0`
- **Fecha:** Viernes 20 de noviembre de 2026, 08:29:46 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `docs(reporte): formaliza las 11 respuestas de discusión teórica`
- **Archivos modificados/añadidos:** 3 archivos (+51 / -57 líneas).
- **Aportes clave:**
  - Ampliación rigurosa de la Sección 7 del reporte técnico en LaTeX, integrando ecuaciones numeradas, referencias cruzadas y respuestas formales a los 11 puntos conceptuales exigidos en la rúbrica oficial.
  - Condensación armónica de las secciones 1 a 6 para mantener el cuerpo estricto en 13 páginas numeradas (14 con portada).

### Commit 7: `cf8dffb`
- **Fecha:** Viernes 20 de noviembre de 2026, 08:38:23 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `docs: agrega flujo unico, dependencias fijadas y README reproducible`
- **Archivos modificados/añadidos:** 4 archivos (+374 / -2 líneas).
- **Aportes clave:**
  - `codigo/main.py`: Orquestador principal que ejecuta el flujo integral de 9 etapas en una sola orden de terminal, respetando el congelamiento de la evaluación en prueba y garantizando ejecución por debajo del límite de 10 minutos (tiempo medido: 39.14 segundos).
  - `requirements.txt`: Fijación exacta de dependencias (`numpy==2.2.4`, `matplotlib==3.10.1`).
  - `README.md`: Guía integral de instalación, ejecución individual/completa, compilación del reporte, estructura del repositorio y cifras congeladas.

### Commit 8: `22712d8`
- **Fecha:** Viernes 20 de noviembre de 2026, 09:09:24 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `docs: empaqueta la entrega final de la Semana 4`
- **Archivos modificados/añadidos:** 2 archivos.
- **Aportes clave:**
  - Generación del archivo empaquetado de entrega `Proyecto_probabilidad_31.678.578_21.129.684_33.638.501_30.445.947.zip` conteniendo los archivos del repositorio verificados por SHA-256 y CRC.
  - Actualización de casillas en `Tareas a realizar y orden.md`.

### Commit 9: `3c88bbf`
- **Fecha:** Viernes 20 de noviembre de 2026, 09:24:21 -0400
- **Autor:** `enrique13valerocastillo-beep <enrique13valerocastillo-beep@users.noreply.github.com>`
- **Mensaje:** `docs: cierra el checklist de seguridad y actualiza la entrega final`
- **Archivos modificados/añadidos:** 4 archivos (+15 / -10 líneas).
- **Aportes clave:**
  - Incorporación en `reporte/reporte.tex` de la cita y referencia bibliográfica formal del libro de texto del curso (Luis Rincón, *Introducción a la Probabilidad*), logrando que las 6 referencias bibliográficas queden explícitamente citadas en el texto.
  - Verificación y marcado formal de las 8 casillas del checklist de seguridad en `Tareas a realizar y orden.md`.
  - Regeneración optimizada del ZIP de entrega (reducción de tamaño de 11.4 MB a 5.8 MB al excluir copias internas recursivas de `.git`), conservando exactamente 157 archivos.

---

## 4. Inventario Completo y Análisis Detallado de Archivos

A continuación se presenta el catálogo exhaustivo de los 37 archivos involucrados en el pull, clasificados por naturaleza y rol dentro de la arquitectura del proyecto:

### 4.1 Scripts de Código Python (`codigo/`)

| Archivo | Estado | Líneas | Función y Descripción Técnica |
|---|:---:|:---:|---|
| `codigo/main.py` | **Añadido** | 134 | **Orquestador Maestro del Pipeline:** Encadena de forma secuencial las 9 etapas del proyecto (`preparar.py` $\to$ `pruebas.py` $\to$ `fase1.py` $\to \cdots \to$ `verificar_todo.py`). Monitorea y reporta los tiempos de ejecución de cada fase y el tiempo acumulado (39.14 s). Implementa control estricto de no repetición de la evaluación de prueba: detecta la existencia de `tablas/T3_evaluacion_prueba.csv` y omite automáticamente `fase4.py` para preservar el aislamiento de prueba. Admite parámetros `--max-segundos` (default 600) y `--sin-limite`. |
| `codigo/fase1.py` | **Añadido** | 157 | **Exploración del Corpus y Entropía Marginal:** Carga las tres particiones (`entrenamiento.txt`, `validacion.txt`, `prueba.txt`), calcula el conteo y distribución de frecuencias marginales de unigramas en entrenamiento ($N = 252\,626$, $|\mathcal{V}| = 27$). Calcula la entropía empírica de unigramas $H(\hat p) = 4.0592$ bits, la entropía teórica máxima $H_{\max} = \log_2(27) = 4.7549$ bits y la redundancia relativa $R = 14.63\,\%$. Exporta `tablas/T1_particiones.csv` y genera `figuras/F1_frecuencias.pdf` y `.png`. |
| `codigo/fase4.py` | **Añadido** | 269 | **Evaluación Oficial de Prueba y Validación de Leyes Teóricas:** Toma los modelos de $n$-gramas ($n \in \{1,\ldots,5\}$) entrenados sobre entrenamiento con los hiperparámetros óptimos fijados en validación ($\alpha^*(1)=1.0, \alpha^*(2)=0.001, \alpha^*(3)=0.1, \alpha^*(4)=0.03, \alpha^*(5)=0.03$). Evalúa una única vez el bloque de prueba heredando contexto final ($n-1$ caracteres). Calcula BPC de entrenamiento y prueba, así como Perplejidad ($2^{\text{BPC}}$). Demuestra numéricamente la Desigualdad de Gibbs ($H(\hat p) \le H(\hat p, \hat q)$) y calcula la divergencia KL ($0.006433$ bits). Genera F3 (comparación de BPC train vs test contra $n$) y F4 (convergencia asintótica del promedio acumulado de sorpresa $S_k$, LLN, en escala horizontal logarítmica). Protegido contra sobreescritura accidental (requiere `--forzar` o `--solo-f4`). |
| `codigo/fase5.py` | **Añadido** | 172 | **Cadenas de Markov y Generación Estocástica:** Construye la matriz de transición empírica estocástica $P$ ($27 \times 27$) para el modelo bigrama con suavizado $\alpha = 0.001$. Verifica que todas las filas sumen 1 (desviación máxima $\le 2.22 \times 10^{-16}$) y que todas las probabilidades sean estrictamente positivas ($P_{ij} \ge 2.207 \times 10^{-8}$), asegurando irreducibilidad y aperiodicidad. Calcula la distribución estacionaria $\pi$ por iteración de potencias (converge en 22 pasos con tolerancia $\ell_1 < 10^{-10}$). Compara $\pi$ con las frecuencias de unigramas (diferencia máxima $3.71 \times 10^{-6}$, distancia $\ell_1 = 9.05 \times 10^{-6}$). Genera 3 secuencias de 300 caracteres ($n \in \{2, 3, 5\}$, semilla 2026, prefijo `"habia "`). Exporta `tablas/T5_muestras.csv` y `figuras/F5_pi_unigramas.*`. |
| `codigo/fase6.py` | **Añadido** | 199 | **Cuantificación de Incertidumbre por Bootstrap de Bloques:** Compara el modelo óptimo ($n=5$) contra el competidor inmediato ($n=4$) sobre los 31 579 caracteres de prueba particionados en 16 bloques contiguos (15 bloques de 2 000 caracteres y 1 bloque final de 1 579 caracteres). Calcula en cada bloque $\Delta_j = \text{BPC}_j(n=4) - \text{BPC}_j(n=5)$. Aplica bootstrap percentil de $B = 10\,000$ remuestras con semilla 2026 a nivel del 95 %. Obtiene una media $\bar\Delta = 0.0926$ bits, IC 95 % $[0.0553, 0.1259]$ (estrictamente positivo, excluye el cero en su totalidad, confirmando la superioridad estadística de $n=5$). Realiza análisis de sensibilidad descartando el bloque incompleto (15 bloques: $\bar\Delta = 0.1031$, IC $[0.0711, 0.1326]$). Genera `tablas/T4_bootstrap.csv`, `tablas/T4_deltas_bloques.csv` y `figuras/bootstrap_delta.*`. |
| `codigo/verificar_todo.py` | **Añadido** | 256 | **Suite de Auditoría y Verificación Interna:** Reconstruye de manera completamente independiente todos los conteos y modelos desde los archivos crudos de `datos/`. Recalcula punto por punto 127 magnitudes numéricas reportadas a lo largo de las tablas T1–T5, Gibbs, F1–F5 y Bootstrap. Comprueba la coincidencia exacta o bajo tolerancias analíticas estrictas. Exporta el reporte tabular completo en `tablas/verificacion_resultados.csv` arrojando un resultado perfecto: 127 verificadas OK, 0 fallas. |

*(Nota: Los scripts `codigo/preparar.py`, `codigo/pruebas.py`, `codigo/modelos.py`, `codigo/fase2.py` y `codigo/fase3.py` ya existían con anterioridad en el commit `394f4c2` y no sufrieron alteraciones en este intervalo).*

---

### 4.2 Documentación del Reporte Técnico (`reporte/`)

| Archivo | Estado | Tamaño / Líneas | Función y Descripción Técnica |
|---|:---:|:---:|---|
| `reporte/reporte.tex` | **Añadido** | 693 líneas | **Documento Fuente LaTeX del Reporte Final:** Cumple con la estructura de la guía (Portada del Equipo 05, Resumen con cifras clave, Secciones 1 a 8, Referencias con 6 citas, y Anexos A, B y C). La Sección 7 desarrolla detalladamente las 11 respuestas teóricas obligatorias de la rúbrica. El Anexo A incluye la deducción formal de la MLE con multiplicadores de Lagrange. El Anexo B especifica las condiciones de reproducibilidad. El Anexo C reporta las muestras generadas y la declaración de IA. Utiliza `geometry` (2.5 cm), `booktabs`, `amsmath`, `microtype`, y vincula figuras vectoriales vía `\graphicspath{{../figuras/}}`. Longitud de cuerpo ajustada rigurosamente a 14 páginas (1 de portada + 13 de cuerpo) y 16 páginas en total con anexos. |
| `reporte/reporte.pdf` | **Añadido** | 244 586 bytes | **PDF Compilado Oficial:** Documento final listo para entrega, renderizado con tipografía vectorial y alta resolución. |

---

### 4.3 Documentación de Bitácora, Guías y Repositorio

| Archivo | Estado | Líneas | Función y Descripción Técnica |
|---|:---:|:---:|---|
| `README.md` | **Añadido** | 236 | **Guía de Reproducibilidad y Documentación General:** Contiene especificaciones de entorno (Python 3.13.5, NumPy 2.2.4, Matplotlib 3.10.1, Tectonic), instrucciones de instalación en entorno virtual, ejecución en comando único vía `python3 codigo/main.py`, ejecución fase por fase, protocolo de prueba ciega, compilación de LaTeX, estructura de carpetas, tabla consolidada de cifras congeladas y solución de problemas comunes. |
| `requirements.txt` | **Añadido** | 2 | **Dependencias Fijadas:** Especifica versiones exactas probadas sin librerías de NLP externas: `numpy==2.2.4` y `matplotlib==3.10.1`. |
| `decisiones_informe.md` | **Modificado** | +112 líneas | **Bitácora de Decisiones Metodológicas:** Se añadieron las Secciones 11 a 16: Cierre de Semana 2 y Revisión 1 (Sec. 11), Criterio y Justificación analítica de la elección de $\alpha^*$ (Sec. 12), Evaluación única de Fase 4 y salvaguardas (Sec. 13), Cadenas de Markov y ergodicidad de Fase 5 (Sec. 14), Justificación de Bootstrap por bloques contiguos de 2000 caracteres de Fase 6 (Sec. 15), y Acta de Revisión Interna de 127 verificaciones numéricas (Sec. 16). |
| `Tareas a realizar y orden.md` | **Modificado** | +78 / -39 | **Plan Maestro y Checklist de Entrega:** Actualización de todo el plan de trabajo reflejando las 6 fases completadas. Marcado con evidencia verificada de las 8 casillas del Checklist de Seguridad previo al empaquetado final (resumen con $n=5$, glosario, prueba ciega, test abracadabra 6/6, tablas T1-T4 y F1-F5, 11 preguntas, 6 referencias y tiempo de ejecución < 10 min). Documenta la justificación del nombre asignado al archivo ZIP con las 4 cédulas de identidad. |
| `notas_importantes/Preguntas_del_proyecto.md` | **Añadido** | 504 | **Banco de Preguntas Teóricas y de Defensa:** Documento exhaustivo con 55 preguntas divididas en 6 bloques: Bloque 1 (11 preguntas oficiales del enunciado respondidas con cifras de los datos), Bloque 2 (conceptos clave de teoría de la información y evaluación), Bloque 3 (decisiones metodológicas y blindaje), Bloque 4 (detalles matemáticos y derivaciones), Bloque 5 (preguntas trampa y de contraargumentación para la defensa oral) y Bloque 6 (registro de tareas cerradas). |
| `notas_importantes/Preguntas_del_proyecto.txt` | **Añadido** | 504 | **Copia en Texto Plano:** Versión espejo exacta en `.txt` para lectura directa en terminal o editores sin soporte markdown. |
| `notas_importantes/traspaso_semana4.md` | **Añadido** | 82 | **Acta de Handoff Operativo:** Síntesis técnica de traspaso redactada al cerrar la Semana 3 para coordinar el trabajo de redacción de la Semana 4 sin ambigüedades. |
| `resumen_revision_1.md` | **Modificado** | +2 líneas | **Consolidado de Revisión 1:** Incorporación del párrafo formal justificando el criterio de minimización de BPC en validación para los valores $\alpha^*$. |
| `resumen_revision_2.md` | **Añadido** | 131 | **Consolidado Narrativo de Semana 3:** Resumen ejecutivo de las Fases 4, 5 y 6, documentando los hallazgos numéricos principales para su integración en los capítulos de Resultados y Discusión del reporte. |
| `revision_resultados.md` | **Añadido** | 144 | **Acta Técnica de Revisión Interna:** Registro detallado de la auditoría interna cruzada realizada con `codigo/verificar_todo.py`, detallando el desglose de las 127 pruebas en 8 bloques de comprobación. |
| `.gitignore` | **Modificado** | +3 líneas | **Reglas de Exclusión Git:** Añade `/resumen_proyecto_probabilidad.pdf` en la raíz para evitar duplicados con el archivo localizado en `resumen/`. |

---

### 4.4 Tablas de Datos (`tablas/`)

| Archivo | Estado | Registros | Contenido y Significado Numérico |
|---|:---:|:---:|---|
| `tablas/T1_particiones.csv` | **Reubicado** | 4 filas | Trasladado desde `T1_particiones.csv`. Tamaño y porcentaje de particiones: Entrenamiento ($252\,626$ caracteres, $80.00\,\%$), Validación ($31\,578$ caracteres, $10.00\,\%$), Prueba ($31\,579$ caracteres, $10.00\,\%$), Total ($315\,783$ caracteres, $100.00\,\%$). |
| `tablas/T3_evaluacion_prueba.csv` | **Añadido** | 5 filas | Resultados congelados de la evaluación oficial en prueba para $n=1,\ldots,5$ con sus respectivos $\alpha^*$ fijados: BPC de entrenamiento (4.0592, 3.2354, 2.6872, 2.1538, 1.7320), BPC de prueba (4.0536, 3.2122, 2.7223, 2.3461, 2.2514) y Perplejidad de prueba (16.605, 9.268, 6.599, 5.085, 4.761). Mejor modelo: $n=5$. |
| `tablas/T3_gibbs.csv` | **Añadido** | 1 fila | Verificación numérica de la Desigualdad de Gibbs para unigramas: Entropía empírica de prueba $H(p) = 4.047143$ bits, Entropía cruzada $H(p, q) = 4.053576$ bits, y divergencia Kullback-Leibler $KL(p \parallel q) = 0.006433$ bits. Confirma $H(p) \le H(p,q)$. |
| `tablas/T4_bootstrap.csv` | **Añadido** | 1 fila | Resumen del contraste bootstrap $n=5$ vs $n=4$: media de $\Delta_j = 0.092644$ bits, IC 95 % percentil $[0.055343, 0.125915]$, 10 000 remuestras, 16 bloques, semilla 2026, `excluye_cero = si`. |
| `tablas/T4_deltas_bloques.csv` | **Añadido** | 16 filas | Detalle por bloque contiguo: columnas `bloque`, `inicio`, `fin`, `longitud`, `bpc_n4`, `bpc_n5`, `delta`. Permite observar que 14 de los 16 bloques presentan ventaja para $n=5$ ($\Delta > 0$), mientras que los bloques 15 y 16 (epílogo) favorecen a $n=4$. |
| `tablas/T5_muestras.csv` | **Añadido** | 3 filas | Textos sintéticos generados de 300 caracteres (longitud total 306 incluyendo prefijo `"habia "`, semilla 2026) para los modelos $n=2$, $n=3$ y $n=5$. |
| `tablas/verificacion_resultados.csv` | **Añadido** | 127 filas | Tabla exhaustiva de auditoría interna cruzada: registra para cada una de las 127 comprobaciones la variable, el valor reportado, el valor recalculado, la diferencia absoluta, la tolerancia permitida y el estado (`OK`). |

---

### 4.5 Figuras Gráficas (`figuras/`)

| Archivo | Estado | Formatos | Contenido y Relevancia en el Informe |
|---|:---:|:---:|---|
| `figuras/F1_frecuencias.*` | **Reubicado** | PDF / PNG | Trasladado desde la raíz. Gráfico de barras de las frecuencias relativas empíricas de los 27 símbolos del vocabulario en entrenamiento, ordenados decrecientemente. Muestra la dominancia del espacio ($17.89\,\%$) y de `#` ($8.10\,\%$). |
| `figuras/F3_bpc_n.*` | **Añadido** | PDF / PNG | Curvas comparativas de BPC en función del orden $n \in \{1,\ldots,5\}$ para entrenamiento y prueba. Evidencia visualmente la bifurcación a partir de $n=3$, demostrando el fenómeno de sobreajuste estructural de los modelos de n-gramas de orden superior. |
| `figuras/F4_promedio_acumulado.*` | **Añadido** | PDF / PNG | Curva del promedio acumulado de sorpresa $S_k$ a lo largo de las 31 579 posiciones de prueba con eje horizontal en escala logarítmica. Ilustra las fluctuaciones iniciales y la convergencia asintótica hacia el BPC final ($2.251$ bits), en concordancia con la Ley de los Grandes Números (LLN). |
| `figuras/F5_pi_unigramas.*` | **Añadido** | PDF / PNG | Comparación gráfica de barras adyacentes entre la distribución estacionaria calculada $\pi$ y las frecuencias relativas marginales de unigramas, demostrando visualmente su cuasi-coincidencia (diferencia máxima del orden de $10^{-6}$). |
| `figuras/bootstrap_delta.*` | **Añadido** | PDF / PNG | Histograma complementario de la distribución bootstrap de las medias de $\Delta_j$ (10 000 remuestras) con líneas de la media ($0.0926$), los extremos del IC del 95 % ($[0.0553, 0.1259]$) y la línea de referencia cero, evidenciando que toda la masa muestral se encuentra en el semiplano positivo. |

---

### 4.6 Paquete Comprimido de Entrega Final

| Archivo | Estado | Tamaño | Contenido y Verificación |
|---|:---:|:---:|---|
| `Proyecto_probabilidad_31.678.578_21.129.684_33.638.501_30.445.947.zip` | **Añadido** | 5 828 819 bytes (~5.8 MB) | Archivo empaquetado de entrega final. Contiene la réplica exacta de los 157 archivos del repositorio (excluyendo el historial interno `.git/`). Verificado mediante suma de comprobación SHA-256 y CRC32. Conserva la nomenclatura oficial definida y acordada por el equipo con las 4 cédulas de identidad de los integrantes. |

---

## 5. Síntesis de Resultados Numéricos y Teóricos Incorporados

Los commits del pull incorporan al proyecto un cuerpo coherente y cerrado de hallazgos estadísticos y probabilísticos:

1. **Parámetros del Corpus:**
   - Longitud total normalizada: 315 783 caracteres.
   - Partición 80/10/10 contigua: Entrenamiento = 252 626; Validación = 31 578; Prueba = 31 579 caracteres.
   - Vocabulario: $|\mathcal{V}| = 27$ caracteres (26 letras estándar del alfabeto sin 'w' + espacio `' '`, unificando tildes, 'ñ', dígitos y signos en `#`).
   - Entropía de unigramas en entrenamiento: $H(\hat p) = 4.0592$ bits frente al tope uniforme $\log_2(27) = 4.7549$ bits (Redundancia del $14.63\,\%$).

2. **Fallo de la MLE y Calibración de Suavizado Aditivo:**
   - La MLE produce BPC infinito en validación a partir de $n=3$ por la aparición de ceros ($n=3$: 50 ceros, 0.158 %; $n=4$: 491 ceros, 1.555 %; $n=5$: 2 171 ceros, 6.875 %). En $n=1$ y $n=2$ no hay ceros en validación.
   - Rejilla de $\alpha \in \{0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0\}$. Valores óptimos calibrados en validación y congelados:
     $\alpha^*(1)=1.0$, $\alpha^*(2)=0.001$, $\alpha^*(3)=0.1$, $\alpha^*(4)=0.03$, $\alpha^*(5)=0.03$.

3. **Evaluación Oficial de Prueba (Cifras Definitivas):**
   - $n=1$: BPC entreno = 4.0592, BPC prueba = 4.0536, PPL = 16.605
   - $n=2$: BPC entreno = 3.2354, BPC prueba = 3.2122, PPL = 9.268
   - $n=3$: BPC entreno = 2.6872, BPC prueba = 2.7223, PPL = 6.599
   - $n=4$: BPC entreno = 2.1538, BPC prueba = 2.3461, PPL = 5.085
   - $n=5$: BPC entreno = 1.7320, BPC prueba = **2.2514**, PPL = **4.761**
   - **Sobreajuste demostrado:** La brecha entre entrenamiento y prueba crece desde prácticamente cero en $n=1$ hasta $0.5194$ bits en $n=5$.

4. **Verificación Teórica de la Desigualdad de Gibbs:**
   - Para unigramas: $H(p_{\text{prueba}}) = 4.047143 \le H(p_{\text{prueba}}, q_{\alpha^*(1)}) = 4.053576$ bits.
   - Divergencia de Kullback-Leibler: $KL(p \parallel q) = 0.006433$ bits $\ge 0$.

5. **Ergodicidad de la Cadena de Markov (Bigrama):**
   - Matriz $P$ ($27 \times 27$): Estocástica (filas suman 1 con error $\le 2.22 \times 10^{-16}$) y estrictamente positiva ($P_{ij} \ge 2.207 \times 10^{-8}$).
   - Teorema ergódico verificado: La distribución estacionaria $\pi$ converge en 22 iteraciones y reproduce las frecuencias de unigramas con diferencia máxima de $3.71 \times 10^{-6}$ y distancia $\ell_1 = 9.05 \times 10^{-6}$.

6. **Incertidumbre Estadística (Bootstrap por Bloques):**
   - 16 bloques de 2 000 caracteres en prueba.
   - Comparación $n=5$ vs $n=4$: $\bar\Delta = 0.0926$ bits, IC 95 % $[0.0553, 0.1259]$.
   - Al excluir el cero, la superioridad de $n=5$ sobre $n=4$ es estadísticamente significativa al $95\,\%$, aunque representa una reducción modesta de perplejidad del $6.6\,\%$.

7. **Consistencia Global y Blindaje:**
   - Suite `codigo/verificar_todo.py`: 127 comprobaciones independientes, 127 correctas, 0 fallidas.
   - Tiempo de ejecución integral (`codigo/main.py`): 39.14 segundos (ampliamente inferior a la cuota límite de 10 minutos).

---

## 6. Observaciones de Cumplimiento y Recomendaciones para la Auditoría

1. **Aislamiento de la Muestra de Prueba:**
   La implementación respeta estrictamente el protocolo de evaluación única ciega:
   - Los $\alpha^*$ fueron calibrados exclusivamente sobre validación.
   - El script `codigo/main.py` y `codigo/fase4.py` impiden la reevaluación repetida de prueba.
2. **Nomenclatura del Archivo ZIP:**
   En la guía general se propone la convención `P1_EquipoNN_Apellido1_Apellido2.zip`. No obstante, el repositorio contiene el archivo `Proyecto_probabilidad_31.678.578_21.129.684_33.638.501_30.445.947.zip`. Esta decisión fue documentada expresamente en el checklist de `Tareas a realizar y orden.md` (commit `3c88bbf`) como una convención deliberada del equipo para asegurar la identificación unívoca de las cédulas de los 4 integrantes. El auditor debe considerar si es necesario conservar ambos nombres o generar un enlace simbólico/copia con la nomenclatura alternativa.
3. **Extensión del Documento en LaTeX:**
   El archivo `reporte/reporte.tex` cuenta con 1 portada + 13 páginas de cuerpo numerado (total 14 páginas de cuerpo), más 3 páginas de anexos (total 16 páginas). Esto satisface la restricción estricta de 10 a 14 páginas para el cuerpo principal del reporte.
4. **Respuestas de Discusión:**
   Las 11 preguntas obligatorias del enunciado están formalizadas con ecuaciones y referencias cruzadas en la Sección 7 (`7.1` a `7.11`) de `reporte/reporte.tex`, y respaldadas exhaustivamente en `notas_importantes/Preguntas_del_proyecto.md`.

---
*Fin del reporte de análisis de Git.*

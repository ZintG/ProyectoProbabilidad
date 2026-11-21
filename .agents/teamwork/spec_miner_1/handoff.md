# Handoff Report — Specification & Rubric Mining
**Agent:** `spec_miner_1`  
**Date:** 2026-11-20T22:09:00Z  
**Type:** Hard Handoff (Task Complete)

---

## 1. Observation

1. **Enunciado y Rúbrica Oficial (`proyecto_S01_probabilidad.pdf`):**
   - Extraído vía `pdftotext` resultando en 663 líneas distribuidas en 9 páginas.
   - **Pregunta central:** *«¿Cuánto mejora la predicción del siguiente carácter al aumentar la memoria del modelo (el orden n de un modelo de n-gramas) y a partir de qué orden deja de compensar por falta de datos?»* (§1, líneas 19–21).
   - **Restricciones de datos:** Corpus en español $\ge 300\,000$ caracteres de dominio público / Project Gutenberg; normalización obligatoria (minúsculas, colapso de espacios `\s+` a `' '`, sustitución de símbolos fuera de alfabeto por un único símbolo `#`); partición contigua 80/10/10 en ese orden sin barajar; evaluación única del conjunto de prueba al final (§3, líneas 150–171).
   - **Prueba de cordura:** Texto `"abracadabra"` con valores obligatorios exactos: entropía unigramas $2.0404$ bits, MLE bigrama $\hat{q}(b\mid a) = 0.5$, Laplace $\alpha=1, |V|=5 \implies 0.3333$, BPC bigrama MLE $0.6$ bits, PPL $1.5157$ (§3, Tabla 2, líneas 181–199).
   - **Fases del proyecto:** Fases 1 a 6 obligatorias, Fase 7 (BPE) opcional de hasta +10 puntos extra. Requiere tablas T1–T4 y figuras F1–F5. 11 preguntas en cursiva obligatorias en la sección de discusión (§4, líneas 200–315).
   - **Formato del reporte:** 10 a 14 páginas en PDF sin anexos, tamaño carta, márgenes de 2.5 cm, fuente 11 pt, interlineado 1.15, páginas numeradas, punto decimal, 4 cifras significativas en BPC/PPL, tablas con título arriba, figuras con leyenda abajo, cero capturas de pantalla, fragmentos de código $\le 15$ líneas (§5.1–5.2, líneas 316–410).
   - **Estructura del ZIP:** `P1_EquipoNN_Apellido1_Apellido2.zip` con subcarpeta raíz y archivos `reporte.pdf`, `README.md`, `requirements.txt`, `datos/FUENTE.md`, `codigo/{preparar,modelos,experimentos,pruebas}.py`, `resultados/` (§5.3, líneas 418–444).
   - **Rúbrica (100 pts + 10 extra):** Marco probabilístico y deducciones (20 pts), Implementación y verificaciones (20 pts), Resultados y análisis (25 pts), Incertidumbre y protocolo (10 pts), Reproducibilidad (10 pts), Redacción y formato (15 pts), Fase 7 opcional (+10 pts) (§6, Tabla 4, líneas 467–599).
   - **Penalizaciones:** $-10$ pts/día de retraso (máx 2 días); uso de prueba para elegir $\alpha$ o $n$ anula 10 pts de Incertidumbre y protocolo; reporte sin código obtiene máx 50 pts; copia o cifras no producidas por código anula el proyecto (§6, líneas 600–602, 644–645).

2. **Memoria Técnica y Bitácora (`decisiones_informe.md`):**
   - Obra elegida: *Niebla* de Miguel de Unamuno (Project Gutenberg #49836, 12-nov-2026), 315 783 caracteres netos tras limpieza de preámbulo, nota de transcripción (459 car.) e índice (750 car.) (§1–2, líneas 7–24).
   - Alfabeto: 26 letras inglesas (`a`–`z`, sin `w` por no usarse en la obra) + `' '` + token `#` que absorbe acentos, `ñ`, dígitos y puntuación $\implies |\mathcal{V}|=27$ (§5, líneas 39–51).
   - Particiones contiguas exactas: Entrenamiento $252\,626$ (80%), Validación $31\,578$ (10%), Prueba $31\,579$ (10%) (§6, líneas 53–62).
   - Verificaciones numéricas:
     - MLE: sumas condicionales con desviación máx $1.11 \times 10^{-16} < 10^{-12}$; log-verosimilitud MLE supera perturbaciones A y B (§9, líneas 98–116).
     - Validación ceros: $n=1,2 \implies 0$ ceros; $n=3 \implies 50$ ceros; $n=4 \implies 491$ ceros; $n=5 \implies 2171$ ceros (§9, líneas 118–127).
     - Calibración $\alpha^*(n)$: $n=1 \to 1.0$, $n=2 \to 0.001$, $n=3 \to 0.1$, $n=4 \to 0.03$, $n=5 \to 0.03$ (§10, líneas 158–165).
     - Evaluación de prueba: Mejor $n=5$ confirmado con BPC $2.2514$ y PPL $4.761$. Desigualdad de Gibbs en unigramas $KL = 0.006433$ bits. Ley de grandes números estabilizada en F4 (§13, líneas 221–235).
     - Matriz $P$: $27 \times 27$ estrictamente positiva ($P_{ij} \ge 2.2 \times 10^{-8}$); iteración de potencias converge en 22 pasos ($\|\Delta\|_1 = 3.35 \times 10^{-11} < 10^{-10}$); $\pi$ reproduce frecuencias de unigramas ($D_{\ell_1} = 9.05 \times 10^{-6}$) (§14, líneas 240–243).
     - Bootstrap: 16 bloques contiguos de prueba (15 de 2000 + 1 de 1579); media $\Delta_j = 0.0926$ bits; IC percentil 95% $[0.0553, 0.1259]$ excluye el 0 (§15, líneas 256–270).
     - Verificador general: `codigo/verificar_todo.py` ejecuta 127 aserciones numéricas: 127 correctas, 0 fallidas (§16, líneas 282–286).

3. **Fuentes Teóricas de S01 (`S01/`):**
   - Mapeo unívoco con `REGISTRO_TERMINOLOGIA_S01.md` y `CAMBIOS_S01_v0_9.md`: Def. 1.1.1 (Vocabulario), Def. 1.1.2 (BPE), Prop. 1.1.3 (Cadena), Def. 1.1.6 (Markov), Prop. 1.1.8 (MLE), Teo. 1.1.12 / Prop. 1.1.13–1.1.14 (Dirichlet y suavizado), §1.1.4 / Prop. 1.1.15 / Def. 1.1.17 / Prop. 1.1.18 (Entropía, Gibbs y KL), Def. 1.1.20 / Prop. 1.1.42 (BPC y PPL), Teo. 1.1.40 (Distribución estacionaria), Def. 1.1.44 (Bootstrap).

---

## 2. Logic Chain

1. **Delimitación del Problema:** La especificación autoritativa fija una frontera clara: modelar caracteres de un texto literario en español usando cadenas de Markov de órdenes $n-1 \in \{0, 1, 2, 3, 4\}$, con estimadores MLE y Laplace.
2. **Coherencia de Decisiones Metodológicas:** La bitácora `decisiones_informe.md` demuestra que el equipo implementó con exactitud matemática y conceptual cada una de las 6 fases obligatorias requeridas por el enunciado, respetando escrupulosamente el principio de aislamiento del bloque de prueba (usado una única vez en la Fase 4 tras congelar $\alpha^*$).
3. **Respuesta a Preguntas Teóricas:** El enunciado exige responder 11 preguntas en cursiva en la discusión (Sección 7 del reporte). Las 11 preguntas fueron extraídas y formalizadas con argumentos fundamentados en teoría de la información y procesos de Markov.
4. **Criterios de Evaluación y Tolerancias:** Se identificaron con precisión los 6 criterios cuantitativos de la rúbrica oficial (total 100 puntos), el criterio opcional de BPE (+10 puntos), las penalizaciones graves (como la anulación de 10 puntos por contaminación del conjunto de prueba), y las tolerancias matemáticas explícitas ($10^{-12}$ en sumas de condicionales, $10^{-10}$ en norma $\ell_1$ de iteración de potencias, tiempo de regeneración $< 10$ minutos, límite de páginas de 10 a 14 pp).
5. **Estructuración del Documento Final:** Con base en estas deducciones, se compuso `spec.md` en el directorio de trabajo del subagente conteniendo la matriz completa de características, catálogo de casos de borde, respuestas teóricas y mapeo con la bitácora y rúbrica.

---

## 3. Caveats

- **Fase 7 (BPE):** El enunciado contempla hasta +10 puntos extra por la implementación de BPE (200 fusiones). En `decisiones_informe.md` §16 se documenta que el equipo decidió de forma deliberada no abordarla para concentrarse en asegurar los 100 puntos de las 6 fases obligatorias. La especificación documenta el requisito completo por si el evaluador o el equipo decide auditarlo o implementarlo.
- **Número de páginas del PDF compilado actual:** `reporte/reporte.pdf` tiene actualmente 16 páginas en total (12 páginas de cuerpo principal más 4 páginas de anexos A, B y C). Dado que la restricción del enunciado es "10 a 14 páginas (sin contar anexos)", el cuerpo cumple el límite (12 pp $\in [10, 14]$), pero debe destacarse en la auditoría final para evitar confusiones de conteo bruto.

---

## 4. Conclusion

La especificación completa, técnica y formal del proyecto ha sido extraída y estructurada exhaustivamente en:
`/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/spec.md`

El documento proporciona el estándar de oro (*ground truth*) contra el cual los agentes de auditoría (`project_auditor_1`) y registro de cambios (`change_detector_1`) pueden contrastar el código, las salidas, las tablas, las figuras y el reporte técnico final para emitir el veredicto definitivo de cumplimiento frente a la rúbrica oficial de 100 puntos.

---

## 5. Verification Method

Para verificar independientemente la exactitud de esta extracción de especificaciones:

1. **Inspeccionar el documento de especificación generado:**
   ```bash
   test -f /home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/spec.md && echo "OK"
   ```
2. **Verificar concordancia con la extracción de texto del PDF oficial:**
   ```bash
   grep -E "(Pregunta central|Tabla 2|Tabla 4|10 a 14)" .agents/teamwork/spec_miner_1/pdf_full.txt
   ```
3. **Verificar batería de pruebas unitarias y consistencia numérica del proyecto:**
   ```bash
   python3 codigo/pruebas.py
   python3 codigo/verificar_todo.py
   ```
   *Condición de éxito:* Ambas suites deben reportar 0 errores y 127/127 verificaciones correctas.
4. **Verificar condiciones de invalidación:**
   - Si el archivo `spec.md` omite alguna de las 11 preguntas en cursiva o no incluye los criterios y ponderaciones exactas de la Tabla 4 del PDF, la especificación se considerará incompleta.

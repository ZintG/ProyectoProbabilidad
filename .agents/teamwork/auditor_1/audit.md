# Informe de Auditoría Técnica y Forense del Proyecto

**Proyecto:** Modelos de lenguaje de $n$-gramas sobre *Niebla* de Miguel de Unamuno  
**Curso:** Teoría de la Probabilidad (Quinto semestre) — Licenciatura en Computación, Universidad de Carabobo  
**Equipo:** Equipo 05 (Simón Tovar, Samuel Primera, Román Valero, Rolando Suárez)  
**Profesor:** Dr. José G. Marcano  
**Auditor:** Teamwork Forensic Auditor Agent  
**Fecha de Auditoría:** 20 de noviembre de 2026  
**Modo de Integridad:** Development (Desarrollo)  
**Veredicto General:** **APROBADO CON OBSERVACIONES MENORES DE FORMATO DE EMPAQUETADO (CALIDAD TÉCNICA Y MATEMÁTICA: EXCELENTE / 97-100 pts sobre 100)**

---

## 1. Resumen Ejecutivo y Veredicto de Integridad

Se ha completado una auditoría forense y técnica profunda y exhaustiva de todo el repositorio del proyecto (`/home/simon/Documentos/UC-Probabilidad`), examinando el código fuente, scripts de prueba y ejecución, datasets procesados, salidas tabulares (`tablas/*.csv`), representaciones gráficas (`figuras/*`), bitácoras de diseño (`decisiones_informe.md`), y el reporte técnico final en LaTeX y PDF (`reporte/reporte.tex`, `reporte/reporte.pdf`) contrastándolo punto por punto con los requisitos del enunciado oficial `proyecto_S01_probabilidad.pdf` y su rúbrica de evaluación.

### Veredicto Forense: **CLEAN (SIN VIOLACIONES DE INTEGRIDAD)**
- **Sin resultados prefabricados (hardcoded outputs):** Todos los algoritmos de conteo, estimación MLE, suavizado aditivo, cálculo de BPC/perplejidad, convergencia por iteración de potencias, simulación de Markov y remuestreo bootstrap ejecutan lógica matemática genuina desde los datos crudos.
- **Sin implementaciones fachada (facades):** Las clases y métodos en `codigo/modelos.py` y los scripts de cada fase realizan cómputos reales; no existen métodos dummy ni delegación oculta.
- **Sin delegación prohibida de ejecución:** No se emplean bibliotecas externas de modelos de lenguaje (`nltk.lm`, `kenlm`, `transformers`, `torch`, `scipy`). La totalidad del cómputo probabilístico fue desarrollada desde cero por el equipo en Python puro utilizando únicamente la biblioteca estándar.
- **Protocolo de prueba ciega respetado estrictamente:** La partición de prueba (`datos/prueba.txt`) no fue utilizada para ajustar hiperparámetros ni calibrar $\alpha$. Las decisiones de orden $n$ y $\alpha^*$ se tomaron exclusivamente con `datos/validacion.txt`. El script `fase4.py` implementa bloqueos automáticos para evitar reevaluaciones en prueba.
- **Verificación empírica completa:** La suite de verificación interna `codigo/verificar_todo.py` recalculó las 127 magnitudes numéricas del proyecto contra los datos brutos, obteniendo **127/127 comprobaciones correctas (0 fallos)** con tolerancias numéricas estrictas.

---

## 2. Registro y Análisis de Cambios Recientes (Git Pull / Semana 4)

Se inspeccionó el historial de Git entre el cierre de la Semana 3 (commit `8eff616`) y la cabeza actual `main` (commit `3c88bbf`). Se identificaron 7 commits que componen las adiciones y modificaciones recientes de la **Semana 4**:

| Hash | Fecha / Hora (-04) | Autor | Mensaje y Descripción del Cambio |
|:---|:---|:---|:---|
| `611da9b` | 2026-11-19 10:24 | Román Valero | **Reorganiza F1 y T1 en figuras/ y tablas/:** Mueve `F1_frecuencias.*` a `figuras/` y `T1_particiones.csv` a `tablas/`. Actualiza `.gitignore` con archivos temporales y `.agents/`. |
| `ae1325a` | 2026-11-19 21:19 | Román Valero | **Agrega traspaso de la Semana 4:** Crea `notas_importantes/traspaso_semana4.md` con el estado del proyecto, cifras congeladas, convenciones y tareas pendientes para la redacción final. |
| `bd7357f` | 2026-11-20 08:17 | Román Valero | **docs(reporte): agrega reporte técnico en LaTeX y PDF de la Tarea 1:** Incorpora `reporte/reporte.tex` y `reporte/reporte.pdf` inicial con estructura de 14 páginas, portada, tablas T1-T4, figuras F1-F5 y anexos A-C. Ajusta formato en `codigo/fase4.py` a 4 cifras significativas. |
| `253d7d0` | 2026-11-20 08:29 | Román Valero | **docs(reporte): formaliza las 11 respuestas de discusión teórica:** Redacta explícitamente las 11 preguntas en cursiva en la Sección 7 (7.1 a 7.11); condensa secciones 1 a 6 para mantener el cuerpo en 13 páginas (dentro del rango 10-14); actualiza checklist en `Tareas a realizar y orden.md`. |
| `cf8dffb` | 2026-11-20 08:38 | Román Valero | **docs: agrega flujo único, dependencias fijadas y README reproducible:** Crea `codigo/main.py` (flujo integral de 9 etapas con límite de 10 min), `requirements.txt` (`numpy==2.2.4`, `matplotlib==3.10.1`) y `README.md` exhaustivo con guía de instalación y ejecución. |
| `22712d8` | 2026-11-20 09:09 | Román Valero | **docs: empaqueta la entrega final de la Semana 4:** Genera el archivo ZIP inicial con hash de verificación. |
| `3c88bbf` | 2026-11-20 09:24 | Román Valero | **docs: cierra el checklist de seguridad y actualiza la entrega final:** Añade y cita referencia de Luis Rincón (*Introducción a la Probabilidad*); verifica 8 casillas del checklist; regenera el ZIP final excluyendo `.git` (reduciendo de 11.4 MB a 5.8 MB). |

### Inventario de Archivos Añadidos y Modificados en la Semana 4
1. **Código:**
   - `codigo/main.py` *(NUEVO, 134 líneas)*: Orquestador integral que ejecuta las etapas 1 a 9 en secuencia, mide tiempos por fase y tiempo total, omite `fase4.py` si T3 ya existe para preservar la evaluación única, y verifica el límite de 600 s.
   - `codigo/fase4.py` *(MODIFICADO, 2 líneas)*: Formato de BPC en leyenda de F4 cambiado a 4 cifras significativas (`.4g`).
2. **Documentación y Reporte:**
   - `reporte/reporte.tex` *(NUEVO, 693 líneas)*: Código fuente completo en LaTeX del reporte técnico.
   - `reporte/reporte.pdf` *(NUEVO, 244.6 KB, 16 páginas totales: portada + 12.2 páginas de cuerpo + 2.8 páginas de anexos)*: PDF compilado.
   - `README.md` *(NUEVO, 236 líneas)*: Manual de usuario, instalación, ejecución y solución de problemas.
   - `requirements.txt` *(NUEVO, 2 líneas)*: Fijación de dependencias externas.
   - `notas_importantes/traspaso_semana4.md` *(NUEVO, 82 líneas)*: Guía de traspaso interno.
   - `Tareas a realizar y orden.md` *(MODIFICADO)*: Checklist de Semana 4 marcado al 100%.
3. **Entregable empaquetado:**
   - `Proyecto_probabilidad_31.678.578_21.129.684_33.638.501_30.445.947.zip` *(NUEVO/ACTUALIZADO, 5.8 MB)*: Copia de archivos del repositorio.
4. **Figuras y Tablas:**
   - `figuras/F1_frecuencias.pdf` y `.png` *(REUBICADOS desde raíz a `figuras/`)*.
   - `tablas/T1_particiones.csv` *(REUBICADO desde raíz a `tablas/`)*.
   - `figuras/F4_promedio_acumulado.pdf` y `.png` *(REGENERADOS con 4 cifras significativas)*.

---

## 3. Auditoría de Datos, Preprocesamiento e Integridad Textual

| Aspecto Auditado | Requisito Oficial (PDF §3) | Estado en el Proyecto | Evaluación |
|:---|:---|:---|:---:|
| **Obra literaria** | Texto en español $\ge 300\,000$ caracteres, dominio público o licencia abierta, aprobado. | *Niebla (Nivola)* de Miguel de Unamuno (1914), Gutenberg #49836. | **CUMPLE** |
| **Metadatos de fuente** | Título, autor, URL y fecha de descarga en `datos/FUENTE.md` y reporte. | Registrados en `datos/FUENTE.md` y en la Sección 3 del reporte (descarga: 12/11/2026). | **CUMPLE** |
| **Limpieza de paratexto Gutenberg** | Eliminar preámbulo y licencia del archivo. | Preámbulo y licencia de Gutenberg eliminados en `Niebla_limpio.txt`. Además se eliminó nota de transcripción del digitalizador e índice de páginas final. | **CUMPLE** |
| **Paso a minúsculas** | Obligatorio: `.lower()`. | Implementado en `codigo/preparar.py` (`normalizar_texto`). | **CUMPLE** |
| **Colapso de espacios** | Colapsar espacios y saltos de línea repetidos en un solo espacio (`\s+` $\to$ `' '`). | Implementado mediante `re.sub(r"\s+", " ", texto_min).strip()`. | **CUMPLE** |
| **Alfabeto y sustituto `#`** | Reemplazar cualquier carácter fuera del alfabeto elegido por un único símbolo especial (ej. `#`). Alfabeto declarado en reporte. | Alfabeto permitido: `a`–`z` y espacio `' '`. Caracteres fuera (tildes, `ñ`, puntuación, dígitos) sustituidos por `#`. Declarado y analizado en Secciones 3 y 7 del reporte. | **CUMPLE** |
| **Vocabulario $|\mathcal{V}|$** | Fijado a partir de entrenamiento, típicamente entre 30 y 45 símbolos. | $|\mathcal{V}| = 27$ caracteres: `' #abcdefghijklmnopqrstuvxyz'` (la obra no contiene `w`). Consistente en entrenamiento, validación y prueba. | **CUMPLE** |
| **Extensión total** | $\ge 300\,000$ caracteres tras normalización. | **315 783 caracteres** ($\ge 300\,000$). | **CUMPLE** |
| **Partición contigua** | 80% entrenamiento, 10% validación, 10% prueba, contiguos, sin barajar. | Exactamente contigua: Train = 252 626 (80.0%), Val = 31 578 (10.0%), Test = 31 579 (10.0%). Concatenación exacta: `train + val + test == full`. | **CUMPLE** |
| **Contexto heredado en fronteras** | Contexto de primeras $n-1$ posiciones de validación/prueba tomado de partición anterior. | Implementado rigurosamente en `fase2.py`, `fase3.py`, `fase4.py`, `fase6.py` y `verificar_todo.py`. | **CUMPLE** |

---

## 4. Auditoría Matemática y de Implementación de Modelos

### 4.1 Prueba de Cordura Obligatoria (`abracadabra`)
Se auditó la ejecución de `codigo/pruebas.py` frente a la Tabla 2 del enunciado oficial:

| Magnitud | Valor Esperado (PDF Tabla 2) | Valor Calculado | Estado |
|:---|:---:|:---:|:---:|
| Conteos de unigramas | `a: 5, b: 2, r: 2, c: 1, d: 1` | `a: 5, b: 2, r: 2, c: 1, d: 1` | **CUMPLE (Exacto)** |
| Entropía unigramas | $2.0404$ bits | $2.04044$ bits | **CUMPLE** |
| $\hat{q}(b \mid a)$ por MLE | $0.5$ | $0.50000$ | **CUMPLE (Exacto)** |
| $\hat{q}_\alpha(b \mid a)$ con $\alpha=1, |\mathcal{V}|=5$ | $1/3 \approx 0.3333$ | $0.33333$ | **CUMPLE** |
| BPC bigrama MLE (10 transiciones) | $0.6$ bits | $0.60000$ bits | **CUMPLE (Exacto)** |
| PPL correspondiente | $1.5157$ | $1.51572$ | **CUMPLE** |

### 4.2 Modelos de $n$-gramas y Máxima Verosimilitud (Fase 2)
- **Definición de contextos y conteos:** Implementado en `ModeloNgramas` (`codigo/modelos.py`). Conteo total de $n$-gramas en entrenamiento es $N - n + 1 = 252\,626 - n + 1$.
- **Suma de probabilidades condicionales:** Se verificó que $\sum_{y \in \mathcal{V}} \hat{q}_{\text{MLE}}(y \mid h) = 1.0$ para todo contexto observado con desviación máxima de $1.11 \times 10^{-16}$, cumpliendo con creces la tolerancia exigida de $10^{-12}$.
- **Maximización de la verosimilitud (Prop. 1.1.8):** Se verificaron dos perturbaciones de $0.01$ sobre el contexto más frecuente (`' '`):
  $$\ell_{\text{MLE}} = -566\,543.6785 > \ell_A = -566\,591.3136 > \ell_B = -567\,021.2821$$
  La MLE supera ambas perturbaciones estrictamente.
- **Ceros de la MLE en validación (Tabla T2):**
  - $n=1$: 0 ceros ($0.00\%$, BPC MLE $= 4.0515$).
  - $n=2$: 0 ceros ($0.00\%$, BPC MLE $= 3.2172$).
  - $n=3$: 50 ceros ($0.1583\%$, BPC MLE $= \infty$).
  - $n=4$: 491 ceros ($1.5549\%$, BPC MLE $= \infty$).
  - $n=5$: 2 171 ceros ($6.8750\%$, BPC MLE $= \infty$).
  *Observación analítica destacada:* El equipo descubrió empíricamente que el bigrama en este corpus no presenta ceros en validación (los 27 contextos posibles están cubiertos), refutando la suposición inicial de que los ceros comenzarían en $n=2$, y reportando el hecho real con honestidad intelectual.

### 4.3 Suavizado Aditivo y Calibración de $\alpha$ (Fase 3)
- **Fórmula programada:** $\hat{q}_\alpha(y \mid h) = \frac{c(h,y) + \alpha}{c(h) + \alpha |\mathcal{V}|}$ con $|\mathcal{V}|=27$.
- **Malla de evaluación:** $\alpha \in \{0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0\}$.
- **Valores óptimos obtenidos en validación ($\alpha^*$):**
  - $n=1$: $\alpha^* = 1.0$ ($\text{BPC}_{\text{val}} = 4.0515$, curva plana).
  - $n=2$: $\alpha^* = 0.001$ ($\text{BPC}_{\text{val}} = 3.2172$, mínimo en el extremo inferior por ausencia de ceros).
  - $n=3$: $\alpha^* = 0.1$ ($\text{BPC}_{\text{val}} = 2.6982$).
  - $n=4$: $\alpha^* = 0.03$ ($\text{BPC}_{\text{val}} = 2.2959$).
  - $n=5$: $\alpha^* = 0.03$ ($\text{BPC}_{\text{val}} = \mathbf{2.1902}$).
- **Gráfica F2:** Generada con eje horizontal logarítmico, curvas claras para $n=1..5$ y puntos mínimos destacados.

### 4.4 Evaluación Única en Prueba y Teoría de la Información (Fase 4)
- **Protocolo ciego:** Parámetros congelados antes de abrir prueba.
- **Resultados oficiales en prueba (Tabla T3):**
  - $n=1$: BPC entreno $4.0592$, BPC prueba $4.0536$, PPL $16.605$.
  - $n=2$: BPC entreno $3.2354$, BPC prueba $3.2122$, PPL $9.268$.
  - $n=3$: BPC entreno $2.6872$, BPC prueba $2.7223$, PPL $6.599$.
  - $n=4$: BPC entreno $2.1538$, BPC prueba $2.3461$, PPL $5.085$.
  - $n=5$: BPC entreno $\mathbf{1.7320}$, BPC prueba $\mathbf{2.2514}$, PPL $\mathbf{4.761}$.
- **Sobreajuste demostrado (Gráfica F3):** El BPC de entrenamiento desciende monótonamente hasta $1.7320$, mientras que el de prueba se aplana en $2.2514$, abriendo una brecha de $0.5194$ bits en $n=5$.
- **Desigualdad de Gibbs (Teo. 1.1.27):** Evaluada sobre unigramas en prueba:
  $$H(\hat{p}_{\text{prueba}}) = 4.047143 \le H(\hat{p}_{\text{prueba}}, \hat{q}) = 4.053576 \implies D_{\text{KL}} = 0.006433 \ge 0$$
- **Ley de los Grandes Números (Gráfica F4):** El promedio acumulado de sorpresa $S_k$ inicia en $8.9$ bits y converge asintóticamente a $2.2514$ bits; graficado con eje horizontal logarítmico para visibilizar la estabilización.

### 4.5 Cadenas de Markov y Distribución Estacionaria (Fase 5)
- **Matriz de transición $P$ ($27 \times 27$):**
  - Desviación máxima de filas respecto a 1: $2.22 \times 10^{-16} \le 10^{-12}$.
  - Entrada mínima: $2.207 \times 10^{-8} > 0$ (estrictamente positiva $\implies$ irreducible y aperiódica).
- **Distribución estacionaria $\pi$:**
  - Iteración de potencias convergió en **22 pasos** con criterio de parada $\Delta_{\ell_1} < 10^{-10}$ (última diferencia $3.35 \times 10^{-11}$).
  - Coincidencia con frecuencias de unigramas: distancia $\ell_1 = 9.05 \times 10^{-6}$, diferencia máxima $3.71 \times 10^{-6}$.
- **Simulación de texto:** 3 muestras de 300 caracteres generadas con semilla `2026`, contexto inicial `"habia "`, para $n=2, 3, 5$. Muestras reproducidas íntegramente en Anexo C.

### 4.6 Cuantificación de Incertidumbre por Bootstrap (Fase 6)
- **Unidades:** 16 bloques contiguos (15 de 2 000 caracteres + 1 de 1 579 caracteres).
- **Métrica:** $\Delta_j = \text{BPC}_j(n=4) - \text{BPC}_j(n=5)$ ($>0 \implies n=5$ supera a $n=4$).
- **Parámetros:** 10 000 remuestreos con reemplazo, semilla `2026`, nivel de confianza 95%.
- **Resultados (Tabla T4):**
  - Media observada: $\bar{\Delta} = 0.0926$ bits.
  - Intervalo percentil 95%: $\mathbf{[0.0553,\, 0.1259]}$ bits.
  - El intervalo **excluye estrictamente el cero** (ventaja estadísticamente significativa).
  - Bloques a favor de $n=5$: 14 de 16 (los bloques 15 y 16, correspondientes al epílogo, favorecen a $n=4$ por cambio de estilo literario).
  - Análisis de sensibilidad con 15 bloques completos: $[0.0711,\, 0.1326]$ bits (conclusión robusta).

---

## 5. Auditoría de Ejecución, Rendimiento y Reproducibilidad

### 5.1 Tiempo de Ejecución y Recursos
- **Límite oficial:** $< 10$ minutos (600 segundos).
- **Tiempo medido del flujo completo (`codigo/main.py`):** **39.14 segundos** en entorno de referencia; la verificación completa de 127 magnitudes corre en solo **7 segundos**. Supera holgadamente el criterio de eficiencia.
- **Hardware:** No requiere GPU ni bibliotecas pesadas. Corre en cualquier CPU x86/ARM estándar.

### 5.2 Dependencias y Entorno de Ejecución
- **Fijación de versiones (`requirements.txt`):**
  - `numpy==2.2.4`
  - `matplotlib==3.10.1`
- **Hallazgo técnico (Ausencia de import de NumPy en código):**
  Ningún script de `codigo/` (`modelos.py`, `fase1.py`–`fase6.py`, `verificar_todo.py`, `pruebas.py`) importa ni utiliza `numpy`. Toda la implementación matemática fue realizada con la biblioteca estándar de Python (`math`, `random`, `collections`). `numpy` se declaró en `requirements.txt` y en el `README.md` como entorno de referencia, pero el código es aún más portátil al depender exclusivamente de Python base y `matplotlib` para graficar.
- **Hallazgo técnico (Entornos Debian/Ubuntu sin virtualenv):**
  En sistemas Debian/Ubuntu modernos con PEP 668, ejecutar `python3 -m venv` requiere el paquete del sistema `python3-venv` / `python3.12-venv`. Si el evaluador no activa un entorno virtual o no tiene `matplotlib` instalado globalmente, `fase1.py` generará `ModuleNotFoundError: No module named 'matplotlib'`. El `README.md` del equipo documenta correctamente los comandos para crear y activar el virtualenv antes de ejecutar `codigo/main.py`.

---

## 6. Auditoría del Reporte Escrito y Cumplimiento de Formato

### 6.1 Extensión y Maquetación
- **Límite del enunciado:** 10 a 14 páginas de cuerpo técnico (sin contar anexos).
- **Reporte compilado (`reporte/reporte.pdf`):**
  - Página 1: Portada institucional (no numerada).
  - Páginas 2 a 14 (numeradas 1 a 13 de 15): Cuerpo técnico (Resumen, Secciones 1 a 8, Referencias). La Sección 8 termina en la página 12 numerada; las referencias concluyen en la parte superior de la página 13 numerada. **Total cuerpo: ~12.2 a 13 páginas**, cumpliendo con máxima precisión la restricción de 10-14 páginas.
  - Páginas 14 a 16 (numeradas 13 a 15 de 15): Anexos A, B y C (extensión libre según Tabla 3).
  - Total de páginas del PDF: **16 páginas**.
- **Parámetros tipográficos:** Papel carta (`letterpaper`), márgenes de 2.5 cm, fuente de 11 pt (`lmodern`), interlineado 1.15 (`\setstretch{1.15}`), páginas numeradas con formato `X de Y`.
- **Cifras numéricas:** Separador decimal con punto (`.`), valores de BPC y PPL presentados con 4 cifras significativas (ej. 2.251 bits, 4.761).

### 6.2 Estructura y Contenido Obligatorio (Tabla 3 del PDF)
1. **Portada:** Título, curso, número de equipo (05), 4 integrantes con nombres y cédulas, profesor, fecha (24/11/2026). *(CUMPLE)*
2. **Resumen:** 185 palabras ($\le 200$ palabras); incluye pregunta central, datos (*Niebla*, 315 783 car., 27 símb.), método, mejor $n=5$, BPC $2.251$ bits e intervalo bootstrap $[0.0553,\, 0.1259]$. *(CUMPLE)*
3. **1. Introducción:** Problema de predicción, pregunta central, organización del informe. *(CUMPLE)*
4. **2. Marco probabilístico:** Notación formal de la Tabla 1 del PDF; definiciones previas al uso; 9 fórmulas numeradas. *(CUMPLE)*
5. **3. Datos:** Obra, URL, fecha de descarga, licencia, normalización, alfabeto, $|\mathcal{V}|=27$, partición contigua 80/10/10, Tabla T1 y Figura F1. *(CUMPLE)*
6. **4. Métodos:** Descripción reproducible de conteos, MLE, calibración de $\alpha$, métricas, simulación y bootstrap. *(CUMPLE)*
7. **5. Resultados:** Tablas T2, T3, T4 y Figuras F2, F3, F4, F5 debidamente numeradas, tituladas arriba (tablas), con leyenda abajo (figuras), citadas previamente en texto y con unidades explícitas. *(CUMPLE)*
8. **6. Verificaciones:** Declaración de tolerancias ($\le 10^{-12}$ en sumas y Gibbs, $<10^{-10}$ en $\pi$), prueba de cordura abracadabra, verificación interna de 127 comprobaciones. *(CUMPLE)*
9. **7. Discusión y limitaciones:** Respuesta exhaustiva y fundamentada a las **11 preguntas oficiales en cursiva** de la Sección 4 (subsecciones 7.1 a 7.11) más 5 limitaciones metodológicas explícitas. *(CUMPLE)*
10. **8. Conclusiones:** Respuesta concreta a la pregunta central en 4 oraciones bien delimitadas. *(CUMPLE)*
11. **Referencias:** 6 referencias bibliográficas completas y uniformes citadas en el texto: Marcano (S01), Rincón (Probabilidad), Unamuno (*Niebla*), Shannon (1948), Cover & Thomas (2006), Efron & Tibshirani (1993). *(CUMPLE)*
12. **Anexo A:** Deducción matemática formal de la MLE con multiplicadores de Lagrange y Hessiano. *(CUMPLE)*
13. **Anexo B:** Especificaciones de reproducibilidad, software, semillas y comandos. *(CUMPLE)*
14. **Anexo C:** Muestras textuales literales ($n=2, 3, 5$), declaración explícita de uso de IA y tabla de contribución individual de los 4 integrantes. *(CUMPLE)*

---

## 7. Matriz de Cumplimiento frente a la Rúbrica Oficial (100 Puntos)

| Criterio de la Rúbrica | Pts | Nivel Alcanzado | Justificación Técnica de la Calificación |
|:---|:---:|:---:|:---|
| **1. Marco probabilístico y deducciones** | 20 | **Excelente (20/20)** | Definiciones impecables de los 8 conceptos de S01 antes de su primer uso; deducción analítica paso a paso de la MLE con multiplicadores de Lagrange en Anexo A; verificación de segunda derivada (Hessiano); comprobación numérica de maximización frente a perturbaciones; notación consistente. |
| **2. Implementación y verificaciones** | 20 | **Excelente (20/20)** | Prueba de cordura con *abracadabra* pasa 6/6 verificaciones con cifras idénticas a la Tabla 2 del PDF; sumas de probabilidades condicionales verificadas con tolerancia de máquina ($1.11 \times 10^{-16} \le 10^{-12}$); filas de matriz de transición suman 1 y $P_{ij} > 0$; desigualdad de Gibbs demostrada con $D_{\text{KL}} \ge 0$; distribución estacionaria $\pi$ converge por potencias ($<10^{-10}$) y coincide con unigramas; 127/127 comprobaciones internas superadas en `verificar_todo.py`. |
| **3. Resultados y análisis** | 25 | **Excelente (25/25)** | Tablas T1–T4 y Figuras F1–F5 completas, claras y bien maquetadas; las 11 preguntas en cursiva de la Sección 4 tienen respuestas profundas y rigurosas en 7.1–7.11 con razonamiento probabilístico (no mera descripción de números); discusión de sobreajuste y divergencia entrenamiento-prueba; análisis de ergodicidad y memoria de Markov. |
| **4. Incertidumbre y protocolo** | 10 | **Excelente (10/10)** | Protocolo ciego intachable: bloque de prueba resguardado y evaluado una sola vez al final; $\alpha^*$ y $n$ elegidos estrictamente en validación; justificación teórica y estadística sólida del bootstrap por bloques contiguos de 2 000 caracteres (evitar romper dependencia serial); intervalo percentil del 95% $[0.0553,\, 0.1259]$ excluye el cero; discusión crítica de la modesta ganancia real (6.6% en PPL) y análisis de sensibilidad. |
| **5. Reproducibilidad** | 10 | **Excelente (10/10)** | Flujo integral encadenado en `codigo/main.py` ejecuta en 39.14 s ($<10$ min requeridos); semillas deterministas (`2026`); `verificar_todo.py` recalcula y contrasta todo en 7 s; `README.md` exhaustivo y claro. |
| **6. Redacción y formato** | 15 | **Suficiente / Parcial (12–13/15)** | El reporte técnico escrito es de calidad sobresaliente (cumple estrictamente tipografía, márgenes, resumen $\le 200$ palabras, cuerpo en 13 páginas, referencias, unidades). **Sin embargo, existen discrepancias en el empaquetado de entrega (PDF §5.3):** el nombre del archivo comprimido es `Proyecto_probabilidad_...zip` en vez del formato genérico `P1_EquipoNN_Apellido1_Apellido2.zip`, y la estructura interna contiene la totalidad del repositorio y textos planos en lugar de limitarse a la estructura mínima sin textos exigida por la sección 5.3. |
| **Fase 7 (Opcional, BPE)** | +10 | **No realizada (0/10)** | Decisión explícita del equipo de no abordar la fase opcional de tokenización por pares de bytes (BPE). No resta puntos de la base de 100. |
| **TOTAL ESTIMADO** | **100** | **97 – 98 / 100** | **Rango de Calificación: Sobresaliente / Excelente.** |

---

## 8. Detalle de Discrepancias, Riesgos y Recomendaciones

### 8.1 Discrepancia Principal: Nomenclatura y Estructura del Archivo ZIP Entregable
- **Criterio afectado:** Enunciado Oficial Sección 5.3 y Lista de comprobación 5.4 (ítem 8).
- **Observación:**
  1. El archivo comprimido generado se llama `Proyecto_probabilidad_31.678.578_21.129.684_33.638.501_30.445.947.zip`. El enunciado estipula la nomenclatura: `P1_EquipoNN_Apellido1_Apellido2.zip` (por ejemplo, `P1_Equipo05_Tovar_Primera.zip`). En `Tareas a realizar y orden.md`, el equipo anotó que conservó el nombre con las 4 cédulas a solicitud del grupo; no obstante, esto representa un apartamiento de la regla literal del PDF.
  2. La Sección 5.3 indica que dentro del ZIP debe existir una carpeta raíz `P1_EquipoNN_Apellido1_Apellido2/` y dentro de ella: `reporte.pdf`, `README.md`, `requirements.txt`, `datos/FUENTE.md` *(con la indicación explícita: "no subir el texto")*, `codigo/` y `resultados/`.
  3. El ZIP actual contiene el repositorio íntegro (incluyendo `libro/Niebla_limpio.txt`, `datos/*.txt`, la carpeta `S01/` con más de 100 archivos del curso, `.gitignore`, etc.), y ubica el PDF en `reporte/reporte.pdf` en lugar de la raíz del entregable.
- **Riesgo:** Pérdida de 2 a 3 puntos en el criterio de *Redacción y formato* por penalización de incumplimiento de la Sección 5.3.
- **Recomendación para el equipo (antes del envío definitivo):**
  Generar adicionalmente el archivo ZIP con la estructura canónica exacta solicitada por el profesor:
  ```bash
  # Ejemplo de empaquetado canónico:
  mkdir -p P1_Equipo05_Tovar_Primera/{datos,codigo,resultados}
  cp reporte/reporte.pdf P1_Equipo05_Tovar_Primera/
  cp README.md requirements.txt P1_Equipo05_Tovar_Primera/
  cp datos/FUENTE.md P1_Equipo05_Tovar_Primera/datos/
  cp codigo/*.py P1_Equipo05_Tovar_Primera/codigo/
  cp tablas/*.csv figuras/*.png figuras/*.pdf P1_Equipo05_Tovar_Primera/resultados/
  zip -r P1_Equipo05_Tovar_Primera.zip P1_Equipo05_Tovar_Primera/
  ```

### 8.2 Observación Menor: Tamaño del Equipo (4 Integrantes vs 2–3)
- **Criterio afectado:** Enunciado Oficial Sección 1 ("Modalidad. Equipos de 2 o 3 personas").
- **Observación:** El equipo está conformado por 4 integrantes (Simón Tovar, Samuel Primera, Román Valero y Rolando Suárez).
- **Mitigación observada:** El equipo está formalmente registrado como "Equipo 05", cuenta con una tabla de responsabilidades y contribuciones individuales equilibrada (Anexo C del reporte y plan de trabajo), y ensayó la preparación para la defensa oral aleatoria de 10 minutos exigida en la Sección 7.

### 8.3 Observación Menor: Declaración de Dependencia `numpy`
- **Observación:** `requirements.txt` y `README.md` declaran `numpy==2.2.4`, pero el código fuente no utiliza `numpy` en ninguna función de cálculo o remuestreo.
- **Evaluación:** Es una inconsistencia inocua que no afecta en absoluto los cálculos (de hecho demuestra mayor mérito al haber implementado los algoritmos probabilísticos desde cero con la biblioteca estándar de Python), pero debe tenerse en cuenta para la defensa oral si el profesor pregunta por qué se incluye en `requirements.txt`.

---

## 9. Conclusión de la Auditoría

El proyecto se encuentra en un estado de **madurez técnica excepcional**. Las formulaciones teóricas son matemáticamente rigurosas, las cifras están 100% verificadas empíricamente, el código es limpio, determinista y rápido (39 s), el reporte en LaTeX es de nivel profesional y responde cada uno de los requerimientos de contenido de la rúbrica oficial. 

Atendiendo a la recomendación de generar el ZIP con la nomenclatura y estructura canónica de la Sección 5.3, el proyecto se perfila para obtener una calificación sobresaliente (**97 a 100 puntos**).

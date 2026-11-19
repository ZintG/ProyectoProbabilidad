# Resumen consolidado de la Semana 3

> **Nota:** la Revisión 2 con el profesor no se realizará. Este documento queda como consolidado narrativo de resultados; la verificación numérica completa está en `revision_resultados.md` (127 de 127 comprobaciones correctas).

**Proyecto:** Modelos de $n$-gramas para el idioma español a partir de *Niebla* de Miguel de Unamuno
**Institución:** Facultad Experimental de Ciencias y Tecnología (FaCyT) — Universidad de Carabobo
**Hito:** cierre de la Semana 3 con todos los resultados numéricos consolidados
**Fecha:** 19 de noviembre de 2026

---

## 1. Estado del proyecto

Las seis fases obligatorias están completas y verificadas. El bloque de prueba se abrió **una sola vez**, después de congelar los hiperparámetros con validación. Queda para la Semana 4 el reporte final y la defensa; la Fase 7 (BPE) es opcional.

| Fase | Contenido | Entregable | Estado |
| :--- | :--- | :--- | :---: |
| 1 | Exploración del corpus y entropía | T1, F1 | Completa |
| 2 | Conteos y estimación MLE | T2 | Completa |
| 3 | Suavizado y elección de $\alpha$ | F2 | Completa |
| 4 | Evaluación única en prueba y Gibbs | T3, F3, F4 | Completa |
| 5 | Simulación y distribución estacionaria | F5, muestras | Completa |
| 6 | Incertidumbre por bootstrap de bloques | T4 | Completa |
| 7 | BPE (opcional) | — | No iniciada |

---

## 2. Lo que se agregó en la Semana 3

### 2.1 Fase 4: el disparo único sobre prueba

Se fijaron los $\alpha^*(n)$ obtenidos en validación y se evaluó `datos/prueba.txt` una única vez. El script incluye dos salvaguardas: un modo de ensayo (`--validar`) que no escribe nada, y un bloqueo que impide repetir la evaluación si la tabla ya existe. Antes del disparo definitivo, el ensayo sobre validación reprodujo **exactamente** los BPC de la Fase 3, lo que descarta errores de contexto o de denominador.

| $n$ | $\alpha^*$ | BPC entrenamiento | BPC prueba | PPL prueba |
|---:|---:|---:|---:|---:|
| 1 | 1.0 | 4.0592 | 4.0536 | 16.605 |
| 2 | 0.001 | 3.2354 | 3.2122 | 9.268 |
| 3 | 0.1 | 2.6872 | 2.7223 | 6.599 |
| 4 | 0.03 | 2.1538 | 2.3461 | 5.085 |
| 5 | 0.03 | **1.7320** | **2.2514** | **4.761** |

Validación y prueba coinciden en elegir $n=5$, con solo $0.0612$ bits de diferencia entre ambas estimaciones. El BPC de entrenamiento sigue bajando mientras el de prueba se aplana: la brecha llega a $0.52$ bits en $n=5$, que es la evidencia de sobreajuste que pide discutir el enunciado.

**Desigualdad de Gibbs** con el modelo de unigramas:

$$
H(\hat p_{\text{prueba}}) = 4.047143 \;\le\; H(\hat p_{\text{prueba}}, \hat q) = 4.053576,
\qquad KL = 0.006433 \text{ bits}.
$$

Se verificó solo con unigramas, como indica el enunciado: comparar el BPC de un modelo condicionado con la entropía marginal no sería una comparación válida.

### 2.2 Fase 5: simulación y cadena de Markov

La matriz $P$ del bigrama suavizado ($27\times27$) tiene desviación máxima de fila $2.22\times10^{-16}$ y entrada mínima $2.207\times10^{-8}$: es estocástica y estrictamente positiva. La iteración de potencias convergió en **22 iteraciones** con última diferencia $\ell_1$ de $3.35\times10^{-11}$.

La distribución estacionaria reproduce las frecuencias de unigramas con diferencia máxima $3.71\times10^{-6}$ y distancia $L_1$ de $9.05\times10^{-6}$. Al ser $P$ positiva, la cadena es irreducible y aperiódica, la estacionaria es única y coincide con el vector de frecuencias relativas del entrenamiento: la ergodicidad queda confirmada numéricamente.

Las tres muestras de 300 caracteres (semilla 2026, contexto inicial `"habia "`) muestran el comportamiento esperado: $n=2$ produce pseudo-español con sílabas plausibles, $n=3$ mejora la sílaba y pierde la palabra, y $n=5$ alterna fragmentos memorizados con tramos aleatorios por contextos no vistos.

### 2.3 Fase 6: ¿la ventaja de $n=5$ es real?

Se dividió el texto de prueba en **16 bloques contiguos de 2\,000 caracteres** (15 completos y uno final de 1\,579) y se calculó en cada uno

$$
\Delta_j = \text{BPC}_j(n=4) - \text{BPC}_j(n=5),
$$

con la convención $\Delta_j>0 \Rightarrow n=5$ predice mejor. Luego se construyó un intervalo percentil del 95 % para la media con 10\,000 remuestras y semilla fija.

| Cantidad | Valor |
| :--- | ---: |
| Media de $\Delta_j$ | 0.0926 bits |
| IC percentil 95 % | [0.0553, 0.1259] |
| Error estándar bootstrap | 0.0179 |
| Sesgo bootstrap | $+2.1\times10^{-5}$ |
| Bloques con $\Delta_j>0$ | 14 de 16 |
| ¿Excluye el cero? | Sí |

El intervalo queda por completo por encima de cero: la ventaja no se explica por el azar de esta partición. En tamaño práctico son $2^{0.0926}\approx1.066$, un $6.6\,\%$ menos de perplejidad, coherente con la meseta de F3.

Los bloques 15 y 16 favorecen a $n=4$ ($-0.0534$ y $-0.0646$): corresponden al epílogo, con un estilo distinto al resto del libro. Es un buen recordatorio de que el supuesto de estacionariedad es aproximado.

**Sensibilidad:** con solo los 15 bloques completos, la media es $0.1031$ y el IC $[0.0711, 0.1326]$. La conclusión no cambia.

---

## 3. Resultados consolidados

| Tabla o figura | Contenido | Resultado principal |
| :--- | :--- | :--- |
| T1 | Tamaño de particiones y $\lvert\mathcal{V}\rvert$ | 252\,626 / 31\,578 / 31\,579; $\lvert\mathcal{V}\rvert=27$ |
| T2 | Contextos y ceros en validación | Ceros desde $n=3$: 0.158 %, 1.555 % y 6.875 % |
| T3 | BPC de entrenamiento, BPC y PPL de prueba | Mejor $n=5$: 2.2514 bits, PPL 4.761 |
| T4 | Bootstrap de $\Delta_j$ | 0.0926 bits, IC [0.0553, 0.1259] |
| F1 | Frecuencias de símbolos | $H=4.0592$ bits frente a $\log_2 27=4.7549$ |
| F2 | BPC de validación contra $\alpha$ | Óptimos: 1.0; 0.001; 0.1; 0.03; 0.03 |
| F3 | BPC de entrenamiento y prueba contra $n$ | Brecha creciente desde $n=3$ |
| F4 | Promedio acumulado de sorpresa | Converge a 2.2514 (eje log) |
| F5 | $\pi$ frente a frecuencias de unigramas | Diferencia máxima $3.71\times10^{-6}$ |

**Respuesta a la pregunta central:** aumentar la memoria de 1 a 5 caracteres reduce el costo de codificación en $1.8022$ bits por carácter (de 4.0536 a 2.2514), es decir, un $44.5\,\%$. La mayor parte de la ganancia ocurre entre $n=1$ y $n=3$; a partir de ahí la curva se aplana y el modelo empieza a memorizar en lugar de generalizar.

---

## 4. Decisiones cerradas en la revisión interna

La Revisión 2 con el profesor no se realizará, así que estos puntos se resolvieron internamente y quedan documentados:

1. **Tratamiento de `#`.** Se mantiene unificado. Agrupa tildes, `ñ`, dígitos y puntuación en un solo símbolo que concentra el $8.1\,\%$ de la masa. Separarlo aumentaría $\lvert\mathcal{V}\rvert$, dispararía los ceros y obligaría a rehacer toda la calibración, sin cambiar la conclusión. Se declara como decisión de normalización en la sección de datos del reporte.
2. **Criterio de bloques en la Fase 6.** Se mantienen los 16 bloques (incluido el último de 1\,579 caracteres) porque usan el 100 % del texto de prueba, y se reporta el análisis de sensibilidad con 15 bloques completos: media 0.1031 e IC [0.0711, 0.1326]. La conclusión no depende de esa elección.
3. **Alcance de la revisión.** Se sustituye la reunión por la verificación completa de `revision_resultados.md`: 127 comprobaciones recalculadas desde los datos, todas correctas.
4. **Fase 7 (BPE).** No se inicia. El tiempo restante se concentra en el reporte, que es lo que se evalúa.
5. **Semana 4.** Queda a cargo de los compañeros. Este resumen, `revision_resultados.md` y el banco de preguntas son el insumo para la sección de resultados y discusión.

---

## 5. Material de la reunión

- `tablas/T1_particiones.csv`, `T2_ceros_validacion.csv`, `T3_evaluacion_prueba.csv`, `T3_gibbs.csv`, `T4_bootstrap.csv`, `T4_deltas_bloques.csv`, `T5_muestras.csv`
- `figuras/F1_frecuencias`, `F2_bpc_alpha`, `F3_bpc_n`, `F4_promedio_acumulado`, `F5_pi_unigramas` (cada una en `.png` y `.pdf`)
- `figuras/bootstrap_delta` (complementaria, no numerada)
- `decisiones_informe.md` (bitácora completa, secciones 1 a 15)
- `notas_importantes/Preguntas_del_proyecto.md` (banco de preguntas, 11 de 11 oficiales respondidas)
- Código: `codigo/preparar.py`, `pruebas.py`, `modelos.py` y `fase1.py` a `fase6.py`

---

## 6. Lo que queda

La Semana 4 (reporte de 10 a 14 páginas, reproducibilidad y defensa) queda a cargo de los compañeros. Este resumen y el banco de preguntas cubren la parte de resultados y discusión que el reporte necesita.

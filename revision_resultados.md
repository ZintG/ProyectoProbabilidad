# Revisión interna de resultados

**Proyecto:** Modelos de $n$-gramas para el idioma español a partir de *Niebla* de Miguel de Unamuno
**Institución:** Facultad Experimental de Ciencias y Tecnología (FaCyT) — Universidad de Carabobo
**Hito:** cierre de la Semana 3 mediante revisión interna (la Revisión 2 con el profesor no se realizará)
**Fecha:** 19 de noviembre de 2026
**Script:** `codigo/verificar_todo.py` · **Detalle:** `tablas/verificacion_resultados.csv`

---

## 1. Qué es esta revisión

La Revisión 2 estaba planteada como una reunión con el profesor. Al no realizarse, se sustituye por una **revisión interna de resultados**: en lugar de presentar las cifras, se **recalculan todas desde cero** y se comparan contra lo reportado en las tablas, figuras y documentos.

No es una lectura de los archivos: el script `codigo/verificar_todo.py` reconstruye los modelos desde `datos/`, recalcula cada métrica y contrasta el valor con el guardado. Cualquier error de cálculo, de redondeo o de copia entre tabla y texto habría aparecido como `FALLA`.

**Resultado global: 127 verificaciones, 127 correctas, 0 fallidas.**

---

## 2. Alcance

| Bloque | Qué se verificó | Comprobaciones |
| :--- | :--- | ---: |
| 1 | Particiones, vocabulario, entropía y redundancia (T1, F1) | 8 |
| 2 | Conteos y ceros de la MLE en validación (T2) | 30 |
| 3 | Rejilla completa de $\alpha$ y óptimo por $n$ (F2) | 35 |
| 4 | BPC de entrenamiento, BPC y PPL de prueba (T3) | 18 |
| 5 | Desigualdad de Gibbs y KL | 4 |
| 6 | Matriz de transición, $\pi$ y comparación con unigramas (F5) | 8 |
| 7 | Bloques, $\Delta_j$, bootstrap e IC (T4) | 9 |
| 8 | Muestras de la Fase 5 (T5) | 9 |
| | **Total** | **127** |

---

## 3. Resultados consolidados

### 3.1 Corpus y particiones

| Cantidad | Valor verificado |
| :--- | ---: |
| Caracteres totales | 315 783 |
| Entrenamiento (80 %) | 252 626 |
| Validación (10 %) | 31 578 |
| Prueba (10 %) | 31 579 |
| Vocabulario $\lvert\mathcal{V}\rvert$ | 27 |
| Entropía de unigramas $H(\hat p)$ | 4.059163 bits |
| Máximo $\log_2 27$ | 4.754888 bits |
| Redundancia $1-H/\log_2 27$ | 14.63 % |

### 3.2 Ceros de la MLE en validación (T2)

| $n$ | Contextos | $n$-gramas | Ceros | % ceros | Por $c(h)=0$ | Por $c(h,y)=0$ |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 27 | 0 | 0.0000 % | 0 | 0 |
| 2 | 27 | 413 | 0 | 0.0000 % | 0 | 0 |
| 3 | 413 | 3 620 | 50 | 0.1583 % | 0 | 50 |
| 4 | 3 620 | 15 803 | 491 | 1.5549 % | 50 | 441 |
| 5 | 15 803 | 41 148 | 2 171 | 6.8750 % | 491 | 1 680 |

### 3.3 Calibración y evaluación final (T3)

| $n$ | $\alpha^*$ | BPC entreno | BPC validación | BPC prueba | PPL prueba |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 | 4.0592 | 4.0515 | 4.0536 | 16.605 |
| 2 | 0.001 | 3.2354 | 3.2172 | 3.2122 | 9.268 |
| 3 | 0.1 | 2.6872 | 2.6982 | 2.7223 | 6.599 |
| 4 | 0.03 | 2.1538 | 2.2959 | 2.3461 | 5.085 |
| 5 | 0.03 | 1.7320 | 2.1902 | **2.2514** | **4.761** |

Las 35 combinaciones de la rejilla de $\alpha$ reproducen el BPC de validación guardado, y el mínimo de cada fila coincide con el $\alpha^*$ usado en prueba.

### 3.4 Comprobaciones teóricas

| Comprobación | Valor |
| :--- | ---: |
| $H(\hat p_{\text{prueba}})$ | 4.047143 bits |
| $H(\hat p_{\text{prueba}}, \hat q)$ | 4.053576 bits |
| $KL$ | 0.006433 bits |
| $H \le H(p,q)$ | Se cumple |
| Desviación máxima de filas de $P$ | $2.2\times10^{-16}$ |
| Entrada mínima de $P$ | $2.21\times10^{-8}$ |
| Iteraciones hasta $\ell_1<10^{-10}$ | 22 |
| Última diferencia $\ell_1$ | $3.4\times10^{-11}$ |
| $\sum_i \pi_i$ | 1 (error de máquina) |
| $\max\lvert\pi - p_{\text{unigramas}}\rvert$ | $3.7\times10^{-6}$ |
| $\lVert\pi - p_{\text{unigramas}}\rVert_1$ | $9.1\times10^{-6}$ |

### 3.5 Incertidumbre (T4)

| Cantidad | Valor |
| :--- | ---: |
| Bloques | 16 (15 de 2 000 + 1 de 1 579) |
| Caracteres cubiertos | 31 579 (100 %) |
| Media de $\Delta_j$ | 0.0926 bits |
| IC percentil 95 % | [0.0553, 0.1259] |
| Bloques con $\Delta_j>0$ | 14 de 16 |
| ¿Excluye el cero? | Sí |
| Sensibilidad (15 bloques completos) | 0.1031 · [0.0711, 0.1326] |

---

## 4. Coherencia entre entregables

Además de recalcular, se comprobaron las relaciones que deben cumplirse entre tablas y figuras. Todas se cumplen:

1. **T3 ↔ Gibbs:** el BPC de prueba de $n=1$ es exactamente $H(\hat p,\hat q)=4.053576$. Es el mismo cálculo por dos caminos distintos.
2. **T3 ↔ F3:** los puntos de la gráfica son las columnas de T3 (4.0536, 3.2122, 2.7223, 2.3461, 2.2514).
3. **T3 ↔ F4:** la asíntota de F4 es el BPC final de $n=5$, 2.2514.
4. **T3 ↔ T4:** el promedio de los BPC de bloque, ponderado por longitud, devuelve 2.346130 y 2.251390, idénticos a T3. La media simple de $\Delta_j$ difiere en $0.002$ bits porque el último bloque es más corto; está explicado y no es un error.
5. **T2 ↔ F2:** los ceros de la columna MLE ($n\ge3$) son los que hacen infinito el BPC sin suavizar, y por eso el óptimo de $\alpha$ se vuelve interior en $n=3,4,5$.
6. **F5 ↔ T1:** $\pi$ reproduce las frecuencias de unigramas del entrenamiento, que son las de T1/F1.
7. **T5:** las tres muestras tienen 306 caracteres (6 del contexto inicial + 300 generados), semilla 2026 y prefijo `habia `.

---

## 5. Observaciones

Ninguna es un error; son límites que el reporte debe declarar.

1. **El símbolo `#`** concentra el 8.1 % de la masa (tildes, `ñ`, dígitos y puntuación). Se mantiene unificado y se declara como decisión de normalización.
2. **$\alpha^*$ en $n=1$ y $n=2$** cae en el borde de la rejilla, donde la curva es plana. Se reporta como mínimo de la rejilla, sin atribuirle un óptimo estadístico fuerte.
3. **Los 16 bloques** son pocos para un bootstrap percentil: el intervalo es grueso. Se acompaña del análisis de sensibilidad con 15 bloques.
4. **Estacionariedad:** los dos últimos bloques favorecen $n=4$, lo que muestra que el estilo del epílogo difiere del resto.
5. **Alcance:** las conclusiones valen para este corpus y esta partición, no para el español en general.

---

## 6. Dictamen

**127 de 127 verificaciones correctas.** No se encontró ninguna discrepancia entre lo reportado y lo recalculado. Las dos únicas marcas iniciales de `FALLA` correspondían a comparar el intervalo de T4 con tolerancia $10^{-9}$ cuando el CSV guarda 6 decimales; se corrigió la tolerancia y quedó documentado en el propio script.

Los resultados de la Semana 3 quedan cerrados y listos para que el equipo redacte la sección de resultados y discusión del reporte.

---

## 7. Archivos de esta revisión

- `codigo/verificar_todo.py` — script de verificación (reproducible)
- `tablas/verificacion_resultados.csv` — las 127 comprobaciones con valor reportado, recalculado, diferencia y estado
- `resumen_revision_2.md` — consolidado narrativo de resultados
- `decisiones_informe.md`, sección 16 — registro de esta revisión
- `notas_importantes/Preguntas_del_proyecto.md` — banco de preguntas actualizado

# Especificación Técnica Completa y Rúbrica Oficial de Evaluación
## Proyecto: Modelos de Lenguaje de $n$-gramas (Curso de Probabilidad)

**Documentos fuente autoritativos analizados:**
- `proyecto_S01_probabilidad.pdf` (Enunciado y rúbrica oficial, Noviembre 2026, Prof. Dr. José G. Marcano)
- `decisiones_informe.md` (Memoria técnica de cálculo y bitácora de decisiones metodológicas)
- Carpeta `S01/` (`contenido_libro.tex`, `REGISTRO_TERMINOLOGIA_S01.md`, `CAMBIOS_S01_v0_9.md`, `s01_integrada.tex`)
- Archivos del repositorio (`codigo/`, `datos/`, `tablas/`, `figuras/`, `reporte/`)

---

## 1. Features Discovered (Matriz de Requisitos y Capacidades)

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Corpus & Datos | Selección y limpieza de obra | Texto en español de dominio público o licencia abierta con longitud $\ge 300\,000$ caracteres; eliminar encabezado Gutenberg, licencias y notas editoriales. | Archivo texto plano Project Gutenberg (eBook #49836) | Archivo de texto plano delimitado exclusivamente a la obra literaria | Si longitud $< 300\,000$, rechazo por enunciado | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §1–2 |
| 2 | Corpus & Datos | Normalización a minúsculas | Conversión uniforme de todos los caracteres alfabéticos a minúsculas para unificar espacio de estados. | Texto delimitado | Texto en minúsculas | Ninguno | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §3 |
| 3 | Corpus & Datos | Colapso de espacios en blanco | Reemplazo de cualquier secuencia continua de espacios, tabuladores y saltos de línea (`\s+`) por un único espacio `' '`. | Texto en minúsculas | Flujo continuo con espacios simples | Ninguno | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §4 |
| 4 | Corpus & Datos | Sustitución de caracteres fuera de alfabeto (`#`) | Definición explícita del alfabeto permitido (`a`–`z`, espacio) y mapeo de todos los demás caracteres (tildes, `ñ`, dígitos, signos de puntuación) al token `#`. | Caracteres fuera del alfabeto | Símbolo `#` | Ninguno; el símbolo `#` absorbe masa de puntuación y diacríticos | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §5 |
| 5 | Corpus & Datos | Fijación del vocabulario $\mathcal{V}$ | Construcción del conjunto finito $\mathcal{V}$ exclusivamente a partir de la partición de entrenamiento; reporte de $\|\mathcal{V}\|$. | Partición de entrenamiento | Conjunto $\mathcal{V}$, cardinalidad $\|\mathcal{V}\|=27$ | Si aparece símbolo en prueba/val no presente en $\mathcal{V}$, se trata como fuera de alfabeto | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §5 |
| 6 | Corpus & Datos | Partición secuencial contigua 80/10/10 | División del texto en 80% entrenamiento, 10% validación y 10% prueba en orden estricto, sin barajar ni mezclar oraciones (preserva dependencia temporal). | Texto normalizado (315 783 caracteres) | Tres archivos: `entrenamiento.txt` (252 626), `validacion.txt` (31 578), `prueba.txt` (31 579) | Mezclar caracteres causa fuga de información (*data leakage*) | `proyecto_S01_probabilidad.pdf` §3, `decisiones_informe.md` §6 |
| 7 | Verificación | Prueba de cordura (`abracadabra`) | Reproducción previa y exacta de las métricas sobre el texto de juguete `"abracadabra"` antes de procesar el corpus real. | Cadena `"abracadabra"` | Conteos unigramas, entropía 2.0404 bits, MLE bigrama 0.5, Laplace ($\alpha=1$, $\|\mathcal{V}\|=5$) 0.3333, BPC 0.6 bits, PPL 1.5157 | Si no coincide exactamente, código no califica para evaluación | `proyecto_S01_probabilidad.pdf` §3 (Tabla 2), `codigo/pruebas.py` |
| 8 | Modelado | Conteos de $n$-gramas ($n=1,\dots,5$) | Conteo exhaustivo de ocurrencias de contextos $c(h)$ y pares contexto-símbolo $c(h, y)$ en el texto de entrenamiento. | Orden $n$, partición de entrenamiento | Tablas de conteos $c(h)$ y $c(h, y)$ | Contexto vacío `""` para $n=1$; sólo contar $n$-gramas con sucesor | `proyecto_S01_probabilidad.pdf` §4 (Fase 2), `codigo/modelos.py` |
| 9 | Modelado | Estimación por Máxima Verosimilitud (MLE) | Estimación de la probabilidad condicional $\hat{q}_{\text{MLE}}(y \mid h) = \frac{c(h, y)}{c(h)}$. | Conteos de entrenamiento | Matriz/distribución condicional $\hat{q}(y \mid h)$ | Si $c(h)=0$, indefinido ($0/0$); se asigna probabilidad 0 | `proyecto_S01_probabilidad.pdf` §2 (Ec. 2), Prop. 1.1.8 |
| 10 | Verificación | Verificación de suma de probabilidades condicionales | Comprobación numérica de que $\sum_{y \in \mathcal{V}} \hat{q}(y \mid h) = 1$ para todo contexto observado con tolerancia $10^{-12}$. | Probabilidades condicionales | Desviación máxima observada | Falla si $|\sum \hat{q} - 1| > 10^{-12}$ | `proyecto_S01_probabilidad.pdf` §4 (Fase 2), `codigo/fase2.py` |
| 11 | Verificación | Maximización de log-verosimilitud MLE vs perturbaciones | Verificación teórica de que la MLE supera a cualquier distribución perturbada por $0.01$ en un contexto frecuente. | Distribución MLE y dos perturbaciones | Log-verosimilitudes de entrenamiento $\ell_{\text{MLE}} > \ell_A, \ell_B$ | Falla si la perturbación supera o empata a la MLE | `proyecto_S01_probabilidad.pdf` §4 (Fase 2), Prop. 1.1.8 |
| 12 | Diagnóstico | Detección y cuantificación de ceros en validación | Medición de la proporción de caracteres en validación a los que la MLE asigna probabilidad cero, heredando contexto en primeras $n-1$ posiciones. | Partición de validación, modelo MLE | Tabla T2 (contextos, $n$-gramas, conteo de ceros, % ceros, BPC MLE) | Si hay ceros, BPC MLE $=\infty$ | `proyecto_S01_probabilidad.pdf` §4 (Fase 2), Tabla T2 |
| 13 | Modelado | Suavizado aditivo de Laplace | Estimación regularizada $\hat{q}_\alpha(y \mid h) = \frac{c(h, y) + \alpha}{c(h) + \alpha \|\mathcal{V}\|}$ para $\alpha > 0$. | Parámetro $\alpha$, conteos, $\|\mathcal{V}\|$ | Probabilidad estrictamente positiva $\hat{q}_\alpha > 0$ | Si $c(h)=0$, se reduce a la distribución uniforme $1/\|\mathcal{V}\|$ | `proyecto_S01_probabilidad.pdf` §2 (Ec. 2), Prop. 1.1.14 |
| 14 | Calibración | Selección de $\alpha^*(n)$ en validación | Búsqueda en la rejilla $\alpha \in \{0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0\}$ del valor que minimiza el BPC en validación para cada $n \in \{1,\dots,5\}$. | Rejilla de $\alpha$, partición de validación | Curva F2 y valores óptimos $\alpha^*(n)$ | Prohibido optimizar $\alpha$ sobre el conjunto de prueba (anula criterio) | `proyecto_S01_probabilidad.pdf` §4 (Fase 3), F2, Rubric |
| 15 | Evaluación | Protocolo de evaluación única en prueba | Cálculo una única vez de BPC y PPL sobre `prueba.txt` congelando los hiperparámetros $\alpha^*(n)$ y el mejor orden $n^*$ seleccionados en validación. | Partición de prueba, $\alpha^*(n)$ congelados | Tabla T3 (BPC entreno, BPC prueba, PPL prueba, $\alpha^*$) | Reevaluar o reajustar con prueba anula el criterio de Incertidumbre | `proyecto_S01_probabilidad.pdf` §3, §4 (Fase 4), Rubric |
| 16 | Verificación | Verificación de Desigualdad de Gibbs | Comprobación de $H(\hat{p}_{\text{prueba}}) \le H(\hat{p}_{\text{prueba}}, \hat{q})$ y cálculo de divergencia KL $D_{\text{KL}}(\hat{p} \| \hat{q}) \ge 0$ sobre unigramas. | Unigramas empíricos de prueba vs modelo suavizado | Valores de $H(\hat{p})$, $H(\hat{p}, \hat{q})$, $D_{\text{KL}}$ | Falla si $H(p) > H(p, q)$ (viola Teo. 1.1.27) | `proyecto_S01_probabilidad.pdf` §2 (Ec. 4), §4 (Fase 4), Teo. 1.1.27 |
| 17 | Verificación | Verificación de Ley de los Grandes Números | Graficado del promedio acumulado de la pérdida logarítmica $-\log_2 \hat{q}$ a lo largo de las posiciones del texto de prueba. | Texto de prueba evaluado secuencialmente | Gráfica F4 mostrando convergencia asintótica al BPC medio | Comportamiento ruidoso inicial estabilizándose tras pocos miles de caracteres | `proyecto_S01_probabilidad.pdf` §4 (Fase 4), F4 |
| 18 | Modelado | Matriz de transición y ergodicidad | Construcción de la matriz $P$ ($27 \times 27$) para el modelo de bigramas suavizado; verificación de filas sumando 1 y entradas estrictamente positivas $P_{ij} > 0$. | Modelo bigrama con $\alpha^*$ | Matriz estocástica positiva $P$ | Filas deben sumar 1 ($|\sum P_{ij} - 1| \le 10^{-12}$) | `proyecto_S01_probabilidad.pdf` §4 (Fase 5), `codigo/fase5.py` |
| 19 | Algoritmo | Distribución estacionaria $\pi$ por iteración de potencias | Cálculo de $\pi$ mediante $\pi_{t+1} = \pi_t P$ hasta que $\|\pi_{t+1} - \pi_t\|_1 < 10^{-10}$; comparación contra frecuencias de unigramas. | Matriz $P$, vector inicial uniforme $\pi_0$ | Vector $\pi$, Gráfica F5 ($\pi$ vs frecuencias unigramas) | Falla si no converge o si norma $\ell_1 \ge 10^{-10}$ | `proyecto_S01_probabilidad.pdf` §4 (Fase 5), Teo. 1.1.40 |
| 20 | Generación | Simulación de texto con semilla fija | Muestreo autoregresivo de 3 secuencias de 300 caracteres para $n=2, 3, 5$ a partir del contexto común `"habia "` con semilla fija (`2026`). | Contexto inicial, longitud 300, modelos $n=2,3,5$, semilla | Muestras sintéticas reportadas en Anexo C y Tabla T5 | Degeneración a caracteres incoherentes ante contextos no vistos suavizados | `proyecto_S01_probabilidad.pdf` §4 (Fase 5), Anexo C |
| 21 | Estadística | Bootstrap por bloques de 2000 caracteres | Partición del texto de prueba en bloques contiguos de 2000 caracteres; cálculo de diferencias $\Delta_j = \text{BPC}_j(n=4) - \text{BPC}_j(n=5)$. | Bloques contiguos de prueba (16 bloques) | Serie de diferencias $\Delta_j$ | No remuestrear caracteres individuales (rompe dependencia temporal) | `proyecto_S01_probabilidad.pdf` §4 (Fase 6), Def. 1.1.44 |
| 22 | Estadística | Intervalo de confianza bootstrap percentil del 95% | Remuestreo de 10 000 réplicas con reemplazo de las $\Delta_j$ con semilla fija para construir el intervalo percentil $[q_{0.025}, q_{0.975}]$. | 10 000 remuestras, vector $\Delta_j$ | Tabla T4 (media de $\Delta_j$, IC 95%, número de bloques) | Si el IC contiene al 0, la ventaja no es estadísticamente distinguible | `proyecto_S01_probabilidad.pdf` §4 (Fase 6), Tabla T4 |
| 23 | Opcional | Tokenización BPE (Fase 7, +10 pts) | Implementación de 200 fusiones de Byte Pair Encoding y entrenamiento de bigrama de tokens, normalizado a BPC por carácter. | Texto de entrenamiento, 200 fusiones | Vocabulario subpalabras, BPC normalizado | Comparación injusta si no se divide entre el número de caracteres | `proyecto_S01_probabilidad.pdf` §4 (Fase 7), Def. 1.1.2 |
| 24 | Formato | Estructura formal del reporte técnico | Reporte técnico en PDF de 10 a 14 páginas (sin anexos), compuesto por Portada, Resumen ($\le 200$ palabras), Secciones 1 a 8, Referencias y Anexos A, B, C. | Manuscrito LaTeX / PDF | Documento `reporte.pdf` | Fuera de rango de páginas penaliza en criterio de Redacción | `proyecto_S01_probabilidad.pdf` §5.1, Tabla 3 |
| 25 | Formato | Tipografía y presentación editorial | Tamaño carta, márgenes 2.5 cm, fuente 11 pt, interlineado 1.15, páginas numeradas, punto decimal, 4 cifras significativas en BPC/PPL. | Documento fuente LaTeX | PDF con maquetación estricta | Comas decimales o capturas de pantalla penalizan formato | `proyecto_S01_probabilidad.pdf` §5.2 |
| 26 | Entrega | Empaquetado comprimido estándar | Archivo ZIP único con nombre `P1_EquipoNN_Apellido1_Apellido2.zip` y estructura estricta (`reporte.pdf`, `README.md`, `requirements.txt`, `datos/FUENTE.md`, `codigo/`, `resultados/`). | Archivos del proyecto | Archivo `.zip` autocontenido | No subir textos gigantes ni alterar la estructura | `proyecto_S01_probabilidad.pdf` §5.3 |
| 27 | Reproducibilidad | Límite de tiempo de ejecución | Regeneración completa de todas las tablas y figuras a partir de los datos limpios en menos de 10 minutos en equipo limpio. | Comandos de `README.md` | Tablas `.csv` y figuras `.png`/`.pdf` idénticas | Ejecución $> 10$ minutos o dependiente de intervención manual penaliza | `proyecto_S01_probabilidad.pdf` §5.3, §6 |
| 28 | Verificación | Batería integral de pruebas automatizadas | Script `codigo/verificar_todo.py` con 127 aserciones numéricas que validan de punta a punta cada cifra de las tablas T1–T5. | Datos crudos normalizados y tablas generadas | Reporte 127/127 éxitos | Cualquier discrepancia salta como `FALLA` | `decisiones_informe.md` §16, `codigo/verificar_todo.py` |

---

## 2. Edge Cases and Observed Behaviors

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Ceros de MLE en orden bajo ($n=1, 2$) | Partición de validación sobre *Niebla* | Cero absoluto de ceros (0.0000%). El vocabulario $\|\mathcal{V}\|=27$ está saturado en bigramas (413 pares observados cubren todas las transiciones reales). BPC MLE es finito (4.0515 y 3.2172). |
| 2 | Primer cero de MLE en orden $n=3$ | Partición de validación sobre *Niebla* | Aparecen exactamente 50 ceros de pares no observados ($c(h, y)=0$ con $c(h)>0$). El BPC MLE se vuelve instantáneamente $\infty$ porque $-\log_2(0) = \infty$. |
| 3 | Ceros de MLE por contexto no visto ($c(h)=0$) | Órdenes $n=4$ y $n=5$ en validación | En $n=4$ ocurren 50 ceros por contexto nuevo ($c(h)=0$) y 441 por transición no vista. En $n=5$ ocurren 491 ceros por $c(h)=0$ y 1680 por $c(h,y)=0$. Totaliza 2171 ceros (6.875%). |
| 4 | Suavizado de Laplace ante contexto no visto ($c(h)=0$) | Contexto arbitrario nunca visto en entrenamiento (ej. `"    "`) | La fórmula $\frac{0 + \alpha}{0 + \alpha\|\mathcal{V}\|} = \frac{1}{\|\mathcal{V}\|} = \frac{1}{27} \approx 0.037037$ asigna la distribución uniforme pura. No produce indeterminación ni ceros. |
| 5 | Curva de calibración $\text{BPC}(\alpha)$ en unigramas ($n=1$) | Rejilla $\alpha \in [0.001, 1.0]$ | La curva es esencialmente plana (variación en el orden de $10^{-6}$ bits). El mínimo nominal cae en $\alpha^*=1.0$, pero no representa un óptimo estadístico estricto, sino indiferencia por la gran masa de datos ($N=252\,626$) frente a $\alpha \|\mathcal{V}\|$. |
| 6 | Sensibilidad de $\alpha^*$ en órdenes altos ($n=4, 5$) | Rejilla $\alpha \in [0.001, 1.0]$ | El óptimo converge a $\alpha^*=0.03$. Si $\alpha$ es muy bajo ($0.001$), los ceros reciben probabilidad diminuta y disparan el BPC. Si $\alpha$ es alto ($1.0$), se añade una masa $\alpha \|\mathcal{V}\| = 27$ que diluye excesivamente los contextos raros ($c(h) \approx 16$), degradando el BPC. |
| 7 | Fenómeno de sobreajuste (*overfitting*) en $n=5$ | Evaluación en entrenamiento vs prueba | El BPC de entrenamiento desciende monótonamente hasta 1.7320 bits, pero el de prueba se estanca en 2.2514 bits. La brecha de generalización de 0.5194 bits evidencia memorización de secuencias específicas de entrenamiento. |
| 8 | Comportamiento asintótico de Ley de Grandes Números (F4) | Primeras 100 posiciones vs posición final en prueba | El promedio acumulado arranca en $\sim 8.9$ bits (primeros caracteres impredecibles y salto de partición), oscila fuertemente y converge asintóticamente hacia 2.2514 bits a partir de los $5\,000$ caracteres. Requiere eje horizontal logarítmico para apreciarse. |
| 9 | Ergodicidad y distribución estacionaria $\pi$ | Matriz de transición $P$ ($27 \times 27$) con bigrama $\alpha=0.001$ | Todas las entradas son positivas ($P_{ij} \ge 2.2 \times 10^{-8}$), garantizando que la cadena es irreducible y aperiódica. La iteración de potencias converge en 22 pasos con norma $\ell_1 < 10^{-10}$. $\pi$ coincide con frecuencias empíricas de entrenamiento con diferencia $\ell_1 = 9.05 \times 10^{-6}$. |
| 10 | Generación de texto en orden alto ($n=5$) | Muestreo autoregresivo con semilla 2026 | Alterna entre pasajes de palabras literarias perfectamente reproducidas por memorización y cadenas de caracteres incoherentes cuando entra a un contexto no visto donde el suavizado distribuye probabilidad uniforme entre 27 símbolos. |
| 11 | Bloque de prueba final no homogéneo en Bootstrap | Bloques 15 y 16 (últimos $\sim 3\,500$ caracteres de *Niebla*) | En los bloques 15 y 16, la diferencia es negativa ($\Delta_{15}=-0.0534, \Delta_{16}=-0.0646$), favoreciendo a $n=4$ sobre $n=5$. Se explica por el cambio de estilo literario en el epílogo de la novela, demostrando que la estacionariedad del texto es una hipótesis aproximada. |
| 12 | Bloque final residual de longitud menor a 2000 | Partición de 31 579 caracteres | Da 15 bloques de 2000 caracteres y 1 bloque final de 1579 caracteres. La media simple de $\Delta_j$ es 0.0926 bits, mientras que la media ponderada por longitud coincide exactamente con la diferencia de T3 ($2.3461 - 2.2514 = 0.0947$ bits). El análisis de sensibilidad sin el bloque 16 mantiene el IC positivo ($[0.0711, 0.1326]$). |

---

## 3. Desglose Exhaustivo de las 11 Preguntas Teóricas en Cursiva

El enunciado exige que cada una de las preguntas formuladas en cursiva en la Sección 4 sea respondida explícitamente en la Sección 7 del reporte técnico:

1. **Fase 1:** *¿Qué tan lejos está el texto de ser «al azar» sobre su alfabeto? Interprete la diferencia en bits.*
   - **Respuesta esperada:** Un texto generado uniformemente al azar sobre $\|\mathcal{V}\|=27$ posee una entropía máxima de $\log_2(27) \approx 4.7549$ bits por carácter. La entropía empírica de unigramas de *Niebla* es $H(\hat{p}) = 4.0515$ bits. La diferencia es de aproximadamente $0.7034$ bits por carácter. Esto significa que la distribución natural de las letras en español (alta frecuencia del espacio, la `'e'`, la `'a'` y la `'o'`) ahorra $0.70$ bits por símbolo respecto a la incertidumbre máxima.
2. **Fase 2:** *¿Por qué el BPC de la MLE en validación es infinito en cuanto aparece un cero?*
   - **Respuesta esperada:** Por definición, $\text{BPC} = -\frac{1}{N} \sum_t \log_2 \hat{q}(x_t \mid h_t)$. Si en algún punto del texto no visto ocurre un carácter $x_t$ para el cual el modelo asigna probabilidad $\hat{q}(x_t \mid h_t) = 0$, el término $-\log_2(0) = +\infty$, lo que anula la suma y hace el costo medio infinito. En teoría de la información, equivale a afirmar que el modelo asignó certeza de imposibilidad a un suceso que efectivamente ocurrió.
3. **Fase 2:** *¿Por qué crece la proporción de ceros con n?*
   - **Respuesta esperada:** El número potencial de contextos y $n$-gramas crece exponencialmente como $\|\mathcal{V}\|^{n-1}$ (en este caso $27^{n-1}$), mientras que el tamaño del corpus de entrenamiento es finito y fijo ($N = 252\,626$). Por la maldición de la dimensionalidad y la escasez de datos (*data sparsity*), a mayor $n$ la gran mayoría de las combinaciones posibles nunca son observadas en entrenamiento, aumentando drásticamente la proporción de ceros en textos nuevos.
4. **Fase 3:** *¿Por qué el $\alpha$ óptimo cambia con n?*
   - **Respuesta esperada:** El impacto del término de suavizado $\alpha \|\mathcal{V}\|$ depende del conteo típico del contexto $c(h)$. Para $n=1, 2$, los conteos por contexto son masivos ($c(h) \approx 9\,357$ en bigramas), por lo que el sesgo por ceros es despreciable y el modelo prefiere $\alpha \to 0$ (casi MLE). Para $n=4, 5$, los contextos son muy escasos ($c(h) \approx 16$ en $n=5$), y un $\alpha$ mal ajustado domina sobre los conteos reales, obligando a calibrar un $\alpha$ fino ($\alpha^*=0.03$) que evite probabilidades nulas sin aplanar excesivamente la distribución.
5. **Fase 3:** *¿Qué ocurre con $\alpha = 1$ en contextos que aparecen pocas veces?*
   - **Respuesta esperada:** Si un contexto aparece solo una vez ($c(h)=1$), fijar $\alpha=1$ con $\|\mathcal{V}\|=27$ hace que el denominador sea $1 + 27 = 28$. El símbolo observado recibe probabilidad $(1+1)/28 = 2/28 \approx 0.071$, mientras que los 26 símbolos nunca vistos se reparten el resto de la masa ($26/28 \approx 0.929$, es decir $1/28 \approx 0.036$ cada uno). Esto diluye drásticamente la señal observada y sobrerregulariza el modelo hacia una distribución casi uniforme.
6. **Fase 4:** *¿Qué n elige la validación y confirma la prueba ese orden?*
   - **Respuesta esperada:** La validación elige inequívocamente el orden $n^*=5$ con $\alpha^*=0.03$, obteniendo un BPC de validación de $2.1902$ bits. La evaluación única en el conjunto de prueba confirma exactamente este orden como el mejor, registrando un BPC de prueba de $2.2514$ bits (PPL de 4.761), con una discrepancia mínima de solo $0.0612$ bits respecto a validación.
7. **Fase 4:** *¿Por qué el BPC de entrenamiento sigue bajando cuando el de prueba ya no?*
   - **Respuesta esperada:** Este fenómeno ilustra el sobreajuste (*overfitting*). En entrenamiento, aumentar la memoria del modelo ($n$) permite memorizar cadenas específicas y giros exactos del texto, reduciendo la entropía empírica de entrenamiento hasta 1.7320 bits en $n=5$. Sin embargo, en prueba la tasa de mejora se estanca (meseta en $\sim 2.25$ bits) porque la falta de datos impide estimar confiablemente probabilidades para contextos largos no vistos, ensanchando la brecha de generalización.
8. **Fase 5:** *¿Por qué $\pi$ se parece a las frecuencias del texto?*
   - **Respuesta esperada:** Por el Teorema Ergódico para cadenas de Markov regulares (irreducibles y aperiódicas con matriz de transición estocástica estrictamente positiva $P>0$), existe una única distribución estacionaria $\pi$ tal que $\pi P = \pi$. Dado que $P$ se estimó a partir de las frecuencias de transición del propio texto y el suavizado $\alpha=0.001$ es mínimo, la distribución de largo plazo del sistema dinámico coincide asintóticamente con la distribución marginal empírica de unigramas ($D_{\ell_1} = 9.05 \times 10^{-6}$).
9. **Fase 5:** *¿Qué propiedades del español capturan las muestras y cuáles no?*
   - **Respuesta esperada:**
     - *Propiedades capturadas:* Estructura fonotáctica local, alternancia natural de consonantes y vocales, formación de sílabas válidas en español, palabras funcionales cortas (`"de"`, `"que"`, `"la"`), y longitud promedio verosímil de palabras.
     - *Propiedades NO capturadas:* Concordancia gramatical de género y número a media y larga distancia, estructura sintáctica de oraciones complejas, significado semántico global, coherencia narrativa y puntuación lógica coherente (el token `#` agrupa indistintamente pausas, signos y tildes).
10. **Fase 6:** *¿El intervalo excluye el cero?*
    - **Respuesta esperada:** Sí, el intervalo de confianza bootstrap percentil del 95% para la mejora $\Delta = \text{BPC}(n=4) - \text{BPC}(n=5)$ es $[0.0553, 0.1259]$ bits. Al estar estrictamente contenido en el semiplano positivo y excluir el cero, permite afirmar con $95\%$ de confianza que el modelo de 5-gramas es genuinamente superior al de 4-gramas en este corpus y que la ventaja no es producto del azar de la partición.
11. **Fase 6:** *¿Por qué se remuestrean bloques y no caracteres individuales?*
    - **Respuesta esperada:** La validez teórica del método bootstrap requiere que las unidades remuestreadas sean independientes e idénticamente distribuidas (i.i.d.). En el lenguaje natural existe una fuerte dependencia serial de Markov entre caracteres vecinos. Remuestrear caracteres individuales destruiría por completo la estructura lingüística y subestimaría drásticamente la varianza real (falsa precisión). El bootstrap por bloques contiguos de 2000 caracteres preserva la dependencia interna y genera unidades aproximadamente incorreladas.

---

## 4. Estructura Obligatoria del Reporte (Sección 5 y Tabla 3 del PDF)

| Sección | Contenido Específico Obligatorio | Extensión Requerida |
|---|---|---|
| **Portada** | Título, curso, número de equipo, integrantes con cédula, profesor, fecha | 1 página |
| **Resumen** | Pregunta central, datos, método, resultado numérico principal (mejor $n$, su BPC de prueba con intervalo bootstrap) | $\le 200$ palabras |
| **1. Introducción** | Problema de predicción de caracteres, formulación de la pregunta central, estructura y organización del reporte | $\frac{1}{2}$ a 1 página |
| **2. Marco probabilístico** | Definiciones previas de los 8 conceptos de S01 con notación consistente; deducción analítica de la MLE (o remisión a Anexo A) | 2 a 3 páginas |
| **3. Datos** | Obra analizada (*Niebla*), URL Gutenberg, fecha de descarga, licencia, normalización obligatoria, alfabeto, vocabulario $\mathcal{V}$ y partición 80/10/10; Tabla T1 y Figura F1 | 1 página |
| **4. Métodos** | Modelos $n$-gramas, suavizado de Laplace, protocolo de calibración de $\alpha$, métricas (BPC, PPL), simulación ergódica y bootstrap por bloques, reproducible | 1 a 2 páginas |
| **5. Resultados** | Presentación sistemática de Tablas T2–T4 y Figuras F2–F5, todas citadas y comentadas analíticamente en el cuerpo | 3 a 4 páginas |
| **6. Verificaciones** | Prueba de cordura `abracadabra`, sumas de filas de condicionales ($10^{-12}$), desigualdad de Gibbs, convergencia de $\pi$ ($10^{-10}$), con tolerancias declaradas | $\frac{1}{2}$ a 1 página |
| **7. Discusión y limitaciones** | Respuesta punto por punto a las 11 preguntas en cursiva de la Sección 4; análisis explícito de lo que los datos no permiten concluir | 1 a 2 páginas |
| **8. Conclusiones** | Respuesta directa, concisa y respaldada a la pregunta central del proyecto redactada en 3 a 5 oraciones | $\frac{1}{2}$ página |
| **Referencias** | Libro de texto de S01 (Dr. José G. Marcano), Shannon (1948), Cover & Thomas (2006), Efron & Tibshirani (1993), Project Gutenberg, citadas con formato uniforme | Sin límite |
| **Anexo A** | Deducción matemática completa de la MLE mediante multiplicadores de Lagrange sobre el símplex de probabilidad; análisis bayesiano si aplica | Extensión libre |
| **Anexo B** | Especificaciones completas de reproducibilidad: versiones de librerías, semillas utilizadas, comandos de terminal y tiempos de cómputo | Extensión libre |
| **Anexo C** | Textos generados en la Fase 5 (300 caracteres para $n=2,3,5$) con sus semillas; declaración formal del uso de asistentes de IA | Extensión libre |
| **Tabla de Contribución** | Tabla obligatoria al final del documento detallando la contribución porcentual y tareas asumidas por cada integrante | 1 tabla breve |

### Requisitos de Formato y Tipografía (§5.2):
- **Formato:** PDF compilado preferiblemente desde LaTeX.
- **Extensión:** 10 a 14 páginas estrictas de cuerpo principal (sin contar los anexos A, B y C).
- **Dimensiones:** Tamaño carta (*letterpaper*), márgenes de 2.5 cm en los 4 bordes.
- **Tipografía:** Letra de 11 pt, interlineado 1.15, páginas numeradas correlativamente.
- **Notación numérica:** Punto (`.`) obligatorio como separador decimal (prohibida la coma decimal). Cuatro cifras significativas para métricas de información (BPC y PPL, ej. `2.2514`).
- **Tablas y Figuras:** Toda tabla lleva título en la parte superior; toda figura lleva leyenda en la parte inferior. Deben estar numeradas correlativamente (T1–T4, F1–F5), citadas en el texto antes de aparecer, con ejes rotulados y legibles en blanco y negro. Unidades obligatorias (bits, caracteres).
- **Cero capturas de pantalla:** Todas las figuras deben generarse mediante código vectorial o de alta resolución (`.pdf` / `.png`).
- **Código en reporte:** Prohibido pegar listados extensos de código; solo fragmentos indispensables menores a 15 líneas.

---

## 5. Rúbrica Oficial de Evaluación y Penalizaciones (Tabla 4 del PDF)

Puntaje total base: **100 puntos** (más hasta **+10 puntos extra** de la Fase 7 opcional).
*Regla de exclusión:* Un reporte sin código que reproduzca sus cifras obtiene como máximo 50 puntos.

| Criterio | Pts | Excelente (90–100%) | Suficiente (60–89%) | Insuficiente (<60%) |
|---|---|---|---|---|
| **Marco probabilístico y deducciones** | **20** | Definiciones correctas antes de su uso; MLE deducida paso a paso; notación consistente en todo el reporte. (18–20 pts) | Definiciones correctas con omisiones menores o pasos sin justificar. (12–17 pts) | Conceptos confundidos (p. ej., entropía y entropía cruzada) o fórmulas sin explicar. (0–11 pts) |
| **Implementación y verificaciones** | **20** | Prueba de cordura, sumas de condicionales, desigualdad de Gibbs y convergencia de $\pi$ comprobadas con tolerancias numéricas declaradas. (18–20 pts) | Comprobaciones parciales o tolerancias no documentadas. (12–17 pts) | Sin comprobaciones, o cifras que no coinciden con `abracadabra`. (0–11 pts) |
| **Resultados y análisis** | **25** | Tablas T1–T4 y Figuras F1–F5 completas; las 11 preguntas en cursiva respondidas con argumentos probabilísticos rigurosos. (22.5–25 pts) | Resultados completos con análisis superficial o interpretaciones débiles. (15–22 pts) | Resultados incompletos o sin interpretar. (0–14 pts) |
| **Incertidumbre y protocolo** | **10** | Conjunto de prueba usado una sola vez; bootstrap por bloques bien justificado teóricamente; conclusiones estrictamente acordes al intervalo. (9–10 pts) | Bootstrap correcto pero con justificación teórica débil. (6–8.5 pts) | $\alpha$ o $n$ elegidos usando datos de prueba, o conclusiones que omiten la incertidumbre muestral. (0–5.5 pts) |
| **Reproducibilidad** | **10** | `README.md` claro y semillas fijadas que regeneran todas las cifras, tablas y figuras en menos de 10 minutos en entorno limpio. (9–10 pts) | El proyecto se regenera tras ajustes menores o dependencias omitidas. (6–8.5 pts) | El código no se puede ejecutar, faltan archivos o falla con excepciones. (0–5.5 pts) |
| **Redacción y formato** | **15** | Cumple íntegramente la Sección 5: extensión 10–14 pp, márgenes 2.5 cm, tablas y figuras citadas y numeradas, texto técnico claro y preciso. (13.5–15 pts) | Incumplimientos menores de formato o maquetación descuidada. (9–13 pts) | Fuera de extensión (más de 14 pp o menos de 10 pp de cuerpo), o tablas/figuras sin numerar ni citar. (0–8.5 pts) |
| **Fase 7 (Opcional)** | **+10** | Implementación correcta de BPE (200 fusiones) y comparación justa expresada en BPC por carácter frente a la Fase 4. (+9 a +10 pts) | Implementación de BPE con comparación cuestionable o no normalizada. (+6 a +8 pts) | No implementada o incompleta (0 pts extra). |

### Penalizaciones Graves:
1. **Retraso en entrega:** $-10$ puntos por cada día de retraso, admitiéndose un máximo de dos días de demora.
2. **Violación de protocolo de prueba:** Utilizar el bloque de prueba para ajustar o seleccionar $\alpha$ o el orden $n$ **anula automáticamente la totalidad del criterio de Incertidumbre y protocolo (0 de 10 puntos)**.
3. **Fraude académico o falsedad:** Copiar código o texto de otro equipo, o presentar cifras en el reporte que el código entregado no produce, anula por completo el proyecto (calificación 0).

---

## 6. Estructura del Entregable ZIP (§5.3)

Nombre del archivo: `P1_EquipoNN_Apellido1_Apellido2.zip` (donde NN es el número de equipo a dos dígitos).

```
P1_EquipoNN_Apellido1_Apellido2/
|-- reporte.pdf          # Reporte técnico final compilado (10-14 pp sin anexos)
|-- README.md            # Instrucciones claras de reproducción y orden de ejecución
|-- requirements.txt     # Dependencias de Python fijadas (o sessionInfo.txt si R)
|-- datos/
|   `-- FUENTE.md        # Título, autor, URL Gutenberg y fecha (sin subir el corpus crudo)
|-- codigo/
|   |-- preparar.py      # Descarga, limpieza editorial, normalización y partición 80/10/10
|   |-- modelos.py       # Clase ModeloNgramas: conteos, MLE, Laplace, BPC, PPL
|   |-- experimentos.py  # Pipeline integrado de Fases 1 a 6; genera artefactos en resultados/
|   `-- pruebas.py       # Prueba de cordura abracadabra y comprobaciones unitarias
`-- resultados/          # Tablas (.csv) T1-T4 y figuras (.pdf/.png) F1-F5 del reporte
```
*Criterio de evaluación de reproducibilidad:* Ejecución de extremo a extremo en $<10$ minutos.

---

## 7. Mapeo de Conceptos y Notación Formal S01

| Concepto | Notación | Definición Matemática Operativa | Referencia S01 |
|---|---|---|---|
| Alfabeto y Vocabulario | $\mathcal{V}$, $\|\mathcal{V}\|$ | Conjunto finito de símbolos (caracteres); cardinalidad finita $\|\mathcal{V}\|$. En *Niebla*, $\|\mathcal{V}\|=27$. | Def. 1.1.1 |
| Codificación por pares de bytes | BPE | Algoritmo voraz que fusiona iterativamente el par de bytes/caracteres adyacentes más frecuente. | Def. 1.1.2 |
| Regla de la cadena | $P(x_{1:T})$ | $P(x_{1:T}) = \prod_{t=1}^T P(x_t \mid x_{1:t-1})$. | Prop. 1.1.3 |
| Hipótesis de Markov | $n-1$ | $P(x_t \mid x_{1:t-1}) = P(x_t \mid x_{t-n+1:t-1})$, memoria acotada a $n-1$ caracteres. | Def. 1.1.6 |
| Estimador MLE | $\hat{q}_{\text{MLE}}$ | $\hat{q}_{\text{MLE}}(y \mid h) = \frac{c(h, y)}{c(h)}$ con $c(h) = \sum_{y \in \mathcal{V}} c(h, y)$. | Prop. 1.1.8 |
| Suavizado aditivo | $\hat{q}_\alpha$ | $\hat{q}_\alpha(y \mid h) = \frac{c(h, y) + \alpha}{c(h) + \alpha \|\mathcal{V}\|}$, con pseudoconteo $\alpha > 0$. | Prop. 1.1.14 |
| Prior de Dirichlet | $\text{Dir}(\alpha)$ | Distribución a priori conjugada de la multinomial; esperanza posterior coincide con Laplace. | Teo. 1.1.12, Prop. 1.1.13 |
| Entropía de Shannon | $H(p)$ | $H(p) = -\sum_{x \in \mathcal{V}} p(x) \log_2 p(x)$. Cota máxima: $H(p) \le \log_2 \|\mathcal{V}\|$. | §1.1.4, Prop. 1.1.15 |
| Divergencia KL | $D_{\text{KL}}(p \| q)$ | $D_{\text{KL}}(p \| q) = \sum_{x} p(x) \log_2 \frac{p(x)}{q(x)} \ge 0$. | Def. 1.1.17 |
| Entropía cruzada | $H(p, q)$ | $H(p, q) = -\sum_{x} p(x) \log_2 q(x) = H(p) + D_{\text{KL}}(p \| q)$. | Prop. 1.1.18 |
| Desigualdad de Gibbs | $H(p) \le H(p, q)$ | Teorema fundamental de teoría de la información: igualdad si y solo si $p = q$. | Teo. 1.1.27 |
| Bits por carácter | BPC | $\text{BPC} = -\frac{1}{N_e} \sum_{t=1}^{N_e} \log_2 \hat{q}(x_t \mid h_t)$. | Def. 1.1.20 |
| Perplejidad | PPL | $\text{PPL} = 2^{\text{BPC}}$. Número efectivo de ramificaciones igualmente probables. | Prop. 1.1.42 |
| Matriz de transición | $P$ | Matriz $\|\mathcal{V}\| \times \|\mathcal{V}\|$ donde $P_{ij} = \hat{q}_\alpha(V_j \mid V_i)$, estocástica y positiva. | §1.1.5 |
| Distribución estacionaria | $\pi$ | Vector fila no negativo tal que $\pi P = \pi$ y $\sum_i \pi_i = 1$; obtenido por potencias $\pi_0 P^t$. | Teo. 1.1.40 |
| Bootstrap percentil | IC $95\%$ | Remuestreo no paramétrico con reemplazo de bloques independientes; percentiles 2.5 y 97.5. | Def. 1.1.44 |

---

## 8. Verificación Cruzada con `decisiones_informe.md`

| Aspecto | Decisión en Bitácora | Alineación con Enunciado y S01 | Estado |
|---|---|---|---|
| **Corpus** | *Niebla* de Miguel de Unamuno (#49836), 315 783 caracteres netos. | Cumple requisito $\ge 300\,000$ caracteres y licencia de dominio público. | Conforme |
| **Limpieza** | Eliminada "Nota de transcripción" (459 car.) e "Índice" (750 car.). | Cumple la directriz de descartar paratextos para no sesgar el español autoral. | Conforme |
| **Normalización** | Minúsculas + colapso `\s+` a `' '` + reemplazo a `#`. | Cumple reglas 1, 2 y 3 de la Sección 3 del enunciado. | Conforme |
| **Vocabulario** | $\|\mathcal{V}\|=27$ (25 letras presentes en la obra + `' '` + `#`). | Cumple rango típico reportado en enunciado (30–45, o alfabetos acotados). | Conforme |
| **Partición** | 80/10/10 contiguo (252 626 / 31 578 / 31 579 caracteres). | Cumple orden estricto sin barajar oraciones ni caracteres. | Conforme |
| **Prueba cordura** | `abracadabra` reproduce Tabla 2 exactamente. | Pasa 6/6 métricas con cero discrepancia. | Conforme |
| **Fase 2 (MLE)** | Ceros en validación: 0% en $n=1,2$, 0.158% en $n=3$, 1.55% en $n=4$, 6.87% en $n=5$. | Respaldado empíricamente; sumas de condicionales $< 1.11 \times 10^{-16}$. | Conforme |
| **Fase 3 (Alpha)** | Rejilla 7 valores: $\alpha^*(1)=1.0, \alpha^*(2)=0.001, \alpha^*(3)=0.1, \alpha^*(4)=0.03, \alpha^*(5)=0.03$. | Búsqueda exhaustiva en validación según la regla de minimización de BPC. | Conforme |
| **Fase 4 (Prueba)** | Evaluación única congelando $\alpha^*$: Mejor $n=5$ (BPC=2.2514, PPL=4.761). | Desigualdad de Gibbs comprobada en unigramas ($KL=0.0064$ bits); LLN verificada en F4. | Conforme |
| **Fase 5 (Simulación)** | Matriz $27 \times 27$ positiva; potencias convergen en 22 iteraciones ($\|\Delta\|_1 < 10^{-10}$). Muestras con semilla 2026. | Cumple convergencia a $\pi$ ($D_{\ell_1}=9.05 \times 10^{-6}$) y generación autoregresiva. | Conforme |
| **Fase 6 (Bootstrap)** | 16 bloques contiguos de prueba (15 de 2000 + 1 de 1579). 10 000 remuestras. IC 95%: $[0.0553, 0.1259]$. | Justificado teóricamente; excluye el 0 y valida la superioridad de $n=5$. | Conforme |
| **Fase 7 (Opcional)** | No abordada (decisión explícita del equipo de afianzar la excelencia en fases 1 a 6). | Conforme a la opción voluntaria de la rúbrica (hasta +10 pts extra). | Conforme |
| **Verificación integral**| `codigo/verificar_todo.py` con 127/127 pruebas superadas. | Respaldo total de la consistencia numérica cruzada entre código, tablas y figuras. | Conforme |

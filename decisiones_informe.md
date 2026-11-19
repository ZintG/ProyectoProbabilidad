# Bitácora de Decisiones del Proyecto: Modelos de $n$-gramas

Este documento registra todas las decisiones técnicas, metodológicas y de modelado tomadas durante el desarrollo del proyecto final de **Teoría de la Probabilidad**. Sirve como memoria de cálculo y referencia directa para la redacción de las secciones del **Reporte Técnico Final** (Datos, Métodos, Verificaciones y Discusión).

---

## 1. Selección de la Obra Literaria (Corpus)
* **Decisión:** Se seleccionó la novela ***Niebla (Nivola)*** del autor español **Miguel de Unamuno**, publicada originalmente en 1914.
* **Fuente:** Project Gutenberg, [eBook #49836](https://www.gutenberg.org/ebooks/49836). Archivo en texto plano UTF-8 descargado el 12 de noviembre de 2026.
* **Justificación:**
  1. Es una obra cumbre de la literatura en español del siglo XX con vocabulario rico y estilo representativo del idioma.
  2. Es de dominio público con licencia que permite su libre uso para fines académicos.
  3. Supera el requisito obligatorio de extensión mínima ($\ge 300\,000$ caracteres): el texto base cuenta con **319\,674 caracteres**, y tras la limpieza editorial y normalización conserva **315\,783 caracteres**.

---

## 2. Limpieza Editorial y Delimitación del Texto
* **Decisión:** Se eliminó el paratexto editorial añadido por transcriptores modernos:
  - Al inicio: Se removió la *«NOTA DE TRANSCRIPCIÓN»* (459 caracteres) añadida por los voluntarios de Project Gutenberg.
  - Al final: Se removió el *«ÍNDICE»* de capítulos con numeración de páginas (aproximadamente 750 caracteres).
* **Justificación:** El objetivo del proyecto es modelar la distribución probabilística del español literario escrito por el autor, no las notas de digitalización del siglo XXI ni listados numéricos de páginas que distorsionarían las frecuencias de los caracteres.
* **Resultado:** La novela pura comprende desde el título y prólogo de la novela hasta el epílogo (*Oración fúnebre por la muerte de Orfeo*).

---

## 3. Normalización: Paso a Minúsculas
* **Decisión:** Todo el texto se convierte a minúsculas (`.lower()`).
* **Justificación:** Cumple la directriz obligatoria de la Sección 3 del enunciado. Desde el punto de vista probabilístico, tratar las mayúsculas como estados distintos (por ejemplo, separar `'A'` de `'a'`) duplicaría artificialmente el tamaño del vocabulario $|\mathcal{V}|$, dispersaría las frecuencias de conteo y generaría una matriz de transición con muchos más ceros innecesarios.

---

## 4. Normalización: Colapso de Espacios y Saltos de Línea
* **Decisión:** Cualquier secuencia de uno o más espacios, tabuladores o saltos de línea consecutivos (`\n`, `\r`, `\t`) se colapsa a un único espacio en blanco `' '` usando la expresión regular `\s+`.
* **Justificación:** Cumple con la regla obligatoria del proyecto. En un modelo de caracteres contiguos, múltiples saltos de línea vacíos entre párrafos sobrestimarían la probabilidad de transiciones vacías. El espacio simple actúa como el delimitador natural entre palabras.
* **Resultado de longitud:** El texto final continuo queda exactamente en **315\,783 caracteres**.

---

## 5. Definición del Alfabeto y Regla del Numeral (`#`)
* **Decisión:**
  - **Alfabeto permitido:** Las 26 letras del abecedario en inglés (`a`–`z`) más el espacio en blanco `' '`.
  - **Sustitución por `#`:** Todo carácter que no pertenezca al alfabeto permitido se reemplaza por el símbolo especial único `#`. Esto incluye:
    - Signos de puntuación (puntos, comas, dos puntos, punto y coma, guiones, signos de interrogación y exclamación, comillas, etc.).
    - Dígitos numéricos (`0`–`9`).
    - Caracteres propios del español como la letra `ñ` y las vocales con tildes o diéresis (`á`, `é`, `í`, `ó`, `ú`, `ü`).
* **Justificación:** El enunciado establece explícitamente: *«el alfabeto elegido (letras con tildes, ñ, dígitos, signos) se declara en el reporte»*. El equipo decidió unificar todo elemento no alfabético estándar bajo el token `#`.
* **Impacto y Observaciones para el Reporte:**
  1. El tamaño del vocabulario del texto queda en **$|\mathcal{V}| = 27$** (el espacio en blanco, el numeral `#` y 25 letras, dado que Unamuno no empleó la letra `w` en esta obra).
  2. El símbolo `#` absorberá una masa probabilística considerable, pues acumula signos de puntuación y caracteres acentuados. Palabras como *año* pasan a ser *a#o* y *más* pasa a ser *m#s*. Esto debe justificarse formalmente en la sección de discusión del reporte técnico.

---

## 6. Partición Contigua de los Datos (80% / 10% / 10%)
* **Decisión:** El texto continuo normalizado de 315\,783 caracteres se dividió en tres bloques contiguos y secuenciales:
  - **Entrenamiento (80%):** Primeros **252\,626 caracteres** (posiciones `0` a `252625`).
  - **Validación (10%):** Siguientes **31\,578 caracteres** (posiciones `252626` a `284203`).
  - **Prueba (10%):** Últimos **31\,579 caracteres** (posiciones `284204` a `315782`).
* **Justificación:**
  1. *Dependencia temporal contigua:* El lenguaje natural presenta una fuerte dependencia de Markov entre caracteres vecinos. Barajar aleatoriamente caracteres u oraciones generaría fuga de información (*data leakage*), violando la hipótesis de prueba ciega.
  2. *Uso estricto del bloque de prueba:* La partición de prueba se resguarda bajo llave y solo se evaluará una única vez al final del proyecto (Fase 4), como exige la rúbrica metodológica.

---

## 7. Verificación Inicial de Cordura (`abracadabra`)
* **Decisión:** Se implementó y ejecutó el script `codigo/pruebas.py` antes de procesar el libro grande, utilizando la palabra de juguete *«abracadabra»*.
* **Resultados obtenidos (100% coincidentes con la Tabla 2 del PDF):**
  - Conteos unigramas: `a: 5, b: 2, r: 2, c: 1, d: 1`.
  - Entropía unigramas: `2.0404 bits`.
  - $\hat{q}(b \mid a)$ por MLE: `0.5000`.
  - $\hat{q}_\alpha(b \mid a)$ con $\alpha = 1$ y $|\mathcal{V}| = 5$: `0.3333` ($1/3$).
  - BPC del bigrama MLE (10 transiciones): `0.6000 bits`.
  - Perplejidad (PPL): `1.5157`.
* **Justificación:** Garantiza matemáticamente que los algoritmos de estimación, entropía y evaluación están programados sin sesgos conceptuales.

---

## 8. Inicialización del Control de Versiones con Git
* **Decisión:** Se inicializó un repositorio Git local en la rama principal `main` con un archivo `.gitignore` configurado para ignorar binarios, cachés de Python (`__pycache__`) y archivos auxiliares de LaTeX (`.aux`, `.log`, `.out`). Se realizó el primer *commit* con los 112 archivos base del proyecto.
* **Justificación:** Garantiza la trazabilidad, reproducibilidad y trabajo colaborativo para sincronizar el código con GitHub y plataformas en la nube (como Google Colab).

---

## 9. Fase 2: Conteos de \(n\)-gramas y estimación por máxima verosimilitud (MLE)

**En palabras sencillas:** un modelo de \(n\)-gramas intenta adivinar el siguiente carácter de un texto mirando los \(n-1\) caracteres anteriores. La estimación por máxima verosimilitud (MLE) aprende contando cuántas veces apareció cada combinación en el entrenamiento y dividiendo entre cuántas veces apareció el contexto.

* **Decisión:** se implementó el módulo `codigo/modelos.py` con la clase `ModeloNgramas`. La clase construye, para cualquier orden \(n\), los conteos \(c(h)\) de contextos y \(c(h,y)\) de pares \((h,y)\), y calcula la probabilidad MLE.
* **Convenciones:**
  - El vocabulario \(\mathcal{V}\) se fija exclusivamente con `datos/entrenamiento.txt`: \(|\mathcal{V}|=27\).
  - El contexto \(h\) tiene longitud \(n-1\). Para \(n=1\), \(h\) es la cadena vacía `""`.
  - Solo se cuentan \(n\)-gramas completos, es decir, contextos que tienen un sucesor. Así, \(c(h)=\sum_{y\in\mathcal{V}} c(h,y)\).
  - El número total de \(n\)-gramas contados en entrenamiento es \(N-n+1\), con \(N=252\,626\).
* **Fórmula MLE:**
  \[
  \hat q_{\text{MLE}}(y\mid h)=\frac{c(h,y)}{c(h)},\qquad c(h)>0.
  \]
  Si \(c(h)=0\), la MLE es una división \(0/0\) no definida; para la detección de ceros se registra como probabilidad \(0\).
* **Verificación de suma:** para todos los contextos observados, la suma de las condicionales sobre \(\mathcal{V}\) dio una desviación máxima de \(1.11\times 10^{-16}\), muy por debajo de la tolerancia \(10^{-12}\).
* **Log-verosimilitud del entrenamiento:** se calculó
  \[
  \ell=\sum_{h}\sum_{y:\,c(h,y)>0} c(h,y)\log \hat q_{\text{MLE}}(y\mid h).
  \]
  Los valores obtenidos fueron:

  | \(n\) | \(\ell_{\text{MLE}}\) |
  |---:|---:|
  | 1 | \(-710\,787.7677\) |
  | 2 | \(-566\,543.6785\) |
  | 3 | \(-469\,869.2064\) |
  | 4 | \(-374\,887.9251\) |
  | 5 | \(-293\,251.1858\) |

* **Verificación de que la MLE maximiza la verosimilitud:** se eligió el contexto \(h=\texttt{" "}\) (espacio), con \(c(h)=45\,320\), y se aplicaron dos perturbaciones que mueven \(0.01\) de probabilidad:
  - Perturbación A: de `e` a `d`.
  - Perturbación B: de `e` a un símbolo con conteo cero en ese contexto.
  Los resultados fueron \(\ell_{\text{MLE}}=-566\,543.6785\), \(\ell_A=-566\,591.3136\) y \(\ell_B=-567\,021.2821\). La MLE es mayor en ambos casos, como exige la Proposición 1.1.8.
* **Evaluación en validación:** se evaluaron los \(31\,578\) caracteres de validación para cada \(n\). Para las primeras \(n-1\) posiciones se tomó como contexto el final del entrenamiento. Los conteos siguieron siendo exclusivamente del entrenamiento; el bloque de prueba no se utilizó.
* **Tabla T2 (ceros de la MLE en validación):**

  | \(n\) | Contextos observados | \(n\)-gramas observados | Ceros | % ceros | Ceros por \(c(h)=0\) | Ceros por \(c(h,y)=0\) | BPC MLE |
  |---:|---:|---:|---:|---:|---:|---:|---:|
  | 1 | 1 | 27 | 0 | 0.0000 % | 0 | 0 | 4.0515 |
  | 2 | 27 | 413 | 0 | 0.0000 % | 0 | 0 | 3.2172 |
  | 3 | 413 | 3 620 | 50 | 0.1583 % | 0 | 50 | \(\infty\) |
  | 4 | 3 620 | 15 803 | 491 | 1.5549 % | 50 | 441 | \(\infty\) |
  | 5 | 15 803 | 41 148 | 2 171 | 6.8750 % | 491 | 1 680 | \(\infty\) |

* **Interpretación:**
  1. La MLE no tiene ceros en \(n=1\) ni en \(n=2\). El primer cero aparece en \(n=3\) (50 caracteres). Por eso el BPC MLE es finito para \(n=1,2\) e infinito para \(n=3,4,5\).
  2. Un solo cero basta para que el BPC sea infinito, porque \(\log_2(0)=-\infty\). El modelo asigna probabilidad cero a un evento que sí ocurrió.
  3. La proporción de ceros crece con \(n\): los contextos posibles crecen como \(27^{n-1}\), mientras el entrenamiento permanece fijo. Cada vez hay más contextos raros y menos datos por contexto.
  4. El plan general afirmaba que los ceros aparecerían para \(n\ge 2\). Los datos de este corpus muestran que el bigrama está completamente cubierto y que el fallo comienza en \(n=3\). El informe debe reportar el hecho empírico, no la suposición.
* **Archivos generados:** `codigo/fase2.py` y `tablas/T2_ceros_validacion.csv`.

---

## 10. Fase 3: Suavizado aditivo de Laplace y calibración de \(\alpha\)

**En palabras sencillas:** el suavizado consiste en sumar una pequeña cantidad \(\alpha\) a todos los conteos, incluso a los que valen cero. Así, ninguna combinación recibe probabilidad cero y la métrica de error deja de ser infinita.

* **Decisión:** se añadieron a `ModeloNgramas` los métodos `prob_suavizada` y `log_prob_suavizada`, con la fórmula de Laplace generalizada:
  \[
  \hat q_\alpha(y\mid h)=\frac{c(h,y)+\alpha}{c(h)+\alpha|\mathcal{V}|},\qquad \alpha>0.
  \]
* **Propiedades verificadas:**
  - La suma sobre \(\mathcal{V}\) es \(1\) para todo contexto, incluso si \(c(h)=0\).
  - Si \(c(h)=0\), la probabilidad se degrada a la uniforme \(1/|\mathcal{V}|=1/27\).
  - Todas las probabilidades son estrictamente positivas.
  - Para \(n=1\), la fórmula se reduce al suavizado de Laplace ordinario sobre unigramas.
* **Verificación numérica:** las desviaciones máximas de la suma fueron \(1.11\times10^{-16}\) o menores; la probabilidad mínima observada fue positiva en todos los órdenes. El contexto no visto `"    "` (cuatro espacios) devolvió \(1/27\) para los 27 símbolos. La prueba de `abracadabra` devolvió \(\hat q_1(b\mid a)=1/3\), como exige la Tabla 2 del enunciado.
* **Rejilla de calibración:** \(\alpha\in\{0.001,0.003,0.01,0.03,0.1,0.3,1.0\}\). Para cada \(n\) y cada \(\alpha\) se calculó el BPC de validación:
  \[
  \text{BPC}(n,\alpha)=-\frac{1}{N_{\text{val}}}\sum_{t=1}^{N_{\text{val}}}\log_2 \hat q_\alpha(x_t\mid h_t),
  \]
  con \(N_{\text{val}}=31\,578\) y contexto heredado en las primeras \(n-1\) posiciones.
* **Resultados de la calibración:**

  | \(n\) | \(\alpha^*\) | BPC de validación |
  |---:|---:|---:|
  | 1 | 1.0 | 4.0515 |
  | 2 | 0.001 | 3.2172 |
  | 3 | 0.1 | 2.6982 |
  | 4 | 0.03 | 2.2959 |
  | 5 | 0.03 | **2.1902** |

* **Interpretación:**
  1. El suavizado elimina los ceros y permite comparar los cinco modelos con una métrica finita.
  2. En \(n=1\) la curva es prácticamente plana: todos los \(\alpha\) producen el mismo BPC hasta la cuarta cifra decimal. El \(\alpha^*=1.0\) no debe interpretarse como un óptimo real.
  3. En \(n=2\) el mejor \(\alpha\) es muy pequeño, casi la MLE, porque no hay ceros en validación.
  4. En \(n=3,4,5\) el \(\alpha^*\) crece porque hay más dispersión de contextos. En \(n=3\), los valores \(\alpha=0.1\) y \(\alpha=0.03\) están casi empatados.
  5. El mejor modelo en validación es \(n=5\) con \(\alpha=0.03\), con BPC \(2.1902\). La comparación definitiva con el bloque de prueba se hará una sola vez en la Fase 4.
* **Archivos generados:** `codigo/fase3.py`, `tablas/F2_bpc_alpha.csv`, `figuras/F2_bpc_alpha.png` y `figuras/F2_bpc_alpha.pdf`.

---

## 11. Cierre de la Semana 2 y Revisión 1

* **Estado técnico:** las cuatro tareas técnicas de la Semana 2 están completadas: conteos y MLE, Tabla T2, suavizado de Laplace y calibración de \(\alpha\) con Gráfica F2.
* **Protocolo de prueba:** el bloque `datos/prueba.txt` no se utilizó en ninguna de estas fases. Se reserva para la evaluación única de la Fase 4.
* **Revisión 1:** realizada. El profesor pidió elegir los mejores \(\alpha^*(n)\) y justificar el porqué de esa elección; la justificación se documenta en la sección 12.
* **Siguiente paso:** comenzar la Semana 3 con la evaluación única en prueba, fijando los \(\alpha^*(n)\) obtenidos en validación.

---

## 12. Criterio de elección de \(\alpha^*\) (justificación para la Revisión 1)

**En palabras sencillas:** \(\alpha\) es la cantidad de "conteo falso" que se suma a cada símbolo para que ninguno quede con probabilidad cero. Elegir \(\alpha\) es decidir cuánto se corrige el modelo: poco deja pasar los ceros, mucho borra la señal del texto.

* **Regla de decisión:** para cada orden \(n\) se elige el valor de la rejilla que minimiza el BPC de validación:
  \[
  \alpha^*(n)=\arg\min_{\alpha\in\{0.001,\,0.003,\,0.01,\,0.03,\,0.1,\,0.3,\,1.0\}}\text{BPC}_{\text{val}}(n,\alpha).
  \]
* **Por qué en validación:** en entrenamiento, bajar \(\alpha\) siempre mejora el ajuste (el mínimo sería \(\alpha\to0\), la MLE); en prueba no se puede elegir porque el bloque está reservado para una sola evaluación. Validación es texto no visto pero disponible para decidir.
* **Los conteos no cambian:** \(c(h)\) y \(c(h,y)\) provienen solo del entrenamiento; validación únicamente compara modelos, de modo que no hay fuga de información.
* **Dilema que resuelve el mínimo:** con \(\alpha\) muy pequeño, un contexto nuevo recibe probabilidad casi nula y un solo cero dispara el BPC a \(\infty\); con \(\alpha\) muy grande, la distribución se aplana hacia la uniforme \(1/27\) y el BPC sube hacia \(\log_2 27=4.7549\).
* **Resultados y sensibilidad:**

  | \(n\) | \(\alpha^*\) | BPC\* | 2.º mejor | BPC del 2.º | Diferencia | \(c(h)\) medio | \(\alpha^*K\) |
  |---:|---:|---:|---:|---:|---:|---:|---:|
  | 1 | 1.0 | 4.051466 | 0.3 | 4.051468 | \(2.0\times10^{-6}\) | 252\,626 | 27.00 |
  | 2 | 0.001 | 3.217190 | 0.003 | 3.217194 | \(3.7\times10^{-6}\) | 9\,357 | 0.03 |
  | 3 | 0.1 | 2.698246 | 0.03 | 2.698294 | \(4.8\times10^{-5}\) | 612 | 2.70 |
  | 4 | 0.03 | 2.295908 | 0.1 | 2.296311 | \(4.0\times10^{-4}\) | 70 | 0.81 |
  | 5 | 0.03 | 2.190168 | 0.1 | 2.193726 | \(3.6\times10^{-3}\) | 16 | 0.81 |

* **Lectura por orden:**
  1. \(n=1\): no hay contexto y no hay ceros; la curva es plana (diferencias de \(10^{-6}\)) y el mínimo cae en el borde de la rejilla. \(\alpha^*=1.0\) no es un óptimo real.
  2. \(n=2\): no hay ceros en validación; el mejor \(\alpha\) es el más pequeño de la rejilla y coincide prácticamente con la MLE. El mínimo verdadero está en \(\alpha\to0\).
  3. \(n=3\): aparecen 50 ceros. El mínimo es 0.1, pero 0.03 queda a \(4.8\times10^{-5}\) bits: empate práctico. Con \(c(h)\approx612\), la masa de suavizado es solo \(0.4\,\%\) y suavizar resulta barato.
  4. \(n=4\): 491 ceros; mínimo en 0.03, con 0.1 a \(4.0\times10^{-4}\) bits. La masa de suavizado pesa \(1.1\,\%\).
  5. \(n=5\): 2\,171 ceros y el mínimo más definido, en 0.03. Aunque hay más ceros, los contextos son raros (\(c(h)\approx16\)): \(\alpha K=0.81\) ya representa casi \(5\,\%\) de la masa, y subir más \(\alpha\) castiga al \(93\,\%\) de caracteres que el modelo predice bien.
* **Solidez de la elección:** en \(n=5\) el mínimo está bien definido (el segundo queda a \(3.6\times10^{-3}\) bits); en \(n=3\) y \(n=4\), 0.03 y 0.1 son casi indistinguibles; en \(n=1\) y \(n=2\) el valor cae en el borde de la rejilla. Por eso, en el informe se afirma que se eligió el mínimo de la rejilla sobre validación, sin atribuir a los casos planos un óptimo estadístico fuerte.
* **Conclusión:** el mejor modelo en validación es \(n=5\) con \(\alpha=0.03\), BPC \(2.1902\) y perplejidad \(2^{2.1902}\approx4.56\). Los valores quedan fijados antes de abrir el bloque de prueba.


---

## 13. Fase 4: evaluación única en prueba y comprobaciones teóricas

* **Protocolo:** los \(\alpha^*(n)\) de la sección 12 se congelaron antes de abrir `datos/prueba.txt`. El script `codigo/fase4.py` tiene dos salvaguardas: `--validar` hace un ensayo sobre validación sin escribir nada, y la ejecución oficial se niega a repetirse si `tablas/T3_evaluacion_prueba.csv` ya existe (salvo `--forzar`). El ensayo reprodujo exactamente los BPC de la Fase 3, lo que valida el cálculo antes del disparo único.
* **Resultado (Tabla T3, \(N=31\,579\)):**

  | \(n\) | \(\alpha^*\) | BPC entreno | BPC prueba | PPL prueba |
  |---:|---:|---:|---:|---:|
  | 1 | 1.0 | 4.0592 | 4.0536 | 16.605 |
  | 2 | 0.001 | 3.2354 | 3.2122 | 9.268 |
  | 3 | 0.1 | 2.6872 | 2.7223 | 6.599 |
  | 4 | 0.03 | 2.1538 | 2.3461 | 5.085 |
  | 5 | 0.03 | **1.7320** | **2.2514** | **4.761** |

* **Lectura:** validación y prueba coinciden en elegir \(n=5\), con una diferencia de solo \(0.0612\) bits entre ambas estimaciones (\(2.1902\) vs \(2.2514\)). El BPC de entrenamiento cae de forma monótona hasta \(1.7320\), mientras el de prueba se aplana en torno a \(2.25\): la brecha crece con \(n\) y es la evidencia de sobreajuste que pide discutir el enunciado. En \(n=5\) el modelo ya memoriza fragmentos del entrenamiento y esa memorización no se traduce en mejor generalización.
* **Desigualdad de Gibbs (unigramas):** \(H(\hat p_{\text{prueba}})=4.047143\), \(H(\hat p_{\text{prueba}},\hat q)=4.053576\) y \(KL=0.006433\) bits. Se cumple \(H\le H(p,q)\) y la diferencia es pequeña porque el unigramas suavizado reproduce bien las frecuencias del bloque. Se verificó **solo con unigramas**, como indica el enunciado: comparar el BPC de un modelo condicionado contra la entropía marginal sería una comparación inválida.
* **Ley de los grandes números (Gráfica F4):** el promedio acumulado \(S_k\) del mejor modelo parte en \(8.9\) bits (primer carácter impredecible), cae rápido y se estabiliza alrededor de \(2.2514\) a partir de unos pocos miles de caracteres. Se graficó con **eje horizontal logarítmico**, porque en escala lineal la caída inicial comprimía toda la zona de convergencia. La figura se rehizo con `python3 fase4.py --solo-f4`, que recalcula el BPC y **verifica que coincide con T3** antes de tocar la imagen; no se repitió ninguna decisión.
* **Gráfica F3:** BPC de entrenamiento y de prueba contra \(n\) en la misma gráfica. Las curvas se separan desde \(n=3\), justo cuando aparecen los ceros en validación y el suavizado empieza a tener un costo apreciable.
* **Archivos generados:** `codigo/fase4.py`, `tablas/T3_evaluacion_prueba.csv`, `tablas/T3_gibbs.csv`, `figuras/F3_bpc_n.png/.pdf` y `figuras/F4_promedio_acumulado.png/.pdf`.

---

## 14. Fase 5: simulación y distribución estacionaria

* **Matriz de transición:** se construyó \(P\) de \(27\times27\) con el bigrama suavizado en \(\alpha^*=0.001\), leyendo \(P_{ij}=q(V_j\mid V_i)\) (filas = contexto, columnas = símbolo siguiente). La desviación máxima de las sumas de fila respecto de 1 es \(2.22\times10^{-16}\) y la entrada mínima es \(2.207\times10^{-8}\): la matriz es estocástica y estrictamente positiva.
* **Distribución estacionaria:** se calculó por iteración de potencias \(\pi_{t+1}=\pi_tP\) partiendo de la uniforme, hasta que el cambio en norma \(\ell_1\) bajó de \(10^{-10}\). Convergió en **22 iteraciones** con última diferencia \(3.35\times10^{-11}\) y \(\sum_i\pi_i=1\) hasta el error de máquina.
* **Comparación con unigramas (Gráfica F5):** la diferencia máxima entre \(\pi\) y las frecuencias empíricas del entrenamiento es \(3.71\times10^{-6}\) y la distancia \(\ell_1\) es \(9.05\times10^{-6}\). Es decir, \(\pi\) reproduce esencialmente la distribución de unigramas. Esto confirma numéricamente la propiedad ergódica: al ser \(P\) positiva, la cadena es irreducible y aperiódica, tiene una única distribución estacionaria y esa distribución coincide con el vector de frecuencias relativas del texto de entrenamiento.
* **Muestras (Anexo, `tablas/T5_muestras.csv`):** se generaron 300 caracteres para \(n=2,3,5\) con semilla `2026`, contexto inicial `"habia "` y los \(\alpha^*\) correspondientes.
  * \(n=2\) produce pseudo-español: sílabas y palabras cortas plausibles (`"de que"`, `"lespostes"`). Los `#` que aparecen en medio de palabras no son saltos de línea: `#` agrupa toda la puntuación, las tildes, la `ñ` y los dígitos (sección 5 de esta bitácora), así que `m#s` es «más» y `a#o` es «año».
  * \(n=3\) mejora la localidad de las sílabas (`"menesto"`, `"aparadia"`, `"precurre"`) pero pierde estructura global.
  * \(n=5\) alterna fragmentos memorizados del entrenamiento (`"contaba porque no"`, `"maravillo dudar"`) con tramos de letras sin estructura (`"dhyqzl..."`). La causa es doble: el modelo solo mira 4 caracteres de contexto y, cuando el contexto es nuevo, el suavizado reparte la probabilidad casi uniforme entre los 27 símbolos. Con \(c(h)\) medio de 16, esos contextos raros son frecuentes durante la generación.
* **Conclusión de la fase:** la simulación confirma lo que ya insinuaba el BPC. Aumentar \(n\) mejora la predicción local (baja el BPC) pero no produce texto globalmente coherente: el modelo de n-gramas no tiene memoria más allá de \(n-1\) caracteres. Es una limitación estructural, no un error de implementación.
* **Archivos generados:** `codigo/fase5.py`, `tablas/T5_muestras.csv` y `figuras/F5_pi_unigramas.png/.pdf`.

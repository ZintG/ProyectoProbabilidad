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

## 11. Cierre de la Semana 2 y preparación de la Revisión 1

* **Estado técnico:** las cuatro tareas técnicas de la Semana 2 están completadas: conteos y MLE, Tabla T2, suavizado de Laplace y calibración de \(\alpha\) con Gráfica F2.
* **Protocolo de prueba:** el bloque `datos/prueba.txt` no se utilizó en ninguna de estas fases. Se reserva para la evaluación única de la Fase 4.
* **Hito pendiente:** la Revisión 1 con el profesor. Debe presentarse con la Tabla T2, la Gráfica F2 y los valores \(\alpha^*(n)\) seleccionados.
* **Siguiente paso:** una vez realizada la Revisión 1, comenzar la Semana 3 con la evaluación única en prueba, fijando los \(\alpha^*(n)\) obtenidos en validación.


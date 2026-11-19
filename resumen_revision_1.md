# Resumen para la Revisión 1

**Proyecto:** Modelos de $n$-gramas para el idioma español a partir de *Niebla* de Miguel de Unamuno
**Institución:** Facultad Experimental de Ciencias y Tecnología (FaCyT) — Universidad de Carabobo
**Hito:** Revisión 1 — cierre de las Semanas 1 y 2
**Fecha:** 15 de noviembre de 2026

---

## 1. Objetivo del proyecto

El proyecto estudia, con herramientas de teoría de la probabilidad, si el español literario presenta regularidades estadísticas que permitan predecir el siguiente carácter de un texto. Para ello se construyen cinco modelos de $n$-gramas ($n = 1, 2, 3, 4, 5$), se mide su desempeño sobre texto no visto y se aplica un mecanismo de suavizado que corrige el fallo característico de estos modelos.

Un **modelo de $n$-gramas** es un modelo que asigna una probabilidad al siguiente símbolo de una secuencia observando únicamente los $n-1$ símbolos inmediatamente anteriores, llamados **contexto**. Por ejemplo, en un modelo de orden $n=3$ (trigramas), la probabilidad de la letra `a` depende solo de los dos caracteres que la preceden. Es una aproximación deliberadamente simple: supone que el texto no tiene memoria más allá de esos $n-1$ caracteres.

---

## 2. Semana 1: preparación del corpus

Se seleccionó la novela *Niebla (Nivola)* (1914), de Miguel de Unamuno, disponible en Project Gutenberg (eBook #49836). El texto se sometió a tres operaciones:

1. **Limpieza editorial:** se eliminaron la nota de transcripción inicial y el índice final de capítulos.
2. **Normalización:** todo el texto se convirtió a minúsculas, y cualquier secuencia de espacios, tabuladores o saltos de línea se redujo a un solo espacio.
3. **Definición del alfabeto:** las 26 letras del abecedario más el espacio en blanco forman el alfabeto permitido; todo carácter restante (tildes, `ñ`, dígitos, signos de puntuación) se sustituyó por el símbolo especial `#`.

El texto resultante tiene **315,783 caracteres** y un vocabulario de **$|\mathcal{V}| = 27$ símbolos** (el espacio, el símbolo `#` y 25 letras, ya que la obra no emplea la letra `w`).

El texto se dividió en tres bloques contiguos, sin mezclar ni barajar, para evitar que información del futuro se filtrara hacia el entrenamiento:

| Bloque | Porcentaje | Caracteres | Uso |
| :--- | :---: | ---: | :--- |
| Entrenamiento | 80 % | 252,626 | Ajustar los modelos |
| Validación | 10 % | 31,578 | Elegir el parámetro $\alpha$ |
| Prueba | 10 % | 31,579 | Evaluación final, una sola vez |

En esta etapa también se calculó la frecuencia de cada símbolo y la entropía empírica de Shannon, y se generaron la Tabla T1 y la Gráfica F1. La entropía mide, en bits, la incertidumbre media al predecir un carácter; su valor máximo posible con 27 símbolos es $\log_2 27 \approx 4.7549$ bits, y la diferencia entre ese máximo y la entropía observada se denomina **redundancia** del idioma. Para este corpus la entropía empírica resultó $H(\hat{p}) = 4.0592$ bits y la redundancia $R = 1 - H(\hat{p})/H_{\max} = 14.63\ \%$: la distribución de frecuencias de los símbolos se aparta de la uniforme en ese porcentaje.

Además se verificó la prueba de cordura con la palabra *«abracadabra»*, que reproduce exactamente los valores de referencia del enunciado y confirma que los conteos y las probabilidades están bien programados.

---

## 3. Semana 2: estimación, fallo de ceros y suavizado

### 3.1 Estimación por máxima verosimilitud (MLE)

La probabilidad de un símbolo $y$ dado un contexto $h$ se estima contando cuántas veces apareció el par en el entrenamiento y dividiendo entre cuántas veces apareció el contexto:

$$
\hat{q}_{\text{MLE}}(y \mid h) = \frac{c(h, y)}{c(h)}.
$$

Aquí $c(h,y)$ es el número de veces que el contexto $h$ fue seguido por $y$, y $c(h)$ es el número de veces que apareció $h$. Se comprobó numéricamente que, para cada contexto, la suma de estas probabilidades sobre los 27 símbolos es igual a 1, con un error máximo del orden de $10^{-16}$. También se verificó, mediante dos perturbaciones controladas, que esta estimación es la que maximiza la verosimilitud de los datos de entrenamiento.

### 3.2 El problema de los ceros

Al evaluar los modelos sobre el bloque de validación se contaron las posiciones cuya probabilidad asignada es cero. El resultado se resume en la Tabla T2:

| $n$ | Ceros | % de ceros | Bits por carácter (MLE) |
|---:|---:|---:|---:|
| 1 | 0 | 0.0000 % | 4.0515 |
| 2 | 0 | 0.0000 % | 3.2172 |
| 3 | 50 | 0.1583 % | $\infty$ |
| 4 | 491 | 1.5549 % | $\infty$ |
| 5 | 2,171 | 6.8750 % | $\infty$ |

La métrica usada es el **BPC** (bits por carácter): el promedio del costo en bits de codificar cada carácter de validación. Un solo cero basta para volverla infinita, porque $\log_2 0 = -\infty$: el modelo declara imposible un evento que sí ocurrió.

Dos observaciones son relevantes para el informe:

- El fallo **no comienza en $n=2$**, como suponía el plan inicial. En este corpus los bigramas están completamente cubiertos y el primer cero aparece en $n=3$.
- La proporción de ceros crece con $n$: el número de contextos posibles crece como $27^{n-1}$, mientras el entrenamiento permanece fijo en 252,626 caracteres. Cada vez hay más contextos poco frecuentes y menos datos para estimarlos.

### 3.3 Suavizado de Laplace y calibración de $\alpha$

El suavizado aditivo suma una cantidad positiva $\alpha$ a todos los conteos, incluidos los que valen cero:

$$
\hat{q}_\alpha(y \mid h) = \frac{c(h,y) + \alpha}{c(h) + \alpha\,|\mathcal{V}|}.
$$

Con ello ninguna probabilidad es cero y, cuando un contexto nunca fue visto, la distribución se degrada a la uniforme $1/27$. Se verificó que las probabilidades siguen sumando 1 en todos los casos y que todas son estrictamente positivas.

El valor de $\alpha$ no se elige a ojo: se probó una rejilla de siete valores sobre el bloque de validación y se conservó, para cada orden $n$, el que produce el menor BPC. Los resultados son:

| $n$ | $\alpha^*$ | BPC de validación |
|---:|---:|---:|
| 1 | 1.0 | 4.0515 |
| 2 | 0.001 | 3.2172 |
| 3 | 0.1 | 2.6982 |
| 4 | 0.03 | 2.2959 |
| 5 | 0.03 | **2.1902** |

El modelo con mejor desempeño en validación es el de orden $n=5$ con $\alpha = 0.03$, con 2.1902 bits por carácter. En $n=1$ la curva es prácticamente plana, por lo que su $\alpha^* = 1.0$ no representa un óptimo real.

El criterio de elección fue, en todos los casos, minimizar el BPC de validación: los conteos provienen solo del entrenamiento y la validación únicamente compara modelos. En $n=1$ y $n=2$ el mínimo cae en el borde de la rejilla porque no hay ceros que corregir; en $n=3$ y $n=4$, los valores $0.03$ y $0.1$ son casi indistinguibles (diferencias menores a $5\times10^{-4}$ bits); en $n=5$ el mínimo es claro y el segundo mejor queda a $3.6\times10^{-3}$ bits. Por eso los $\alpha^*$ se reportan como el mínimo de la rejilla sobre validación, sin atribuir a los casos planos un óptimo estadístico fuerte.

---

## 4. Estado y siguientes pasos

Las cuatro tareas técnicas de la Semana 2 están concluidas: conteos y MLE, Tabla T2, suavizado de Laplace y calibración de $\alpha$ con su Gráfica F2. El bloque `datos/prueba.txt` no se ha utilizado en ninguna etapa y se reserva para una única evaluación en la Fase 4.

El siguiente paso es la evaluación definitiva sobre el bloque de prueba con los valores $\alpha^*(n)$ ya fijados, seguida de las fases de simulación, análisis de cadenas de Markov y cuantificación de la incertidumbre mediante bootstrap.

---

## 5. Glosario mínimo

| Término | Significado |
| :--- | :--- |
| **$n$-grama** | Secuencia de $n$ símbolos consecutivos. |
| **Contexto ($h$)** | Los $n-1$ símbolos que preceden al símbolo que se quiere predecir. |
| **Vocabulario ($\mathcal{V}$)** | Conjunto de símbolos distintos que aparecen en el texto; aquí $|\mathcal{V}| = 27$. |
| **$c(h)$ / $c(h,y)$** | Número de apariciones del contexto / del par contexto-símbolo en el entrenamiento. |
| **MLE** | Estimación por máxima verosimilitud: la frecuencia relativa observada. |
| **Suavizado** | Técnica que añade una pseudomasa $\alpha$ a los conteos para evitar probabilidades cero. |
| **BPC** | Bits por carácter: promedio del costo en bits de codificar el texto evaluado. |
| **Perplejidad** | $2^{\text{BPC}}$; puede interpretarse como el número de alternativas equiprobables que el modelo considera. |
| **Entropía** | Medida de la incertidumbre media de una distribución, en bits. |
| **Redundancia** | Parte de la capacidad teórica de un alfabeto que el idioma no utiliza, por su estructura repetitiva. |

---

## 6. Archivos de respaldo de esta revisión

- `codigo/fase1.py`, `tablas/T1_particiones.csv`, `figuras/F1_frecuencias.pdf` y `.png` — Semana 1.
- `codigo/modelos.py` — clase `ModeloNgramas`: conteos, MLE, log-verosimilitud y suavizado.
- `codigo/fase2.py`, `tablas/T2_ceros_validacion.csv` — ceros y BPC de la MLE.
- `codigo/fase3.py`, `tablas/F2_bpc_alpha.csv`, `figuras/F2_bpc_alpha.pdf` y `.png` — calibración de $\alpha$.
- `decisiones_informe.md` — bitácora completa de decisiones y resultados.

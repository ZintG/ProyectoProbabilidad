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


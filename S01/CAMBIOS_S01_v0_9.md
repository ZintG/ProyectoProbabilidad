# CAMBIOS S01 · v0.8 → v0.9

**Sesión:** S01 «El lenguaje como distribución de probabilidad» (Cap. I, §1.1).
**Fecha:** 31-10-2026. **Ciclo:** Fases 1–5 completas; Fase 2 aprobada por el autor el 31-10-2026 (índice; resultados auxiliares: Beta–Gamma e integral de Dirichlet demostradas, estacionaria demostrada para $P>0$ y citada en general, ley de los grandes números citada; recuperar los ocho bloques de v0.6).
**Decisiones aplicadas:** (1) $V$ conjunto, $|V|$ tamaño; (2) «codificación por pares de bytes (Byte Pair Encoding, BPE)»; (3) PDF de estudiante empaquetados.

---

## 1. Resultado verificable

| Comprobación | v0.8 | v0.9 |
|---|---|---|
| `compilar_libro.sh` | 341 pp., 0 sin resolver | **357 pp.** (S01: pp. 3–47), **0** referencias o citas sin resolver, **0** etiquetas duplicadas, **0** cajas desbordadas |
| `contenido_libro.tex` | 1652 líneas | 2685 líneas |
| Regla 1 (`verificar_terminologia_s01.py`) | — (10 usos antes de definir) | **37 términos, 0 usos antes de la definición** |
| Regla 7 (`control_latex.py`) | 2 tabulaciones, 12 remisiones residuales, 24 enlaces rotos | **0** |
| Números nuevos (`verificar_complementos_s01.py`) | — | **47 comprobaciones, 0 fallos** |
| `verificar_s01.py` | pasa | pasa |
| `verificar_s01_estudiante.py --estricto` | (no existía; v0.5 fallaba) | pasa, incluida la ausencia de soluciones |
| Paridad R–Python (`comparar_r_python.py`) | PENDIENTE (sin R) | **concordancia exacta** (desviación 0 en BPC y BPE) con R 4.3.3 y configuración UTF-8 |
| Beamer `p01.tex` | 31 diapositivas | 66 diapositivas (14 del anexo «continúa en curso posterior»), 0 desbordes |
| Enlaces de la interactiva | 6 PDF inexistentes | 4 PDF presentes en `presentaciones/pdf/` y `sesiones/S01/pdf/` |

## 2. Archivos

**Modificados:** `sesiones/S01/contenido_libro.tex` (archivo completo), `sesiones/S01/p01.tex` (archivo completo), `presentaciones/S01/p01_interactiva.Rmd` y `.html` (y sus copias idénticas en `sesiones/S01/presentacion/`), `capitulos/capitulo_01.tex` ($|V|$, l. 38–40), `estilo/preambulo_curso.tex` (entorno `teorema`, macros `\iniciarcomplementos`, `\complemento`, `\volvera`), `bibliografia/curso_unificado.bib` (4 fichas), `sesiones/S01/s01_integrada.tex` (ahora compila el texto del libro), `sesiones/S01/COMPILAR.sh`, `sesiones/S01/modulos/{30,32,50}_*.tex` (rutas `código/`→`codigo/`, tabulación, «la guía»), `sesiones/S01/codigo/{experimento_s01,ic10_tokenizadores}.R` (argumento `fileEncoding`), `sesiones/S01/ESTADO_R_PYTHON.md`, `sesiones/S01/verificaciones/verificar_s01.py` (rótulo) y `verificar_s01_v05.py` (nota de alcance).

**Nuevos:** `sesiones/S01/verificaciones/{control_latex,verificar_s01_estudiante,verificar_complementos_s01,verificar_terminologia_s01}.py`, `REGISTRO_TERMINOLOGIA_S01.csv`, `sesiones/S01/experimentos/resultados_R.csv`, `resultados_ic10_R.csv`, `sesiones/S01/pdf/` y `presentaciones/pdf/` (s01_integrada, labcomp01, t01, reporte_ejemplo_ejecutado), `sesiones/S01/s01_integrada_modular_v0_8.tex` (manual modular v0.8 conservado).

**No tocados:** `fuentes_historicas/`, `control/fuentes_integradas_v0_7/` y el resto de las sesiones. No se añadió ninguna solución al paquete (comprobado por el verificador).

**Scripts de la edición (reproducibles):** `aplicar_lote0_s01.py`, `ensamblar_s01_v0_9.py` (+ `MAPA_S01_v08_a_v09.csv`), `postajustes_s01_v0_9.py` (+ `POSTAJUSTES_S01.log`), `actualizar_rmd_s01_v0_9.py`, `sincronizar_html_s01_v0_9.py`. Huellas de v0.8: `SHA256_S01_v0_8_previos.txt`.

## 3. Estado de los 62 hallazgos del diagnóstico

| H. | Estado y lugar en v0.9 |
|---|---|
| 1–2 (E) tabulaciones | Corregidas (Lote 0). Ninguna en el proyecto. |
| 3–6 (E) «parte II», «siguiente parte», «el suplemento», «la guía» | Sustituidas por `\ref` a secciones, proposiciones y complementos. `control_latex.py`: 0. |
| 7–8 (E) rutas y erratas | Corregidas en el libro (Lote 0) y en los módulos empaquetados (`código/`→`codigo/`). |
| 9–10 (E) encabezados vacíos; sección sin número | Sustituidos por «Complementos matemáticos de S01» (§1.1.9), con 12 complementos numerados S01.C1–C12. |
| 11 (E) contenido metodológico | Movido a §1.1.6 (l. 1523–1544). |
| 12 (E) verificador v0.5 | `verificar_s01_estudiante.py` nuevo; v0.5 anotado como docente. |
| 13 (E) enlaces | PDF compilados y empaquetados; `labmat01` y `sup01` redirigidos a `s01_integrada.pdf`. |
| 14 (E) bibliografía | Cita a Chollet y Allaire; 4 fichas nuevas verificadas (páginas de Gage pendientes). Las claves duplicadas preexistentes se conservan (afectan a otras sesiones). |
| 15–30 (T) | Todos los términos definidos antes del uso (§4 y registro). Los tres hallazgos sobre BOS/EOS, bootstrap e IC10 se resolvieron con definiciones en su primer uso. |
| 31 (M) observación de la hipótesis retirada | Presente en cada resultado (bloques `observacion` o párrafo final). |
| 32–47 (M) | Deducciones completas: regla de la cadena (Prop. 1.1.3), MLE (Prop. 1.1.8 y C4 con KKT y Gibbs), Bayes y Dirichlet (Teo. 1.1.12, Props. 1.1.13–1.1.14, C5, C6), cotas de la entropía con Jensen, Gibbs con su lema, entropía condicional y «condicionar no aumenta la entropía» (C7), regla de la cadena de la KL, suma logarítmica y procesamiento de datos (C8), estacionaria con prueba para $P>0$ y eliminación paso a paso, tasa de entropía (C9), parada geométrica deducida (C10), BPE con contraejemplo verificado (C11), bootstrap definido (C12). |
| 48–56 (N) | Tabla de notación (l. 24–56) y renombrados: alfabeto en `\texttt`, $s(x)$, $\rho_t$, $\pi_0$/$\pi$, $H_\infty$, $M$, $t_{\max}$, $k$, $\Delta_j$/$J$, $|z|$, $\operatorname{bits}(z)$, $V_A$/$V_{\rm ej}$/$V_{\rm sal}$, $\langle/\mathrm w\rangle$, $\langle\mathrm s\rangle$/$\langle/\mathrm s\rangle$. Cambio de $V$ declarado (Regla 5). |
| 57–62 (P) | Beamer y la interactiva reescritas con la notación del libro, las deducciones y el anexo «continúa en curso posterior». |

## 4. Bloques recuperados de v0.6 (`fuentes_historicas/contenido_libro_v0_6.tex`)

| ID | v0.6 | v0.9 | Adaptación |
|---|---|---|---|
| R1 | l. 66–74 «Cuatro alcances» | l. 13–22 | IC10 → remisión a §1.1.6 |
| R1 | l. 38–42 «Dos preguntas, dos mediciones» | l. 973–978 | Situado en §1.1.5, porque usa BPC y BPE |
| R2 | l. 431–448 «¿Por qué existen las subpalabras?» | l. 247–299 | Figura alineada con la tabla de fusiones ($\langle/\mathrm w\rangle$, pasos 1–3) |
| R3 | l. 681–702 «Suavizado como regularización» | l. 713–726 | — |
| R4 | l. 704–726 «Perplejidad: tres lecturas» | l. 921–933 | $r_t\to\rho_t$ |
| R5 | l. 753–774 «De muestras a poblaciones» | l. 879–905 | Proposición con prueba; ley de los grandes números citada |
| R6 | l. 837–844 contexto `b`, $\alpha=1/2$ | l. 727–734 | — |
| R7 | l. 932–952 «Cierre del laboratorio matemático» | l. 1231–1248 | «unidad de resampling» → «unidad de remuestreo» |
| R8 | l. 1235–1242 invariante de BPE | C11 | — |

## 5. Correspondencia antiguo → nuevo de `contenido_libro.tex`

| v0.8 (líneas) | Tratamiento | v0.9 (líneas, aprox.) |
|---|---|---|
| — | nuevo / recuperado / adaptado: `F00_preliminares` | 1–4 |
| 2–6 | conservado | 5–9 |
| — | nuevo / recuperado / adaptado: `F00b_alcances_notacion` | 11–59 |
| — | nuevo / recuperado / adaptado: `F01_idea_llm` | 60–68 |
| 16–40 | conservado | 71–93 |
| — | nuevo / recuperado / adaptado: `F02_ngrama_op` | 96–107 |
| 48–129 | conservado con 1 sustitución(es) | 109–189 |
| — | nuevo / recuperado / adaptado: `F03_def_vocabulario` | 190–195 |
| 130–178 | conservado con 2 sustitución(es) | 199–243 |
| — | nuevo / recuperado / adaptado: `F04_bpe` | 247–299 |
| 179–209 | conservado con 2 sustitución(es) | 300–326 |
| 210–332 | conservado con 20 sustitución(es) | 331–450 |
| — | nuevo / recuperado / adaptado: `F05_cadena` | 454–489 |
| — | nuevo / recuperado / adaptado: `F06_markov` | 490–513 |
| 347–361 | conservado | 515–526 |
| — | nuevo / recuperado / adaptado: `F07_mle` | 529–603 |
| — | nuevo / recuperado / adaptado: `F08_dirichlet` | 604–737 |
| 388–390 | conservado | 739–739 |
| — | nuevo / recuperado / adaptado: `F09_idea_bit` | 741–748 |
| 398–423 | conservado con 1 sustitución(es) | 752–773 |
| 430–451 | conservado con 2 sustitución(es) | 776–796 |
| — | nuevo / recuperado / adaptado: `F10_cotas` | 798–825 |
| — | nuevo / recuperado / adaptado: `F11_condicional` | 826–842 |
| — | nuevo / recuperado / adaptado: `F12_kl` | 843–869 |
| 464–472 | conservado con 1 sustitución(es) | 870–875 |
| — | nuevo / recuperado / adaptado: `F13_riesgo` | 879–905 |
| 473–487 | conservado con 1 sustitución(es) | 907–920 |
| — | nuevo / recuperado / adaptado: `F14_ppl_r4` | 921–933 |
| 488–490 | conservado | 935–936 |
| — | nuevo / recuperado / adaptado: `F15_bpc` | 937–947 |
| 491–513 | conservado con 1 sustitución(es) | 948–970 |
| — | nuevo / recuperado / adaptado: `F19_dos_preguntas` | 971–978 |
| 514–664 | conservado con 12 sustitución(es) | 980–1128 |
| — | nuevo / recuperado / adaptado: `F16_L4` | 1135–1151 |
| 679–754 | conservado con 3 sustitución(es) | 1153–1229 |
| — | nuevo / recuperado / adaptado: `F17_cierre_lab` | 1231–1248 |
| 755–1026 | conservado con 1 sustitución(es) | 1253–1519 |
| 1111–1115 | movido a §1.1.6 (1 sustitución) | 1523–1527 |
| 1543–1560 | movido a §1.1.6 | 1529–1544 |
| 1027–1035 | conservado | 1546–1554 |
| 1593–1651 | conservado con 7 sustitución(es) | 1560–1615 |
| — | nuevo / recuperado / adaptado: `F18_vocabulario` | 1618–1636 |
| 1583–1588 | conservado | 1639–1644 |
| — | nuevo / recuperado / adaptado: `C01_C02` | 1646–1744 |
| — | nuevo / recuperado / adaptado: `C03_C04` | 1746–1918 |
| — | nuevo / recuperado / adaptado: `C05_C06` | 1920–2062 |
| — | nuevo / recuperado / adaptado: `C07_C08` | 2064–2276 |
| — | nuevo / recuperado / adaptado: `C09_C10` | 2278–2560 |
| — | nuevo / recuperado / adaptado: `C11_C12` | 2562–2685 |

**Destino del antiguo «Demostraciones y profundización» (v0.8, l. 1041–1559), sin pérdida de contenido:** símplex y soporte (1046–1053) → C1; regla de la cadena, Markov y parámetros (1054–1077) → C2; existencia del MLE (1079–1087) → C4; Dirichlet (1088–1101) → C6, con la deducción en el texto principal; compromiso (1102–1110) → C6; selección y evaluación (1111–1115) → §1.1.6; entropía, cotas, Gibbs, H+KL, no métrica (1117–1164) → C3; KL sobre secuencias (1165–1175) → C8; perplejidad, probabilidad inicial, BPC, PPL↔BPC (1177–1211) → C10; BPE (1212–1226) → C11; procesamiento de datos (1227–1280) → C8; contexto y entropía condicional (1282–1325) → C7; cadenas de Markov (1329–1381) → C9; entropía condicional y tasa (1383–1432) → C7 y C9; soporte, final de secuencia y parada (1434–1476) → C10; códigos ideales (1478–1500) → C10; regla de puntuación propia (1502–1507) → C3; incertidumbre experimental (1509–1542) → C12; ventaja metodológica (1544–1559) → §1.1.6.

## 6. Supresiones registradas (Regla 6)

- «Por Bayes la posterior es Dirichlet(…)» (v0.8 l. 1095) y «Se demuestra integrando…» (l. 1098–1099): sustituidas por la deducción completa (Props. 1.1.13–1.1.14 y C5). Eran el salto que el autor pidió eliminar.
- «Para un máximo interior… La solución en todo el símplex…» (l. 368–375): sustituido por la Proposición 1.1.8, que prueba el caso del borde.
- Encabezados vacíos (l. 1046, 1079, 1117, 1177, 1227, 1329) y etiqueta `s01:mod:sup` (l. 1045, sin usos): retirados con la reestructuración.
- Glosario del vocabulario de consulta (l. 1571–1580): sustituido por la versión con remisiones; «Cadena de Markov» se redefine con precisión.
- «Si $K$ crece, la masa agregada aumenta» (l. 1110): precisado como Proposición de la masa de lo no visto (C6).

## 7. Números nuevos o modificados (todos verificados con código)

Moda de $\mathrm{Dir}(8,5,3,2,2)$ $=(7,4,2,1,1)/15$ y media $(8,5,3,2,2)/20$; con $\alpha=1$ la moda es el MLE $(6,3,1,0,0)/10$; predictivas $(7,4,2,1,1)/15$ y $(13,7,3,1,1)/25$; $\lambda=2/3$ y $1/11$; $\widehat P_{1/2}(\cdot\mid\texttt b)=(5/9,1/3,1/9)$; masa de lo no visto $2/15$ ($K=5$) y $97/110$ ($K=100$); eliminación $w=\frac{75}{98}u$, $v=\frac{108}{98}u$ y $\pi=(98,108,75)/281$ (exacto); factor de contracción $4/7$; $H(\pi)\approx1.568836$ y $H_\infty\approx1.472301$ bits; contraejemplo BPE $59\to45$ (voraz) frente a $59\to43$ (óptimo); $6^6=46656$ remuestras e intervalo $[-0.66771,-0.42038]$ reproducido; Gamma, Beta e integral de Dirichlet comprobadas por cuadratura; parada geométrica $\mathbb E[M]=(1-r)/r$; Kraft $\{0,10,11\}$.

## 8. Presentaciones y PDF

- **`p01.tex`** (archivo completo): orden y notación del libro, Regla 1 en las diapositivas (LLM, BPE, MLE, KL, PPL, BPC, KKT, IC10, Q1 definidos en su primera aparición), deducciones de cadena, MLE, Bayes y Dirichlet, cotas, Gibbs y PPL↔BPC, contraejemplo BPE, bootstrap, y anexo C1–C12 marcado «continúa en curso posterior».
- **`p01_interactiva.Rmd`**: 39 cambios sincronizados (notación, terminología, secciones nuevas 2.4 y 2.5, anexo de complementos, enlaces).
- **`p01_interactiva.html`**: la carcasa de proyección original no procede de knitr, así que se conservó y se sustituyeron por pandoc (`--mathml`) solo las 13 secciones cambiadas, con 3 secciones nuevas. Probado en Chrome sin interfaz: sin errores de JavaScript; navegación y pestañas 2.4 y 2.5 operativas.
- **PDF de estudiante:** `s01_integrada.pdf` (48 pp.: el texto de S01 tal como entra al libro, con sus complementos y bibliografía), `labcomp01.pdf`, `t01.pdf` y `reporte_ejemplo_ejecutado.pdf`, en `presentaciones/pdf/` y `sesiones/S01/pdf/`. `labmat01.tex` y `sup01.tex` se conservan como fuentes, pero no se empaquetan: su contenido está en el libro.
- **Maquetación:** la tabla de notación pasa a `longtable`; se corrige la superposición de etiquetas en la figura 1.1.2, un defecto previo de v0.8.

## 9. Código

`write.csv(..., encoding='UTF-8')` → `fileEncoding='UTF-8'` en `experimento_s01.R` (l. 57) e `ic10_tokenizadores.R` (l. 67): el argumento no existe y detenía ambos programas, que nunca se habían ejecutado. Con R 4.3.3 y `LC_ALL=C.UTF-8` la paridad es exacta. Con la configuración POSIX, `ic10_tokenizadores.R` da 149/152 en lugar de 148/127, por la segmentación de las tildes; el requisito queda indicado en los comandos del libro y en `ESTADO_R_PYTHON.md`.

## 10. Pendientes registrados (no requieren decisión ahora)

1. **Fichas:** las páginas de Gage (1994) y la numeración exacta de capítulos y teoremas citados (Cover y Thomas, caps. 2, 3 y 5; Boyd y Vandenberghe, sec. 5.5.3; Norris, secs. 1.7–1.8) deben confirmarse contra los ejemplares.
2. **S04:** adoptar $|V|$ para el tamaño del vocabulario y desambiguar $V$ como matriz de valores de atención (el solucionario docente ya advierte del choque).
3. **Volumen docente:** el solucionario usa la notación antigua (`(a, fin)`, $K$, `afin`); conviene alinearlo cuando se revise ese volumen, fuera del paquete del estudiante.
4. **Plantilla HTML común (S01–S12):** su pie dice «Material docente interactivo» también en el paquete del estudiante.
5. **Claves duplicadas** en `curso_unificado.bib` (`cover2006`/`cover2006elements`, etc.): unificarlas al revisar las sesiones que las usan.

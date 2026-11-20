# Traspaso a la Semana 4

Documento de continuidad: todo lo que necesita una sesión nueva para seguir sin releer el historial.
Última actualización: 19/11/2026.

## 1. Estado del proyecto

Semanas 1–3 cerradas, verificadas y subidas. Repositorio en GitHub `ZintG/ProyectoProbabilidad`,
rama `main`, último commit `611da9b` (local y remoto sincronizados, git por SSH, sin tokens).

**Alcance de la Semana 4:** solo las cinco primeras tareas. Quedan fuera el ensayo de la defensa
y el empaquetado `.zip`.

## 2. Las cinco tareas, en orden

1. Estructurar y redactar el reporte en LaTeX (10–14 páginas estrictas, sin anexos).
2. Responder formalmente las 11 preguntas de discusión teórica en la sección 7.
3. Integrar figuras vectoriales (`.pdf`/`.png`) y tablas exportadas desde Python.
4. Verificar que todo el flujo corra desde consola en menos de 10 minutos (`codigo/main.py`).
5. Redactar el `README.md` final con instrucciones reproducibles paso a paso.

## 3. Cifras congeladas (no recalcular ni cambiar)

`datos/prueba.txt` se evaluó **una sola vez**. Los $\alpha^*$ están congelados.

| $n$ | $\alpha^*$ | BPC entreno | BPC prueba | PPL prueba |
|---:|---:|---:|---:|---:|
| 1 | 1.0 | 4.0592 | 4.0536 | 16.605 |
| 2 | 0.001 | 3.2354 | 3.2122 | 9.268 |
| 3 | 0.1 | 2.6872 | 2.7223 | 6.599 |
| 4 | 0.03 | 2.1538 | 2.3461 | 5.085 |
| 5 | 0.03 | 1.7320 | **2.2514** | **4.761** |

Otros valores de referencia:

- Corpus: 315 783 caracteres; entrenamiento 252 626, validación 31 578, prueba 31 579.
- $|\mathcal{V}| = 27$; $H(\text{unigramas}) = 4.059163$ bits; $\log_2 27 = 4.754888$; redundancia 14.63 %.
- Gibbs: $H(\hat p) = 4.047143 \le H(\hat p,\hat q) = 4.053576$; $KL = 0.006433$.
- $\pi$ vs unigramas: diferencia máxima $3.71\times10^{-6}$; L1 $9.05\times10^{-6}$; 22 iteraciones.
- Bootstrap: 16 bloques (15×2000 + 1×1579), $\bar\Delta = 0.0926$ bits, IC 95 % [0.0553, 0.1259],
  14/16 bloques favorecen $n=5$. Sensibilidad con 15 bloques: 0.1031 [0.0711, 0.1326].
- Verificación interna: 127/127 comprobaciones correctas (`codigo/verificar_todo.py`).

## 4. Material disponible

- `notas_importantes/Preguntas_del_proyecto.md` (y `.txt` idéntico): las 11 preguntas oficiales
  respondidas, más banco propio. Fuente para la sección 7.
- `revision_resultados.md`: acta con todas las cifras verificadas y las limitaciones a declarar.
- `resumen_revision_2.md`: consolidado narrativo listo para adaptar a Resultados y Discusión.
- `decisiones_informe.md`: bitácora, secciones 1–16.
- `tablas/`: T1–T5, `T3_gibbs.csv`, `T4_bootstrap.csv`, `T4_deltas_bloques.csv`,
  `verificacion_resultados.csv`.
- `figuras/`: F1–F5 en `.png` y `.pdf`, más `bootstrap_delta` (sin numerar).
- `codigo/`: `preparar.py`, `pruebas.py`, `modelos.py`, `fase1.py`–`fase6.py`, `verificar_todo.py`.
- `resumen/resumen_proyecto_probabilidad.tex`: preámbulo y estilo LaTeX ya usados en el proyecto.

## 5. Numeración oficial

F1 = frecuencias; F2 = BPC de validación vs $\alpha$; F3 = BPC train/test vs $n$;
F4 = promedio acumulado (eje $x$ log); F5 = $\pi$ vs unigramas. Tablas T1–T5.

## 6. Limitaciones que el reporte debe declarar

1. El símbolo `#` se mantiene unificado (8.1 % de la masa): tildes, `ñ`, dígitos y puntuación.
2. $\alpha^*$ en $n=1$ y $n=2$ cae en el borde de la rejilla; se reporta como mínimo de la rejilla.
3. 16 bloques es poco para un bootstrap percentil: el intervalo es grueso (se acompaña sensibilidad).
4. Los dos últimos bloques favorecen $n=4$: el estilo del epílogo difiere del resto.
5. Las conclusiones valen para este corpus y esta partición, no para el español en general.

## 7. Convenciones de trabajo

- Responder en español, paso a paso, para alguien sin trasfondo previo.
- El usuario ejecuta el código en VS Code; dar comandos exactos y salida esperada.
- Commits en español, convencionales, indicando archivos, propósito y fecha/hora de subida.
- Subida con `git add` / `git commit` / `git push` por SSH (ya configurado, sin tokens).

## 8. Entregables de la Semana 4

- `reporte/reporte.tex` y `reporte/reporte.pdf` (10–14 páginas).
- `codigo/main.py` que ejecute el flujo completo.
- `README.md` reproducible.
- Todo commiteado y subido.

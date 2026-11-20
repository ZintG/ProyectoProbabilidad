# Proyecto de Probabilidad · Modelos de lenguaje de $n$-gramas

Predicción del siguiente carácter de *Niebla* (Nivola), de Miguel de Unamuno (1914),
con modelos de $n$-gramas de orden $n=1,\ldots,5$, suavizado aditivo, cadenas de Markov
y cuantificación de incertidumbre por bootstrap por bloques.

**Equipo 05** · Teoría de la Probabilidad (quinto semestre), Universidad de Carabobo.
Profesor: José Marcano. Fecha de entrega: 24 de noviembre de 2026.

---

## 1. Requisitos

| Herramienta | Versión verificada | Uso |
|---|---|---|
| Python | 3.13.5 | Ejecución de todas las fases |
| NumPy | 2.2.4 | Arreglos y remuestreo bootstrap |
| Matplotlib | 3.10.1 | Gráficas F1–F5 y bootstrap |
| Tectonic | cualquiera | Compilar el PDF del reporte (opcional) |

No se usan bibliotecas de modelos de lenguaje ni redes neuronales. Todo el código
de conteos, suavizado, métricas, simulación y bootstrap es propio del equipo.

---

## 2. Instalación

Desde una terminal, con SSH ya configurado:

```bash
git clone git@github.com:ZintG/ProyectoProbabilidad.git
cd ProyectoProbabilidad
python3 -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Comprobación rápida de versiones:

```bash
python3 -c "import sys, numpy, matplotlib; print(sys.version.split()[0], numpy.__version__, matplotlib.__version__)"
```

Salida esperada (en el entorno verificado):

```
3.13.5 2.2.4 3.10.1
```

---

## 3. Ejecución completa en un solo comando

Desde la raíz del repositorio:

```bash
python3 codigo/main.py
```

`codigo/main.py` encadena las nueve etapas en orden, imprime el tiempo de cada una
y verifica el límite de 10 minutos. Tiempo medido en el entorno de referencia:

```
TIEMPO TOTAL: 39.14 s (0.65 min)
FLUJO COMPLETADO CORRECTAMENTE.
```

Si ya existe `tablas/T3_evaluacion_prueba.csv`, el programa **omite `fase4.py`** e
imprime:

```
AVISO: tablas/T3_evaluacion_prueba.csv ya existe.
La prueba se evaluó una sola vez: se omite fase4.py y se
conservan T3, T3_gibbs.csv, F3 y F4 tal como están.
```

Esto es intencional: el bloque de prueba se evaluó una sola vez y sus cifras están
congeladas. `main.py` nunca usa `--forzar`.

Opciones:

```bash
python3 codigo/main.py --max-segundos 600   # límite por defecto
python3 codigo/main.py --sin-limite         # medir sin exigir el límite
```

---

## 4. Ejecución paso a paso

Si prefieres correr cada fase por separado, respeta este orden. Todos los comandos
se ejecutan desde la raíz del repositorio.

| # | Comando | Qué genera | Salida destacada |
|---:|---|---|---|
| 1 | `python3 codigo/preparar.py` | `datos/entrenamiento.txt`, `validacion.txt`, `prueba.txt`, `texto_normalizado.txt` | 315 783 caracteres, $\|\mathcal{V}\|=27$ |
| 2 | `python3 codigo/pruebas.py` | — (prueba de cordura) | BPC 0.6000 bits, PPL 1.516 |
| 3 | `python3 codigo/fase1.py` | `tablas/T1_particiones.csv`, `figuras/F1_frecuencias.*` | $H(\hat p)=4.059$ bits |
| 4 | `python3 codigo/fase2.py` | `tablas/T2_ceros_validacion.csv` | Ceros desde $n=3$ |
| 5 | `python3 codigo/fase3.py` | `tablas/F2_bpc_alpha.csv`, `figuras/F2_bpc_alpha.*` | $\alpha^*(5)=0.03$ |
| 6 | `python3 codigo/fase4.py` | `tablas/T3_evaluacion_prueba.csv`, `T3_gibbs.csv`, `figuras/F3_bpc_n.*`, `F4_promedio_acumulado.*` | BPC 2.251 bits, PPL 4.761 |
| 7 | `python3 codigo/fase5.py` | `tablas/T5_muestras.csv`, `figuras/F5_pi_unigramas.*` | $\pi$ vs unigramas: $3.71\times10^{-6}$ |
| 8 | `python3 codigo/fase6.py` | `tablas/T4_bootstrap.csv`, `T4_deltas_bloques.csv`, `figuras/bootstrap_delta.*` | $\bar\Delta=0.0926$, IC $[0.0553,0.1259]$ |
| 9 | `python3 codigo/verificar_todo.py` | `tablas/verificacion_resultados.csv` | 127 correctas, 0 fallidas |

Tiempos individuales medidos: 0.36 s, 0.08 s, 5.21 s, 3.27 s, 10.07 s, 6.76 s
(fase 5), 6.23 s y 7.17 s. Fase 4 se omitió porque T3 ya existía.

---

## 5. Evaluación única en prueba

El protocolo que garantiza la honestidad de la medición final:

1. Los $\alpha^*(n)$ se eligen **solo con validación** en `fase3.py` y se congelan.
2. `fase4.py` se niega a escribir `T3_evaluacion_prueba.csv` si ya existe:

   ```
   tablas/T3_evaluacion_prueba.csv ya existe. La prueba se evalúa una sola vez.
   Si de verdad necesitas repetirla, usa --forzar.
   ```

3. Modos auxiliares de `fase4.py`:

   ```bash
   python3 codigo/fase4.py --validar   # ensayo en validación; no escribe nada
   python3 codigo/fase4.py --solo-f4   # regenera solo F4; no reescribe T3 ni decide nada
   ```

4. **No usar `--forzar`** en una entrega: invalidaría el protocolo de evaluación única.

---

## 6. Verificación de cifras

```bash
python3 codigo/verificar_todo.py
```

El script reconstruye los cinco modelos desde `datos/`, recalcula cada métrica y la
compara contra las tablas guardadas; no copia valores de las tablas. Al terminar:

```
========================================================================
VERIFICACIONES: 127 correctas, 0 fallidas
Detalle: /home/roman/Documentos/ProyectoProbabilidad/tablas/verificacion_resultados.csv
========================================================================
```

---

## 7. Compilar el reporte

El fuente está en `reporte/reporte.tex` y las figuras vectoriales se leen desde
`../figuras/`. Desde la carpeta `reporte/`:

```bash
cd reporte
tectonic -X compile reporte.tex
```

Con TeX Live también funciona:

```bash
pdflatex reporte.tex && pdflatex reporte.tex
```

Resultado: `reporte/reporte.pdf`, 16 páginas en total: 1 de portada, 13 de cuerpo
numerado y 3 de anexos. El cuerpo (portada incluida) cumple el rango exigido
de 10–14 páginas.

---

## 8. Estructura del repositorio

```
.
├── README.md                   este archivo
├── requirements.txt            dependencias fijadas
├── proyecto_S01_probabilidad.pdf   enunciado oficial
├── codigo/
│   ├── main.py                 orquestador del flujo completo
│   ├── preparar.py             limpieza, normalización y partición
│   ├── pruebas.py              prueba de cordura (abracadabra)
│   ├── modelos.py              ModeloNgramas y utilidades
│   ├── fase1.py ... fase6.py   seis fases experimentales
│   └── verificar_todo.py       127 comprobaciones numéricas
├── datos/                      corpus normalizado y ficha de la fuente
├── libro/                      texto de Project Gutenberg
├── tablas/                     T1–T5 y verificaciones (CSV)
├── figuras/                    F1–F5 y bootstrap (PNG y PDF vectorial)
├── reporte/                    reporte.tex y reporte.pdf
├── notas_importantes/          traspaso, preguntas y bitácoras
├── resumen/                   plantilla LaTeX previa
└── S01/                        material del curso
```

---

## 9. Cifras congeladas

| $n$ | $\alpha^*$ | BPC entreno | BPC prueba | PPL prueba |
|---:|---:|---:|---:|---:|
| 1 | 1.0 | 4.059 | 4.054 | 16.61 |
| 2 | 0.001 | 3.235 | 3.212 | 9.268 |
| 3 | 0.1 | 2.687 | 2.722 | 6.599 |
| 4 | 0.03 | 2.154 | 2.346 | 5.085 |
| 5 | 0.03 | 1.732 | **2.251** | **4.761** |

Bootstrap: 16 bloques (15 de 2 000 + 1 de 1 579), $\bar\Delta=0.0926$ bits,
IC 95 % $[0.0553,\,0.1259]$, 14 de 16 bloques favorecen $n=5$.
Semillas: 2026 para la simulación y el bootstrap. BPC y PPL se reportan con
4 cifras significativas; las ecuaciones de verificación conservan mayor precisión.

---

## 10. Solución de problemas

- **`ModuleNotFoundError: No module named 'numpy'`**: activa el entorno virtual
  (`source .venv/bin/activate`) e instala `requirements.txt`.
- **`fase4.py` se niega a correr**: es correcto; T3 ya existe. Usa `main.py`, que
  omite esa etapa, o consulta los modos `--validar` y `--solo-f4`.
- **Las gráficas no aparecen en el PDF**: verifica que `reporte/reporte.tex` tenga
  `\graphicspath{{../figuras/}}` y compila desde `reporte/`.
- **Cifras distintas tras una repetición**: ejecuta `verificar_todo.py`; si hay
  fallos, no reemplaces las tablas congeladas sin revisar `decisiones_informe.md`.

---

## 11. Fuente del corpus

*Niebla (Nivola)*, Miguel de Unamuno (1914), Project Gutenberg eBook
[#49836](https://www.gutenberg.org/ebooks/49836), descargado el 12 de noviembre
de 2026. Dominio público según Project Gutenberg. La ficha completa está en
`datos/FUENTE.md`.

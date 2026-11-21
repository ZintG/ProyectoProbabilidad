# Proyecto de Probabilidad · Modelos de lenguaje de $n$-gramas

Predicción del siguiente carácter de *Niebla* (Nivola), de Miguel de Unamuno (1914),
con modelos de $n$-gramas de orden $n=1,\ldots,5$, suavizado aditivo, cadenas de Markov
y cuantificación de incertidumbre por bootstrap por bloques.

**Equipo 05** · Teoría de la Probabilidad (quinto semestre), Universidad de Carabobo.
Profesor: Dr. José G. Marcano. Fecha de entrega: 24 de noviembre de 2026.

### Integrantes:
* **Simón Tovar** — C.I. 31.678.578
* **Samuel Primera** — C.I. 21.129.684
* **Román Valero** — C.I. 33.638.501
* **Rolando Suárez** — C.I. 30.445.947

---

## 1. Requisitos

| Herramienta | Versión verificada | Uso |
|---|---|---|
| Python | 3.12 / 3.13 | Ejecución de todas las fases |
| NumPy | 2.2.4 | Arreglos y remuestreo bootstrap |
| Matplotlib | 3.10.1 | Gráficas F1–F5 y bootstrap |

No se usan bibliotecas externas de procesamiento de lenguaje natural ni redes neuronales.
Todo el código de conteos, suavizado, métricas, simulación y remuestreo bootstrap fue
desarrollado íntegramente por el equipo.

---

## 2. Instalación y configuración

Desde una terminal en la raíz de la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

---

## 3. Ejecución del proyecto

### Opción A: Experimentos de las Fases 1 a 6 (según §5.3 del enunciado)
Ejecuta las fases experimentales 1 a 6 y actualiza las tablas y figuras en `resultados/`:

```bash
python3 codigo/experimentos.py
```

### Opción B: Flujo completo orquestado
Ejecuta de principio a fin todo el flujo (preparación, pruebas de cordura, fases 1 a 6
y verificación numérica):

```bash
python3 codigo/main.py
```

*Tiempo total medido:* ~39.14 segundos (ampliamente inferior al límite de 10 minutos).

> **Aviso de protocolo honesto:** Si ya existe `resultados/T3_evaluacion_prueba.csv`,
> la fase 4 se omite automáticamente para preservar el resultado congelado de la
> evaluación única en prueba (evitando fuga de información o sobreajuste).

### Opción C: Comprobaciones y verificación rápida
* **Prueba de cordura obligatoria (`abracadabra`):**
  ```bash
  python3 codigo/pruebas.py
  ```
  Comprueba en < 0.1 s los conteos, entropía (2.0404 bits), MLE (0.5), Laplace (0.3333),
  BPC (0.6000) y perplejidad (1.5157). Pasa 6/6 comprobaciones.

* **Auditoría interna exhaustiva (127 cifras):**
  ```bash
  python3 codigo/verificar_todo.py
  ```
  Recalcula todas las métricas del proyecto y verifica contra las tablas guardadas.
  Pasa 127/127 comprobaciones con 0 fallos.

---

## 4. Ejecución paso a paso

Si se prefiere ejecutar cada fase individualmente, respete el siguiente orden secuencial:

| # | Comando | Qué genera | Salida destacada |
|---:|---|---|---|
| 1 | `python3 codigo/preparar.py` | `datos/entrenamiento.txt`, `validacion.txt`, `prueba.txt`, `texto_normalizado.txt` | 315 783 caracteres, $\|\mathcal{V}\|=27$ |
| 2 | `python3 codigo/pruebas.py` | Salida en consola (prueba de cordura) | BPC 0.6000 bits, PPL 1.516 |
| 3 | `python3 codigo/fase1.py` | `resultados/T1_particiones.csv`, `resultados/F1_frecuencias.*` | $H(\hat p)=4.059$ bits |
| 4 | `python3 codigo/fase2.py` | `resultados/T2_ceros_validacion.csv` | Ceros desde $n=3$ |
| 5 | `python3 codigo/fase3.py` | `resultados/F2_bpc_alpha.csv`, `resultados/F2_bpc_alpha.*` | $\alpha^*(5)=0.03$ |
| 6 | `python3 codigo/fase4.py` | `resultados/T3_evaluacion_prueba.csv`, `T3_gibbs.csv`, `resultados/F3_bpc_n.*`, `F4_promedio_acumulado.*` | BPC 2.251 bits, PPL 4.761 |
| 7 | `python3 codigo/fase5.py` | `resultados/T5_muestras.csv`, `resultados/F5_pi_unigramas.*` | $\pi$ vs unigramas: $3.71\times10^{-6}$ |
| 8 | `python3 codigo/fase6.py` | `resultados/T4_bootstrap.csv`, `T4_deltas_bloques.csv`, `resultados/bootstrap_delta.*` | $\bar\Delta=0.0926$, IC $[0.0553,0.1259]$ |
| 9 | `python3 codigo/verificar_todo.py` | `resultados/verificacion_resultados.csv` | 127 correctas, 0 fallidas |

---

## 5. Estructura de la entrega (Sección 5.3)

La carpeta de entrega sigue con total exactitud la jerarquía estipulada en la sección 5.3:

```
P1_Equipo05_Tovar_Primera_Valero_Suarez/
├── reporte.pdf             # Reporte técnico final (16 páginas)
├── README.md               # Guía de reproducción y ejecución
├── requirements.txt        # Dependencias fijadas (numpy, matplotlib)
├── datos/
│   ├── FUENTE.md           # Ficha bibliográfica de la obra (Project Gutenberg #49836)
│   ├── entrenamiento.txt   # Partición contigua de entrenamiento (80 %, 252 626 caracteres)
│   ├── validacion.txt      # Partición contigua de validación (10 %, 31 578 caracteres)
│   ├── prueba.txt          # Partición contigua de prueba (10 %, 31 579 caracteres)
│   └── texto_normalizado.txt
├── codigo/
│   ├── preparar.py         # Lectura, normalización y partición 80/10/10
│   ├── modelos.py          # Clase ModeloNgramas, MLE, conteos y suavizado
│   ├── experimentos.py     # Ejecución de fases 1 a 6; escribe en resultados/
│   ├── pruebas.py          # Prueba de cordura obligatoria (abracadabra)
│   ├── fase1.py ... fase6.py # Módulos individuales de las seis fases
│   ├── main.py             # Orquestador del flujo general
│   └── verificar_todo.py   # Auditoría de verificación interna de 127 cifras
└── resultados/             # Tablas (.csv) y figuras vectoriales (.png y .pdf)
    ├── T1_particiones.csv
    ├── T2_ceros_validacion.csv
    ├── F2_bpc_alpha.csv
    ├── T3_evaluacion_prueba.csv
    ├── T3_gibbs.csv
    ├── T4_bootstrap.csv
    ├── T4_deltas_bloques.csv
    ├── T5_muestras.csv
    ├── verificacion_resultados.csv
    ├── F1_frecuencias.png / F1_frecuencias.pdf
    ├── F2_bpc_alpha.png / F2_bpc_alpha.pdf
    ├── F3_bpc_n.png / F3_bpc_n.pdf
    ├── F4_promedio_acumulado.png / F4_promedio_acumulado.pdf
    ├── F5_pi_unigramas.png / F5_pi_unigramas.pdf
    └── bootstrap_delta.png / bootstrap_delta.pdf
```

---

## 6. Cifras oficiales congeladas

| $n$ | $\alpha^*$ | BPC entrenamiento | BPC prueba | PPL prueba |
|---:|---:|---:|---:|---:|
| 1 | 1.000 | 4.059 | 4.054 | 16.61 |
| 2 | 0.001 | 3.235 | 3.212 | 9.268 |
| 3 | 0.100 | 2.687 | 2.722 | 6.599 |
| 4 | 0.030 | 2.154 | 2.346 | 5.085 |
| 5 | 0.030 | 1.732 | **2.251** | **4.761** |

* **Mejor orden:** $n=5$ con BPC de prueba de **2.251 bits** y perplejidad **4.761**.
* **Incertidumbre bootstrap por bloques:** 16 bloques (15 de 2 000 y 1 de 1 579 caracteres),
  $\bar\Delta = 0.0926$ bits, IC 95 % $[0.0553,\,0.1259]$ bits a favor de $n=5$ frente a $n=4$
  (14 de 16 bloques favorecen a $n=5$).
* **Semilla determinista:** 2026 para simulación y bootstrap.

---

## 7. Fuente del corpus

*Niebla (Nivola)*, Miguel de Unamuno (1914), Project Gutenberg eBook
[#49836](https://www.gutenberg.org/ebooks/49836), descargado el 12 de noviembre
de 2026. Dominio público. Ficha bibliográfica completa en `datos/FUENTE.md`.

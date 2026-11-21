#!/usr/bin/env python3
"""codigo/fase5.py
Fase 5: matriz de transición del bigrama, distribución estacionaria y muestras.
"""

import csv
import random
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_RESULTADOS = BASE_DIR / "resultados"
DIR_TABLAS = BASE_DIR / "tablas" if (BASE_DIR / "tablas").exists() else DIR_RESULTADOS
DIR_FIGURAS = BASE_DIR / "figuras" if (BASE_DIR / "figuras").exists() else DIR_RESULTADOS

ALPHA_OPTIMO = {1: 1.0, 2: 0.001, 3: 0.1, 4: 0.03, 5: 0.03}

SEMILLA = 2026
CONTEXTO_INICIAL = "habia "
LONGITUD = 300


def matriz_transicion(modelo, alpha):
    """P[i][j] = q_alpha(V[j] | V[i]) para el bigrama suavizado."""
    V = modelo.V
    return [
        [modelo.prob_suavizada(V[j], V[i], alpha) for j in range(modelo.K)]
        for i in range(modelo.K)
    ]


def distribucion_estacionaria(P, tolerancia=1e-10, max_iter=10000):
    """Iteración de potencias pi_{t+1} = pi_t P."""
    K = len(P)
    pi = [1.0 / K] * K

    for it in range(1, max_iter + 1):
        nuevo = [
            sum(pi[i] * P[i][j] for i in range(K))
            for j in range(K)
        ]
        diferencia = sum(abs(nuevo[j] - pi[j]) for j in range(K))
        pi = nuevo
        if diferencia < tolerancia:
            return pi, it, diferencia

    raise RuntimeError("La iteración de potencias no convergió")


def generar_texto(modelo, alpha, contexto, longitud, semilla):
    """Muestrea caracteres según q_alpha(y | h)."""
    rng = random.Random(semilla)
    V = modelo.V
    n = modelo.n

    texto = contexto
    for _ in range(longitud):
        h = texto[-(n - 1):] if n > 1 else ""
        pesos = [modelo.prob_suavizada(y, h, alpha) for y in V]
        texto += rng.choices(V, weights=pesos, k=1)[0]
    return texto


def main():
    entrenamiento = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")

    # --- Matriz del bigrama suavizado ---
    modelo2 = ModeloNgramas(entrenamiento, 2)
    alpha2 = ALPHA_OPTIMO[2]
    P = matriz_transicion(modelo2, alpha2)

    desv_max = max(abs(sum(fila) - 1.0) for fila in P)
    minimo = min(min(fila) for fila in P)
    print("MATRIZ DE TRANSICIÓN DEL BIGRAMA")
    print(f"  tamaño            : {len(P)} x {len(P[0])}")
    print(f"  alpha             : {alpha2}")
    print(f"  desv. máx. filas  : {desv_max:.2e}")
    print(f"  entrada mínima    : {minimo:.3e}")
    assert desv_max <= 1e-12, "Las filas no suman 1"
    assert minimo > 0.0, "Hay entradas no positivas"
    print("  Correcto: matriz estocástica y positiva.\n")

    # --- Distribución estacionaria ---
    pi, iteraciones, diferencia = distribucion_estacionaria(P)
    suma_pi = sum(pi)
    pi = [v / suma_pi for v in pi]

    print("DISTRIBUCIÓN ESTACIONARIA")
    print(f"  iteraciones       : {iteraciones}")
    print(f"  última diferencia : {diferencia:.2e}")
    print(f"  suma(pi)          : {sum(pi):.12f}\n")

    # --- Comparación con frecuencias de unigramas ---
    cuenta = Counter(entrenamiento)
    N = len(entrenamiento)
    p_unigramas = [cuenta[y] / N for y in modelo2.V]

    dif_max = max(abs(a - b) for a, b in zip(pi, p_unigramas))
    l1 = sum(abs(a - b) for a, b in zip(pi, p_unigramas))

    print("COMPARACIÓN pi vs FRECUENCIAS DE UNIGRAMAS")
    print(f"  diferencia máxima : {dif_max:.2e}")
    print(f"  distancia L1      : {l1:.2e}")
    print(f"{'símbolo':>8} | {'pi':>10} | {'p unigramas':>12}")
    print("-" * 36)
    for y, a, b in sorted(zip(modelo2.V, pi, p_unigramas),
                          key=lambda t: -t[2]):
        print(f"{y!r:>8} | {a:>10.6f} | {b:>12.6f}")

    # --- Muestras de 300 caracteres ---
    print("\nMUESTRAS DE 300 CARACTERES")
    print(f"  semilla           : {SEMILLA}")
    print(f"  contexto inicial  : {CONTEXTO_INICIAL!r}\n")

    muestras = []
    for n in (2, 3, 5):
        modelo = ModeloNgramas(entrenamiento, n)
        texto = generar_texto(
            modelo, ALPHA_OPTIMO[n], CONTEXTO_INICIAL, LONGITUD, SEMILLA
        )
        muestras.append({
            "modelo": f"n={n}",
            "semilla": SEMILLA,
            "contexto": CONTEXTO_INICIAL,
            "texto": texto,
        })
        print(f"n={n}:")
        print(texto)
        print()

    DIR_TABLAS.mkdir(exist_ok=True)
    ruta_muestras = DIR_TABLAS / "T5_muestras.csv"
    with open(ruta_muestras, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(muestras[0].keys()))
        writer.writeheader()
        writer.writerows(muestras)

    # --- Gráfica F5 ---
    DIR_FIGURAS.mkdir(exist_ok=True)
    orden = sorted(range(len(modelo2.V)), key=lambda i: -p_unigramas[i])
    simbolos = [modelo2.V[i] for i in orden]
    pi_ord = [pi[i] for i in orden]
    p_ord = [p_unigramas[i] for i in orden]

    x = range(len(simbolos))
    ancho = 0.4

    plt.figure(figsize=(12, 5))
    plt.bar([i - ancho / 2 for i in x], p_ord, width=ancho,
            label="Frecuencias de unigramas")
    plt.bar([i + ancho / 2 for i in x], pi_ord, width=ancho,
            label=r"Distribución estacionaria $\pi$")
    plt.xticks(list(x), [repr(s)[1:-1] for s in simbolos])
    plt.xlabel("Símbolo")
    plt.ylabel("Probabilidad")
    plt.title(r"Gráfica F5: $\pi$ frente a las frecuencias de unigramas")
    plt.legend()
    plt.tight_layout()
    plt.savefig(DIR_FIGURAS / "F5_pi_unigramas.png", dpi=300)
    plt.savefig(DIR_FIGURAS / "F5_pi_unigramas.pdf")
    plt.close()

    print(f"Muestras guardadas en: {ruta_muestras}")
    print(f"Gráfica F5 en: {DIR_FIGURAS / 'F5_pi_unigramas.png'}")


if __name__ == "__main__":
    main()
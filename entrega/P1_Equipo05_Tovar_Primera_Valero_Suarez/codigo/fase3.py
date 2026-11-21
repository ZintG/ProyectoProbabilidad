#!/usr/bin/env python3
"""codigo/fase3.py
Fase 3: calibración de alpha con validación y Gráfica F2.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_RESULTADOS = BASE_DIR / "resultados"
DIR_TABLAS = BASE_DIR / "tablas" if (BASE_DIR / "tablas").exists() else DIR_RESULTADOS
DIR_FIGURAS = BASE_DIR / "figuras" if (BASE_DIR / "figuras").exists() else DIR_RESULTADOS

ALPHAS = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


def bpc_validacion(modelo, validacion, entrenamiento, alpha):
    """BPC de validación con suavizado, usando contexto heredado."""
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + validacion

    bits = 0.0
    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]
        y = ext[i]
        bits -= modelo.log_prob_suavizada(y, h, alpha)

    return bits / len(validacion)


def main():
    entrenamiento = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")
    validacion = (DIR_DATOS / "validacion.txt").read_text(encoding="utf-8")

    filas = []
    mejores = {}

    for n in range(1, 6):
        modelo = ModeloNgramas(entrenamiento, n)

        for alpha in ALPHAS:
            bpc = bpc_validacion(modelo, validacion, entrenamiento, alpha)
            filas.append({"n": n, "alpha": alpha, "bpc_validacion": bpc})

        filas_n = [f for f in filas if f["n"] == n]
        mejor = min(filas_n, key=lambda f: f["bpc_validacion"])
        mejores[n] = mejor

        print(
            f"n={n}: alpha* = {mejor['alpha']:<6} "
            f"-> BPC validación = {mejor['bpc_validacion']:.6f}"
        )

    print("\nTABLA BPC DE VALIDACIÓN vs ALPHA")
    print(f"{'n':>2} | " + " | ".join(f"{a:>8}" for a in ALPHAS))
    print("-" * (5 + 11 * len(ALPHAS)))

    for n in range(1, 6):
        valores = [f["bpc_validacion"] for f in filas if f["n"] == n]
        print(f"{n:>2} | " + " | ".join(f"{v:>8.4f}" for v in valores))

    DIR_TABLAS.mkdir(exist_ok=True)
    ruta_csv = DIR_TABLAS / "F2_bpc_alpha.csv"

    with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["n", "alpha", "bpc_validacion"]
        )
        writer.writeheader()
        writer.writerows(filas)

    print(f"\nResultados guardados en: {ruta_csv}")

    # Gráfica F2
    DIR_FIGURAS.mkdir(exist_ok=True)

    plt.figure(figsize=(8, 5))

    for n in range(1, 6):
        puntos = [f for f in filas if f["n"] == n]
        alphas_n = [p["alpha"] for p in puntos]
        bpcs_n = [p["bpc_validacion"] for p in puntos]

        plt.plot(
            alphas_n,
            bpcs_n,
            marker="o",
            linewidth=1.8,
            label=f"n = {n}",
        )

        mejor = mejores[n]
        plt.scatter(
            mejor["alpha"],
            mejor["bpc_validacion"],
            s=90,
            facecolors="none",
            edgecolors="black",
            linewidths=1.5,
            zorder=5,
        )

    plt.xscale("log")
    plt.xlabel(r"$\alpha$ (escala logarítmica)")
    plt.ylabel("BPC de validación (bits por carácter)")
    plt.title(r"Gráfica F2: BPC de validación vs $\alpha$")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(title=r"Orden $n$")
    plt.tight_layout()

    ruta_png = DIR_FIGURAS / "F2_bpc_alpha.png"
    ruta_pdf = DIR_FIGURAS / "F2_bpc_alpha.pdf"

    plt.savefig(ruta_png, dpi=300)
    plt.savefig(ruta_pdf)
    plt.close()

    print(f"Gráfica F2 guardada en: {ruta_png}")
    print(f"Gráfica F2 (vectorial): {ruta_pdf}")


if __name__ == "__main__":
    main()
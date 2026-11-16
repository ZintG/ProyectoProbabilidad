#!/usr/bin/env python3
"""codigo/fase2.py
Fase 2: evaluar la MLE sobre validación y construir la Tabla T2.
"""

import csv
import math
from pathlib import Path

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_TABLAS = BASE_DIR / "tablas"


def evaluar_ceros(modelo, validacion, entrenamiento):
    """Cuenta caracteres de validación con probabilidad MLE cero."""
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + validacion

    ceros = 0
    ceros_contexto = 0
    ceros_par = 0

    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]      # n=1 -> ""
        y = ext[i]
        ch = modelo.conteo_contexto(h)
        cy = modelo.conteo_par(h, y)

        if ch == 0:
            ceros += 1
            ceros_contexto += 1
        elif cy == 0:
            ceros += 1
            ceros_par += 1

    return ceros, ceros_contexto, ceros_par


def calcular_bpc_mle(modelo, validacion, entrenamiento):
    """BPC de la MLE sobre validación; inf si aparece un cero."""
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + validacion

    bits = 0.0
    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]
        y = ext[i]
        p = modelo.prob_mle(y, h)
        if p == 0.0:
            return float("inf")
        bits -= math.log2(p)

    return bits / len(validacion)


def main():
    entrenamiento = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")
    validacion = (DIR_DATOS / "validacion.txt").read_text(encoding="utf-8")

    filas = []
    for n in range(1, 6):
        modelo = ModeloNgramas(entrenamiento, n)
        ceros, ceros_ctx, ceros_par = evaluar_ceros(
            modelo, validacion, entrenamiento
        )
        bpc = calcular_bpc_mle(modelo, validacion, entrenamiento)
        porcentaje = 100.0 * ceros / len(validacion)

        filas.append({
            "n": n,
            "contextos_posibles": modelo.K ** (n - 1),
            "contextos_observados": len(modelo.c_h),
            "ngramas_posibles": modelo.K ** n,
            "ngramas_observados": sum(len(c) for c in modelo.c_hy.values()),
            "caracteres_evaluados": len(validacion),
            "ceros": ceros,
            "porcentaje_ceros": porcentaje,
            "ceros_contexto": ceros_ctx,
            "ceros_par": ceros_par,
            "bpc_mle": bpc,
        })

    print("TABLA T2: CEROS DE LA MLE EN VALIDACIÓN")
    print(
        f"{'n':>2} | {'ctx obs':>8} | {'n-gramas obs':>12} | "
        f"{'ceros':>6} | {'% ceros':>8} | {'c(h)=0':>7} | {'c(h,y)=0':>9}"
    )
    print("-" * 80)

    for f in filas:
        print(
            f"{f['n']:>2} | {f['contextos_observados']:>8} | "
            f"{f['ngramas_observados']:>12} | {f['ceros']:>6} | "
            f"{f['porcentaje_ceros']:>7.4f}% | {f['ceros_contexto']:>7} | "
            f"{f['ceros_par']:>9}"
        )

    print("\nBPC MLE EN VALIDACIÓN")
    print(f"{'n':>2} | {'BPC MLE':>10}")
    print("-" * 18)
    for f in filas:
        print(f"{f['n']:>2} | {f['bpc_mle']:>10.4f}")

    DIR_TABLAS.mkdir(exist_ok=True)
    ruta_csv = DIR_TABLAS / "T2_ceros_validacion.csv"

    with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)

    print(f"\nTabla guardada en: {ruta_csv}")


if __name__ == "__main__":
    main()
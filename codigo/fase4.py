#!/usr/bin/env python3
"""codigo/fase4.py
Fase 4: evaluación única en prueba, Tabla T3, Gibbs y gráficas F3 y F4.
"""

import argparse
import csv
import math
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_TABLAS = BASE_DIR / "tablas"
DIR_FIGURAS = BASE_DIR / "figuras"

ALPHA_OPTIMO = {1: 1.0, 2: 0.001, 3: 0.1, 4: 0.03, 5: 0.03}


def bpc_entrenamiento(modelo, alpha):
    """BPC del entrenamiento a partir de los conteos acumulados."""
    bits = 0.0
    for h, continuaciones in modelo.c_hy.items():
        for y, c in continuaciones.items():
            bits -= c * modelo.log_prob_suavizada(y, h, alpha)
    return bits / (modelo.N - modelo.n + 1)


def costes_bloque(modelo, bloque, entrenamiento, alpha):
    """Lista de -log2 q para cada carácter del bloque, con contexto heredado."""
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + bloque

    costes = []
    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]
        y = ext[i]
        costes.append(-modelo.log_prob_suavizada(y, h, alpha))
    return costes


def gibbs_unigramas(modelo1, bloque, alpha):
    """H(p) <= H(p,q) para unigramas; devuelve H(p), H(p,q) y KL."""
    cuenta = Counter(bloque)
    N = len(bloque)
    p = {y: cuenta[y] / N for y in modelo1.V}

    h_p = -sum(v * math.log2(v) for v in p.values() if v > 0)
    h_pq = -sum(
        v * modelo1.log_prob_suavizada(y, "", alpha)
        for y, v in p.items()
        if v > 0
    )
    return h_p, h_pq, h_pq - h_p


def promedios_acumulados(costes):
    """S_k = (1/k) * suma_{t<=k} (-log2 q_t)."""
    acumulado = []
    total = 0.0
    for k, c in enumerate(costes, start=1):
        total += c
        acumulado.append(total / k)
    return acumulado


def graficar_f4(costes, bpc_final, n):
    """Gráfica F4: promedio acumulado con eje horizontal logarítmico."""
    acumulado = promedios_acumulados(costes)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(acumulado) + 1), acumulado,
             linewidth=1.4, label=f"$S_k$ (n = {n})")
    plt.axhline(bpc_final, linestyle="--",
                label=f"BPC final = {bpc_final:.4g}")
    plt.xscale("log")
    plt.xlabel(r"Caracteres evaluados $k$ (escala logarítmica)")
    plt.ylabel("Promedio acumulado (bits por carácter)")
    plt.title("Gráfica F4: convergencia del promedio acumulado")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(DIR_FIGURAS / "F4_promedio_acumulado.png", dpi=300)
    plt.savefig(DIR_FIGURAS / "F4_promedio_acumulado.pdf")
    plt.close()


def regenerar_f4(entrenamiento):
    """Regenera solo F4 reutilizando los alpha fijados en la Fase 3.

    No escribe T3 ni Gibbs: comprueba que el BPC coincide con el ya
    registrado y solo rehace la figura.
    """
    n = 5
    alpha = ALPHA_OPTIMO[n]

    ruta_t3 = DIR_TABLAS / "T3_evaluacion_prueba.csv"
    if not ruta_t3.exists():
        raise SystemExit(
            f"No existe {ruta_t3}. Ejecuta primero la evaluación oficial."
        )

    with open(ruta_t3, encoding="utf-8") as f:
        registrado = {
            int(fila["n"]): float(fila["bpc_prueba"])
            for fila in csv.DictReader(f)
        }

    bloque = (DIR_DATOS / "prueba.txt").read_text(encoding="utf-8")
    modelo = ModeloNgramas(entrenamiento, n)
    costes = costes_bloque(modelo, bloque, entrenamiento, alpha)
    bpc = sum(costes) / len(bloque)

    print(f"Regenerando F4 con n = {n}, alpha = {alpha}")
    print(f"  BPC recalculado : {bpc:.12f}")
    print(f"  BPC en T3       : {registrado[n]:.12f}")
    if abs(bpc - registrado[n]) > 1e-9:
        raise SystemExit(
            "El BPC recalculado no coincide con T3. No se toca la figura."
        )
    print("  Coincide: los parámetros no cambiaron.\n")

    DIR_FIGURAS.mkdir(exist_ok=True)
    graficar_f4(costes, bpc, n)
    print(f"Gráfica F4: {DIR_FIGURAS / 'F4_promedio_acumulado.png'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validar", action="store_true",
        help="ensayo sobre validación; no escribe archivos",
    )
    parser.add_argument(
        "--forzar", action="store_true",
        help="permite repetir la evaluación oficial de prueba",
    )
    parser.add_argument(
        "--solo-f4", action="store_true",
        help="regenera únicamente la gráfica F4 con los alpha ya fijados; "
             "no reescribe T3 ni vuelve a decidir nada",
    )
    args = parser.parse_args()

    entrenamiento = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")

    if args.solo_f4:
        regenerar_f4(entrenamiento)
        return

    if args.validar:
        bloque = (DIR_DATOS / "validacion.txt").read_text(encoding="utf-8")
        etiqueta = "validación"
        ruta_t3 = None
    else:
        ruta_t3 = DIR_TABLAS / "T3_evaluacion_prueba.csv"
        if ruta_t3.exists() and not args.forzar:
            raise SystemExit(
                f"{ruta_t3} ya existe. La prueba se evalúa una sola vez.\n"
                "Si de verdad necesitas repetirla, usa --forzar."
            )
        bloque = (DIR_DATOS / "prueba.txt").read_text(encoding="utf-8")
        etiqueta = "prueba"

    filas = []
    costes_por_n = {}
    modelos = {}

    for n in range(1, 6):
        alpha = ALPHA_OPTIMO[n]
        modelo = ModeloNgramas(entrenamiento, n)
        modelos[n] = modelo

        bpc_tr = bpc_entrenamiento(modelo, alpha)
        costes = costes_bloque(modelo, bloque, entrenamiento, alpha)
        costes_por_n[n] = costes
        bpc_pr = sum(costes) / len(bloque)

        filas.append({
            "n": n,
            "alpha": alpha,
            "bpc_entrenamiento": bpc_tr,
            "bpc_prueba": bpc_pr,
            "ppl_prueba": 2.0 ** bpc_pr,
        })
        print(
            f"n={n}: alpha={alpha:<6} BPC entreno={bpc_tr:.4f} "
            f"BPC {etiqueta}={bpc_pr:.4f} PPL={2.0 ** bpc_pr:.3f}"
        )

    print(f"\nEVALUACIÓN EN {etiqueta.upper()} (N = {len(bloque)})")
    print(f"{'n':>2} | {'alpha':>6} | {'BPC entreno':>12} | "
          f"{'BPC ' + etiqueta:>14} | {'PPL':>9}")
    print("-" * 58)
    for f in filas:
        print(
            f"{f['n']:>2} | {f['alpha']:>6} | "
            f"{f['bpc_entrenamiento']:>12.4f} | "
            f"{f['bpc_prueba']:>14.4f} | {f['ppl_prueba']:>9.3f}"
        )

    mejor = min(filas, key=lambda f: f["bpc_prueba"])
    print(f"\nMejor n en {etiqueta}: {mejor['n']} "
          f"(BPC {mejor['bpc_prueba']:.4f})")

    # Desigualdad de Gibbs con unigramas
    h_p, h_pq, kl = gibbs_unigramas(modelos[1], bloque, ALPHA_OPTIMO[1])
    print("\nDESIGUALDAD DE GIBBS (unigramas)")
    print(f"  H(p)      = {h_p:.6f} bits")
    print(f"  H(p, q)   = {h_pq:.6f} bits")
    print(f"  KL(p||q)  = {kl:.6f} bits")
    assert h_p <= h_pq + 1e-12, "Gibbs no se cumple"
    print("  Correcto: H(p) <= H(p, q).")

    if args.validar:
        print("\nModo ensayo: no se escribió ningún archivo.")
        return

    # --- a partir de aquí solo en la evaluación oficial ---
    DIR_TABLAS.mkdir(exist_ok=True)
    with open(ruta_t3, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)

    with open(DIR_TABLAS / "T3_gibbs.csv", "w", encoding="utf-8",
              newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["h_p", "h_pq", "kl"])
        writer.writerow([h_p, h_pq, kl])

    # Gráfica F3: BPC de entrenamiento y de prueba contra n
    ns = [f["n"] for f in filas]
    bpc_tr = [f["bpc_entrenamiento"] for f in filas]
    bpc_pr = [f["bpc_prueba"] for f in filas]

    plt.figure(figsize=(8, 5))
    plt.plot(ns, bpc_tr, marker="o", linewidth=1.8,
             label="Entrenamiento")
    plt.plot(ns, bpc_pr, marker="s", linewidth=1.8,
             label="Prueba")
    plt.xticks(ns)
    plt.xlabel(r"Orden $n$")
    plt.ylabel("BPC (bits por carácter)")
    plt.title("Gráfica F3: BPC de entrenamiento y de prueba vs $n$")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(DIR_FIGURAS / "F3_bpc_n.png", dpi=300)
    plt.savefig(DIR_FIGURAS / "F3_bpc_n.pdf")
    plt.close()

    # Gráfica F4: promedio acumulado de la sorpresa (LLN)
    n_mejor = mejor["n"]
    graficar_f4(costes_por_n[n_mejor], mejor["bpc_prueba"], n_mejor)

    print(f"\nTabla T3: {ruta_t3}")
    print(f"Gibbs: {DIR_TABLAS / 'T3_gibbs.csv'}")
    print(f"Gráfica F3: {DIR_FIGURAS / 'F3_bpc_n.png'}")
    print(f"Gráfica F4: {DIR_FIGURAS / 'F4_promedio_acumulado.png'}")


if __name__ == "__main__":
    main()
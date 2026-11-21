#!/usr/bin/env python3
"""codigo/fase6.py
Fase 6: incertidumbre de la comparación n=5 vs n=4 por bootstrap de bloques.
Genera la Tabla T4 y una figura complementaria (no numerada).
"""

import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_RESULTADOS = BASE_DIR / "resultados"
DIR_TABLAS = BASE_DIR / "tablas" if (BASE_DIR / "tablas").exists() else DIR_RESULTADOS
DIR_FIGURAS = BASE_DIR / "figuras" if (BASE_DIR / "figuras").exists() else DIR_RESULTADOS

ALPHA_OPTIMO = {1: 1.0, 2: 0.001, 3: 0.1, 4: 0.03, 5: 0.03}

N_MEJOR = 5
N_ALTERNO = N_MEJOR - 1
TAM_BLOQUE = 2000
REMUESTRAS = 10000
SEMILLA = 2026
NIVEL = 0.95


def costes_bloque(modelo, bloque, entrenamiento, alpha):
    """-log2 q(y|h) para cada carácter del bloque, con contexto heredado."""
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + bloque

    costes = []
    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]
        costes.append(-modelo.log_prob_suavizada(ext[i], h, alpha))
    return costes


def partir_bloques(costes, tam):
    """Divide los costes en bloques contiguos; el último puede ser menor."""
    return [costes[i:i + tam] for i in range(0, len(costes), tam)]


def bootstrap_media(valores, remuestras, semilla, nivel):
    """Intervalo percentil para la media (Def. 1.1.44)."""
    rng = random.Random(semilla)
    k = len(valores)
    medias = []
    for _ in range(remuestras):
        muestra = [valores[rng.randrange(k)] for _ in range(k)]
        medias.append(sum(muestra) / k)
    medias.sort()

    alfa = (1.0 - nivel) / 2.0
    i_inf = int(round(alfa * (remuestras - 1)))
    i_sup = int(round((1.0 - alfa) * (remuestras - 1)))
    media = sum(valores) / k
    sesgo = sum(m - media for m in medias) / remuestras
    var = sum((m - media) ** 2 for m in medias) / (remuestras - 1)
    return {
        "media": media,
        "ic_inferior": medias[i_inf],
        "ic_superior": medias[i_sup],
        "error_estandar": var ** 0.5,
        "sesgo": sesgo,
        "medias": medias,
    }


def main():
    entrenamiento = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")
    prueba = (DIR_DATOS / "prueba.txt").read_text(encoding="utf-8")

    # --- Costes por carácter de los dos modelos ---
    costes = {}
    for n in (N_ALTERNO, N_MEJOR):
        modelo = ModeloNgramas(entrenamiento, n)
        costes[n] = costes_bloque(modelo, prueba, entrenamiento, ALPHA_OPTIMO[n])
        print(f"n={n}: alpha={ALPHA_OPTIMO[n]} lista de {len(costes[n])} costes")

    # --- Bloques contiguos y Delta por bloque ---
    bloques_alt = partir_bloques(costes[N_ALTERNO], TAM_BLOQUE)
    bloques_mej = partir_bloques(costes[N_MEJOR], TAM_BLOQUE)
    n_bloques = len(bloques_alt)

    filas_bloques = []
    deltas = []
    for j, (b_alt, b_mej) in enumerate(zip(bloques_alt, bloques_mej), start=1):
        bpc_alt = sum(b_alt) / len(b_alt)
        bpc_mej = sum(b_mej) / len(b_mej)
        delta = bpc_alt - bpc_mej          # > 0  =>  n=5 predice mejor
        deltas.append(delta)
        filas_bloques.append({
            "bloque": j,
            "inicio": (j - 1) * TAM_BLOQUE,
            "fin": (j - 1) * TAM_BLOQUE + len(b_alt) - 1,
            "longitud": len(b_alt),
            "bpc_n4": bpc_alt,
            "bpc_n5": bpc_mej,
            "delta": delta,
        })

    caracteres_usados = sum(f["longitud"] for f in filas_bloques)
    bpc_global_alt = sum(sum(b) for b in bloques_alt) / caracteres_usados
    bpc_global_mej = sum(sum(b) for b in bloques_mej) / caracteres_usados

    print(f"\nBLOQUES CONTIGUOS DE {TAM_BLOQUE} CARACTERES")
    print(f"  bloques            : {n_bloques} "
          f"({n_bloques - 1} de {TAM_BLOQUE} + 1 de {filas_bloques[-1]['longitud']})")
    print(f"  caracteres usados  : {caracteres_usados} de {len(prueba)}")
    print(f"  BPC n={N_ALTERNO}         : {bpc_global_alt:.4f}")
    print(f"  BPC n={N_MEJOR}         : {bpc_global_mej:.4f}")
    print(f"  Delta global       : {bpc_global_alt - bpc_global_mej:.4f} bits")
    print(f"\n{'bloque':>6} | {'long':>5} | {'BPC n=4':>8} | {'BPC n=5':>8} | "
          f"{'Delta':>8}")
    print("-" * 50)
    for f in filas_bloques:
        print(f"{f['bloque']:>6} | {f['longitud']:>5} | {f['bpc_n4']:>8.4f} | "
              f"{f['bpc_n5']:>8.4f} | {f['delta']:>8.4f}")

    # --- Bootstrap ---
    res = bootstrap_media(deltas, REMUESTRAS, SEMILLA, NIVEL)
    excluye_cero = res["ic_inferior"] > 0 or res["ic_superior"] < 0

    print(f"\nBOOTSTRAP PERCENTIL {int(NIVEL * 100)} % "
          f"({REMUESTRAS} remuestras, semilla {SEMILLA})")
    print(f"  media de Delta_j   : {res['media']:.4f} bits")
    print(f"  IC {int(NIVEL * 100)} %          : "
          f"[{res['ic_inferior']:.4f}, {res['ic_superior']:.4f}]")
    print(f"  error estandar     : {res['error_estandar']:.4f}")
    print(f"  sesgo bootstrap    : {res['sesgo']:+.2e}")
    print(f"  el intervalo {'SI' if excluye_cero else 'NO'} excluye el cero")
    print(f"  bloques con Delta>0: "
          f"{sum(1 for d in deltas if d > 0)} de {n_bloques}")

    # --- Sensibilidad: solo bloques completos ---
    deltas_completos = [f["delta"] for f in filas_bloques
                        if f["longitud"] == TAM_BLOQUE]
    res_comp = bootstrap_media(deltas_completos, REMUESTRAS, SEMILLA, NIVEL)
    print(f"\nSENSIBILIDAD (solo {len(deltas_completos)} bloques completos)")
    print(f"  media de Delta_j   : {res_comp['media']:.4f} bits")
    print(f"  IC {int(NIVEL * 100)} %          : "
          f"[{res_comp['ic_inferior']:.4f}, {res_comp['ic_superior']:.4f}]")

    # --- Tabla T4 ---
    DIR_TABLAS.mkdir(exist_ok=True)
    ruta_t4 = DIR_TABLAS / "T4_bootstrap.csv"
    with open(ruta_t4, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "n_mejor", "n_alterno", "delta_medio", "ic_inferior",
            "ic_superior", "nivel", "remuestras", "semilla",
            "n_bloques", "tam_bloque", "caracteres", "excluye_cero",
        ])
        w.writerow([
            N_MEJOR, N_ALTERNO, f"{res['media']:.6f}",
            f"{res['ic_inferior']:.6f}", f"{res['ic_superior']:.6f}",
            NIVEL, REMUESTRAS, SEMILLA, n_bloques, TAM_BLOQUE,
            caracteres_usados, "si" if excluye_cero else "no",
        ])

    with open(DIR_TABLAS / "T4_deltas_bloques.csv", "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas_bloques[0].keys()))
        w.writeheader()
        w.writerows(filas_bloques)

    # --- Figura complementaria (no numerada) ---
    DIR_FIGURAS.mkdir(exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.hist(res["medias"], bins=60, edgecolor="black", linewidth=0.3)
    plt.axvline(res["media"], linewidth=1.8, color="C0",
                label=f"Media = {res['media']:.4f}")
    plt.axvline(res["ic_inferior"], linestyle="--", linewidth=1.4, color="C1",
                label=f"IC {int(NIVEL * 100)} % = "
                      f"[{res['ic_inferior']:.4f}, {res['ic_superior']:.4f}]")
    plt.axvline(res["ic_superior"], linestyle="--", linewidth=1.4, color="C1")
    plt.axvline(0.0, color="red", linestyle=":", linewidth=1.6,
                label="Cero")
    plt.xlabel(r"Diferencia de BPC por bloque, $\Delta_j$ (bits)")
    plt.ylabel("Frecuencia")
    plt.title(f"Bootstrap de $\\Delta_j$: n={N_MEJOR} frente a n={N_ALTERNO}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(DIR_FIGURAS / "bootstrap_delta.png", dpi=300)
    plt.savefig(DIR_FIGURAS / "bootstrap_delta.pdf")
    plt.close()

    print(f"\nTabla T4: {ruta_t4}")
    print(f"Detalle : {DIR_TABLAS / 'T4_deltas_bloques.csv'}")
    print(f"Figura  : {DIR_FIGURAS / 'bootstrap_delta.png'}")


if __name__ == "__main__":
    main()

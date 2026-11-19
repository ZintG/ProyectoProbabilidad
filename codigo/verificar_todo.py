#!/usr/bin/env python3
"""codigo/verificar_todo.py
Revisión interna: recalcula todos los resultados y los compara con lo
reportado en tablas y figuras. Genera tablas/verificacion_resultados.csv.
"""

import csv
import math
import random
from collections import Counter
from pathlib import Path

from modelos import ModeloNgramas

BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_TABLAS = BASE_DIR / "tablas"

ALPHAS = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
ALPHA_OPTIMO = {1: 1.0, 2: 0.001, 3: 0.1, 4: 0.03, 5: 0.03}

filas = []
resumen = {"OK": 0, "FALLA": 0}


def check(bloque, nombre, reportado, calculado, tol=1e-6):
    dif = abs(reportado - calculado)
    estado = "OK" if dif <= tol else "FALLA"
    resumen[estado] += 1
    filas.append({
        "bloque": bloque,
        "verificacion": nombre,
        "reportado": f"{reportado:.10g}",
        "calculado": f"{calculado:.10g}",
        "diferencia": f"{dif:.3e}",
        "tolerancia": f"{tol:.0e}",
        "estado": estado,
    })
    marca = "OK   " if estado == "OK" else "FALLA"
    fmt = "{:>12.6f}" if max(abs(reportado), abs(calculado)) >= 0.001 \
        else "{:>12.3e}"
    print(f"  {marca} {nombre:<52} rep {fmt.format(reportado)} | "
          f"rec {fmt.format(calculado)}")
    return estado == "OK"


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bpc_validacion(modelo, validacion, entrenamiento, alpha):
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + validacion
    bits = 0.0
    aciertos = 0
    for i in range(n - 1, len(ext)):
        h = ext[i - (n - 1):i]
        bits -= modelo.log_prob_suavizada(ext[i], h, alpha)
        aciertos += 1
    return bits / len(validacion)


def costes(modelo, bloque, entrenamiento, alpha):
    n = modelo.n
    cola = entrenamiento[-(n - 1):] if n > 1 else ""
    ext = cola + bloque
    return [-modelo.log_prob_suavizada(ext[i], ext[i - (n - 1):i], alpha)
            for i in range(n - 1, len(ext))]


def main():
    ent = (DIR_DATOS / "entrenamiento.txt").read_text(encoding="utf-8")
    val = (DIR_DATOS / "validacion.txt").read_text(encoding="utf-8")
    pru = (DIR_DATOS / "prueba.txt").read_text(encoding="utf-8")

    print("\n=== BLOQUE 1: particiones, vocabulario y entropía (T1 / F1) ===")
    t1 = leer_csv(DIR_TABLAS / "T1_particiones.csv")
    esperado = {"Entrenamiento": 252626, "Validacion": 31578,
                "Prueba": 31579, "Total": 315783}
    check("T1", "longitud entrenamiento", esperado["Entrenamiento"], len(ent), 0)
    check("T1", "longitud validación", esperado["Validacion"], len(val), 0)
    check("T1", "longitud prueba", esperado["Prueba"], len(pru), 0)
    check("T1", "longitud total", esperado["Total"], len(ent) + len(val) + len(pru), 0)
    check("T1", "|V| del entrenamiento", 27, len(set(ent)), 0)

    cuenta = Counter(ent)
    N = len(ent)
    h_uni = -sum((c / N) * math.log2(c / N) for c in cuenta.values())
    check("F1", "entropía de unigramas (entrenamiento)", 4.059162507384771, h_uni, 1e-9)
    check("F1", "log2 |V|", 4.754887502163468, math.log2(27), 1e-9)
    check("F1", "redundancia R (fracción)", 0.146321, 1 - h_uni / math.log2(27), 1e-5)

    modelos = {n: ModeloNgramas(ent, n) for n in range(1, 6)}

    print("\n=== BLOQUE 2: ceros de la MLE en validación (T2) ===")
    for fila in leer_csv(DIR_TABLAS / "T2_ceros_validacion.csv"):
        n = int(fila["n"])
        m = modelos[n]
        cola = ent[-(n - 1):] if n > 1 else ""
        ext = cola + val
        ceros_ctx = ceros_par = 0
        for i in range(n - 1, len(ext)):
            h = ext[i - (n - 1):i]
            if m.conteo_contexto(h) == 0:
                ceros_ctx += 1
            elif m.conteo_par(h, ext[i]) == 0:
                ceros_par += 1
        ceros = ceros_ctx + ceros_par
        check("T2", f"n={n} contextos observados", int(fila["contextos_observados"]),
              len(m.c_h), 0)
        check("T2", f"n={n} n-gramas observados", int(fila["ngramas_observados"]),
              sum(len(v) for v in m.c_hy.values()), 0)
        check("T2", f"n={n} ceros totales", int(fila["ceros"]), ceros, 0)
        check("T2", f"n={n} ceros por c(h)=0", int(fila["ceros_contexto"]), ceros_ctx, 0)
        check("T2", f"n={n} ceros por c(h,y)=0", int(fila["ceros_par"]), ceros_par, 0)
        check("T2", f"n={n} porcentaje de ceros", float(fila["porcentaje_ceros"]),
              100 * ceros / len(val), 1e-9)

    print("\n=== BLOQUE 3: calibración de alpha (F2) ===")
    f2 = leer_csv(DIR_TABLAS / "F2_bpc_alpha.csv")
    guardado = {(int(f["n"]), float(f["alpha"])): float(f["bpc_validacion"])
                for f in f2}
    for n in range(1, 6):
        valores = {}
        for alpha in ALPHAS:
            v = bpc_validacion(modelos[n], val, ent, alpha)
            valores[alpha] = v
            check("F2", f"n={n} alpha={alpha} BPC validación",
                  guardado[(n, alpha)], v, 5e-4)
        mejor = min(valores, key=valores.get)
        check("F2", f"n={n} alpha óptimo (índice)", ALPHA_OPTIMO[n], mejor, 0)

    print("\n=== BLOQUE 4: evaluación en prueba (T3) ===")
    costes_pru = {}
    for fila in leer_csv(DIR_TABLAS / "T3_evaluacion_prueba.csv"):
        n = int(fila["n"])
        m = modelos[n]
        alpha = float(fila["alpha"])
        check("T3", f"n={n} alpha reportado", ALPHA_OPTIMO[n], alpha, 0)

        bits = 0.0
        for h, cont in m.c_hy.items():
            for y, c in cont.items():
                bits -= c * m.log_prob_suavizada(y, h, alpha)
        bpc_tr = bits / (m.N - m.n + 1)
        check("T3", f"n={n} BPC entrenamiento", float(fila["bpc_entrenamiento"]),
              bpc_tr, 1e-6)

        c = costes(m, pru, ent, alpha)
        costes_pru[n] = c
        bpc_pr = sum(c) / len(pru)
        check("T3", f"n={n} BPC prueba", float(fila["bpc_prueba"]), bpc_pr, 1e-6)
        check("T3", f"n={n} PPL prueba", float(fila["ppl_prueba"]), 2 ** bpc_pr, 1e-6)

    print("\n=== BLOQUE 5: desigualdad de Gibbs (T3_gibbs) ===")
    g = leer_csv(DIR_TABLAS / "T3_gibbs.csv")[0]
    p_test = {y: Counter(pru)[y] / len(pru) for y in modelos[1].V}
    h_p = -sum(v * math.log2(v) for v in p_test.values() if v > 0)
    h_pq = -sum(v * modelos[1].log_prob_suavizada(y, "", ALPHA_OPTIMO[1])
                for y, v in p_test.items() if v > 0)
    check("Gibbs", "H(p) de prueba", float(g["h_p"]), h_p, 1e-9)
    check("Gibbs", "H(p,q) de prueba", float(g["h_pq"]), h_pq, 1e-9)
    check("Gibbs", "KL = H(p,q) - H(p)", float(g["kl"]), h_pq - h_p, 1e-9)
    ok = h_p <= h_pq
    print(f"  {'OK   ' if ok else 'FALLA'} desigualdad H(p) <= H(p,q)"
          f"{'':>27} {h_p:>12.6f} | {h_pq:>12.6f}")
    resumen["OK" if ok else "FALLA"] += 1
    filas.append({"bloque": "Gibbs", "verificacion": "H(p) <= H(p,q)",
                  "reportado": f"{h_p:.10g}", "calculado": f"{h_pq:.10g}",
                  "diferencia": f"{h_pq - h_p:.3e}", "tolerancia": "0",
                  "estado": "OK" if ok else "FALLA"})

    print("\n=== BLOQUE 6: matriz y distribución estacionaria (F5) ===")
    m2 = modelos[2]
    a2 = ALPHA_OPTIMO[2]
    V = m2.V
    P = [[m2.prob_suavizada(V[j], V[i], a2) for j in range(m2.K)]
         for i in range(m2.K)]
    desv = max(abs(sum(f) - 1.0) for f in P)
    minimo = min(min(f) for f in P)
    check("F5", "desviación máxima de filas", 2.22e-16, desv, 1e-15)
    check("F5", "entrada mínima de P", 2.207e-08, minimo, 1e-11)

    K = len(P)
    pi = [1.0 / K] * K
    it = 0
    while True:
        it += 1
        nuevo = [sum(pi[i] * P[i][j] for i in range(K)) for j in range(K)]
        dif = sum(abs(nuevo[j] - pi[j]) for j in range(K))
        pi = nuevo
        if dif < 1e-10:
            break
    check("F5", "iteraciones hasta 1e-10", 22, it, 0)
    check("F5", "última diferencia L1", 3.35e-11, dif, 1e-11)
    check("F5", "suma de pi", 1.0, sum(pi), 1e-12)

    p_uni = [Counter(ent)[y] / len(ent) for y in V]
    dif_max = max(abs(a - b) for a, b in zip(pi, p_uni))
    l1 = sum(abs(a - b) for a, b in zip(pi, p_uni))
    check("F5", "diferencia máxima pi vs unigramas", 3.71e-06, dif_max, 1e-8)
    check("F5", "distancia L1 pi vs unigramas", 9.05e-06, l1, 1e-8)

    print("\n=== BLOQUE 7: bootstrap de bloques (T4) ===")
    t4 = leer_csv(DIR_TABLAS / "T4_bootstrap.csv")[0]
    deltas = [float(f["bpc_n4"]) - float(f["bpc_n5"])
              for f in leer_csv(DIR_TABLAS / "T4_deltas_bloques.csv")]
    check("T4", "número de bloques", int(t4["n_bloques"]), len(deltas), 0)
    check("T4", "caracteres cubiertos", int(t4["caracteres"]),
          sum(int(f["longitud"]) for f in
              leer_csv(DIR_TABLAS / "T4_deltas_bloques.csv")), 0)
    media = sum(deltas) / len(deltas)
    check("T4", "media de Delta_j", float(t4["delta_medio"]), media, 1e-6)
    check("T4", "bloques con Delta_j > 0", 14, sum(1 for d in deltas if d > 0), 0)

    rng = random.Random(2026)
    k = len(deltas)
    medias = sorted(sum(deltas[rng.randrange(k)] for _ in range(k)) / k
                    for _ in range(10000))
    inf = medias[int(round(0.025 * 9999))]
    sup = medias[int(round(0.975 * 9999))]
    check("T4", "IC 95 % inferior", float(t4["ic_inferior"]), inf, 1e-6)
    check("T4", "IC 95 % superior", float(t4["ic_superior"]), sup, 1e-6)
    check("T4", "el IC excluye el cero", 1.0, 1.0 if inf > 0 else 0.0, 0)

    # Coherencia con T3: promedio ponderado de los BPC de bloque
    det = leer_csv(DIR_TABLAS / "T4_deltas_bloques.csv")
    pond = sum(float(f["bpc_n4"]) * int(f["longitud"]) for f in det) / len(pru)
    check("T4", "BPC n=4 ponderado = T3", 2.346130, pond, 1e-5)
    pond5 = sum(float(f["bpc_n5"]) * int(f["longitud"]) for f in det) / len(pru)
    check("T4", "BPC n=5 ponderado = T3", 2.251390, pond5, 1e-5)

    print("\n=== BLOQUE 8: muestras de la Fase 5 (T5) ===")
    for f in leer_csv(DIR_TABLAS / "T5_muestras.csv"):
        check("T5", f"{f['modelo']} longitud total", 306, len(f["texto"]), 0)
        check("T5", f"{f['modelo']} semilla", 2026, int(f["semilla"]), 0)
        check("T5", f"{f['modelo']} prefijo", 1.0,
              1.0 if f["texto"].startswith("habia ") else 0.0, 0)

    DIR_TABLAS.mkdir(exist_ok=True)
    ruta = DIR_TABLAS / "verificacion_resultados.csv"
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("\n" + "=" * 72)
    print(f"VERIFICACIONES: {resumen['OK']} correctas, {resumen['FALLA']} fallidas")
    print(f"Detalle: {ruta}")
    print("=" * 72)


if __name__ == "__main__":
    main()

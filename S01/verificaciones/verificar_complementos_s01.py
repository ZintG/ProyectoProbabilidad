"""Verificación numérica de los resultados nuevos o modificados de S01 v0.9.

Cada bloque reproduce una cifra que aparece en contenido_libro.tex (texto
principal o Complementos S01.C1-C12). Uso, desde sesiones/S01:
    python3 verificaciones/verificar_complementos_s01.py
Termina con código 0 solo si todas las comprobaciones se cumplen.
"""
import csv
import itertools
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

ROOT = Path(__file__).resolve().parents[1]
fallos = []


def ok(nombre, cond, detalle=""):
    print(("OK  " if cond else "XX  ") + nombre + (f"  [{detalle}]" if detalle else ""))
    if not cond:
        fallos.append(nombre)


# --- C5: función Gamma, Beta e integral de Dirichlet --------------------------
for x in (0.5, 1.0, 2.5, 7.0):
    g, _ = integrate.quad(lambda t: t ** (x - 1) * math.exp(-t), 0, np.inf)
    ok(f"C5 Gamma({x}) por integral", math.isclose(g, math.gamma(x), rel_tol=1e-7), f"{g:.10f}")
ok("C5 Gamma(x+1)=x Gamma(x), x=2.5", math.isclose(math.gamma(3.5), 2.5 * math.gamma(2.5)))
for a, b in ((0.5, 0.5), (2.0, 3.0), (1.5, 4.0)):
    beta, _ = integrate.quad(lambda v: v ** (a - 1) * (1 - v) ** (b - 1), 0, 1)
    ok(f"C5 B({a},{b}) = Gamma(a)Gamma(b)/Gamma(a+b)",
       math.isclose(beta, math.gamma(a) * math.gamma(b) / math.gamma(a + b), rel_tol=1e-6), f"{beta:.8f}")
for beta_v in ((2.0, 3.0, 1.5), (7.0, 4.0, 2.0)):
    b1, b2, b3 = beta_v
    val, _ = integrate.dblquad(lambda q2, q1: q1 ** (b1 - 1) * q2 ** (b2 - 1) * (1 - q1 - q2) ** (b3 - 1),
                               0, 1, 0, lambda q1: 1 - q1)
    teo = math.gamma(b1) * math.gamma(b2) * math.gamma(b3) / math.gamma(b1 + b2 + b3)
    ok(f"C5 integral de Dirichlet K=3, beta={beta_v}", math.isclose(val, teo, rel_tol=1e-6), f"{val:.10f}")

# --- C6 / §1.1.3: posterior, predictiva, media y moda -------------------------
c = np.array([6, 3, 1, 0, 0])
N, K = c.sum(), len(c)
for alpha, esperado in ((1, [F(7, 15), F(4, 15), F(2, 15), F(1, 15), F(1, 15)]),
                        (F(1, 2), [F(13, 25), F(7, 25), F(3, 25), F(1, 25), F(1, 25)])):
    pred = [F(int(ci)) + alpha for ci in c]
    tot = sum(pred)
    ok(f"C6 predictiva alpha={alpha}", [x / tot for x in pred] == esperado, str([str(x / tot) for x in pred]))
# media posterior por Monte Carlo (alpha=1 -> Dir(7,4,2,1,1))
rng = np.random.default_rng(20261031)
muestras = rng.dirichlet(c + 1, size=400_000)
ok("C6 media posterior Monte Carlo ~ (7,4,2,1,1)/15",
   np.allclose(muestras.mean(axis=0), (c + 1) / 15, atol=2e-3), str(np.round(muestras.mean(axis=0), 4)))
# moda con alpha=2: beta=(8,5,3,2,2); fórmula (beta-1)/(sum beta - K) = (7,4,2,1,1)/15
beta2 = c + 2
moda_formula = (beta2 - 1) / (beta2.sum() - K)
res = optimize.minimize(lambda z: -np.sum((beta2 - 1) * np.log(np.exp(z) / np.exp(z).sum())),
                        np.zeros(K), method="BFGS")
moda_num = np.exp(res.x) / np.exp(res.x).sum()
ok("C6 moda Dir(8,5,3,2,2) = (7,4,2,1,1)/15", np.allclose(moda_num, moda_formula, atol=1e-6),
   str(np.round(moda_num, 6)))
ok("C6 media Dir(8,5,3,2,2) = (8,5,3,2,2)/20", np.allclose(beta2 / beta2.sum(), [0.4, 0.25, 0.15, 0.1, 0.1]))
# con alpha=1 la moda coincide con el MLE c/N
beta1 = c + 1
ok("C6 moda alpha=1 = MLE c/N", np.allclose((beta1 - 1) / (beta1.sum() - K), c / N))
# mezcla convexa (R3) y masa de no vistos
ok("R3 lambda N=10,K=5,alpha=1 = 2/3", F(10, 10 + 5) == F(2, 3))
ok("R3 lambda N=10,K=100,alpha=1 = 1/11", F(10, 10 + 100) == F(1, 11))
masa = [F((Kx - 3) * 1, 10 + Kx * 1) for Kx in range(3, 60)]
ok("C6 masa de no vistos (K-K+)a/(N+Ka) creciente en K (N=10,K+=3,a=1)",
   all(x < y for x, y in zip(masa, masa[1:])), f"K=5: {masa[2]}, K=100: {F(97, 110)}")
# R6: contexto b con alpha=1/2
cb = [2, 1, 0]
ok("R6 q_{1/2}(.|b)=(5/9,1/3,1/9)", [(F(x) + F(1, 2)) / (3 + F(3, 2)) for x in cb] == [F(5, 9), F(1, 3), F(1, 9)])

# --- C9: cadena de Markov suavizada ------------------------------------------
P = [[F(1, 7), F(3, 7), F(3, 7)], [F(1, 2), F(1, 3), F(1, 6)], [F(2, 5), F(2, 5), F(1, 5)]]
u = F(98)
w = F(75, 98) * u
v = F(54, 49) * u
ok("C9 eliminación: w=75u/98, v=54u/49 -> (98,108,75)", (u, v, w) == (98, 108, 75))
pi = [F(98, 281), F(108, 281), F(75, 281)]
ok("C9 pi P = pi (exacto)", all(sum(pi[i] * P[i][j] for i in range(3)) == pi[j] for j in range(3)))
delta = min(min(f) for f in P)
ok("C9 delta=min P_ij=1/7, factor de contracción 1-K delta=4/7", delta == F(1, 7) and 1 - 3 * delta == F(4, 7))
Pn = np.array([[float(x) for x in f] for f in P])
mu = np.array([1.0, 0.0, 0.0])
dist = []
for t in range(1, 9):
    mu = mu @ Pn
    dist.append(np.abs(mu - np.array([float(x) for x in pi])).sum())
cota = [2 * (4 / 7) ** t for t in range(1, 9)]
ok("C9 ||mu P^t - pi||_1 <= 2 (4/7)^t, t=1..8", all(d <= b + 1e-15 for d, b in zip(dist, cota)),
   f"t=8: {dist[-1]:.2e} <= {cota[-1]:.2e}")
Hinf = -sum(float(pi[i]) * sum(float(P[i][j]) * math.log2(float(P[i][j])) for j in range(3)) for i in range(3))
Hpi = -sum(float(x) * math.log2(float(x)) for x in pi)
ok("C9 tasa de entropía H_inf(P) ~ 1.472301 bits", math.isclose(Hinf, 1.4723008, abs_tol=5e-7), f"{Hinf:.6f}")
ok("C9 H(pi) ~ 1.568836 bits", math.isclose(Hpi, 1.5688362, abs_tol=5e-7), f"{Hpi:.6f}")

# --- C7 / C8: información ----------------------------------------------------
def H(p):
    return -sum(x * math.log2(x) for x in p if x > 0)


def KL(p, q):
    return sum(a * math.log2(a / b) for a, b in zip(p, q) if a > 0)


# regla de la cadena de KL para T=2 en un ejemplo pequeño
p1, q1 = [0.5, 0.5], [0.25, 0.75]
pc = [[0.9, 0.1], [0.2, 0.8]]
qc = [[0.5, 0.5], [0.5, 0.5]]
pj = [p1[i] * pc[i][j] for i in range(2) for j in range(2)]
qj = [q1[i] * qc[i][j] for i in range(2) for j in range(2)]
lhs = KL(pj, qj)
rhs = KL(p1, q1) + sum(p1[i] * KL(pc[i], qc[i]) for i in range(2))
ok("C8 regla de la cadena de KL (T=2)", math.isclose(lhs, rhs, rel_tol=1e-12), f"{lhs:.6f}")
ok("C8 agregación: D(p_f||q_f)=0.207519 <= 0.25",
   math.isclose(KL([.5, .5], [.25, .75]), 0.207519, abs_tol=1e-6) and KL([.5, .5], [.25, .75]) <= 0.25)
# suma logarítmica: a=(1/2,1/4,1/4), b=(1/4,1/2,1/4) bloque {b,c}
a, b = [0.25, 0.25], [0.5, 0.25]
ok("C8 suma logarítmica en el bloque {b,c}",
   sum(x * math.log(x / y) for x, y in zip(a, b)) >= sum(a) * math.log(sum(a) / sum(b)) - 1e-15)
# monedas: H(X3|X2)=1, H(X3|X1,X2)=0, I(X3;X1|X2)=1
ok("C7 monedas: I(X3;X1|X2) = H(X3|X2)-H(X3|X1,X2) = 1 bit", H([.5, .5]) - 0 == 1)

# --- C10: parada geométrica y PPL/BPC ----------------------------------------
r = 0.2
EM = sum(n * (1 - r) ** n * r for n in range(0, 2000))
ok("C10 E[M]=(1-r)/r con r=0.2 (=4)", math.isclose(EM, (1 - r) / r, rel_tol=1e-12), f"{EM:.10f}")
ok("C10 P(M>=m)=(1-r)^m con m=10", math.isclose(sum((1 - r) ** n * r for n in range(10, 3000)), 0.8 ** 10))
ok("C10 BPC=(T/|z|)log2 PPL (A: 100,3.2,100)", math.isclose(100 / 100 * math.log2(3.2), 100 * math.log2(3.2) / 100))
ok("C10 Kraft {0,10,11}: suma 1", F(1, 2) + F(1, 4) + F(1, 4) == 1)

# --- C12: bootstrap exacto con la regla de cuantiles del código -------------
filas = list(csv.DictReader((ROOT / "experimentos" / "resultados_python.csv").open(encoding="utf-8")))
d = [float(f["delta_bpc"]) for f in filas]
J = len(d)
medias = sorted(sum(d[i] for i in idx) / J for idx in itertools.product(range(J), repeat=J))


def cuantil(s, p):
    h = (len(s) - 1) * p
    lo = int(h)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (h - lo) * (s[hi] - s[lo])


ic = (cuantil(medias, 0.025), cuantil(medias, 0.975))
ok("C12 enumeración J^J = 6^6 = 46656", len(medias) == 46656)
ok("C12 intervalo percentil [-0.66771,-0.42038]",
   math.isclose(ic[0], -0.66770598, abs_tol=5e-9) and math.isclose(ic[1], -0.42038147, abs_tol=5e-9),
   f"[{ic[0]:.8f}, {ic[1]:.8f}]")
ok("C12 media = -0.54025", math.isclose(sum(d) / J, -0.54024842, abs_tol=5e-9))


# --- C11: BPE, reducción exacta y contraejemplo a la optimalidad -------------
def fusionar(seg, par):
    nuevo = {}
    for w, s in seg.items():
        i, out = 0, []
        while i < len(s):
            if i < len(s) - 1 and (s[i], s[i + 1]) == par:
                out.append(s[i] + s[i + 1])
                i += 2
            else:
                out.append(s[i])
                i += 1
        nuevo[w] = tuple(out)
    return nuevo


def pares(seg, frec):
    cnt = {}
    for w, s in seg.items():
        for x, y in zip(s, s[1:]):
            cnt[(x, y)] = cnt.get((x, y), 0) + frec[w]
    return cnt


def longitud(seg, frec):
    return sum(len(s) * frec[w] for w, s in seg.items())


def voraz(seg, frec, k):
    for _ in range(k):
        cnt = pares(seg, frec)
        if not cnt:
            break
        m = max(cnt.values())
        seg = fusionar(seg, min(p for p, v in cnt.items() if v == m))
    return longitud(seg, frec)


def optimo(seg, frec, k):
    if k == 0:
        return longitud(seg, frec)
    cnt = pares(seg, frec)
    if not cnt:
        return longitud(seg, frec)
    return min(optimo(fusionar(seg, p), frec, k - 1) for p in cnt)


# corpus del libro: la reducción en cada paso coincide con las sustituciones efectivas
corpus = {"casa": 5, "casas": 2, "cosa": 6, "cosas": 3, "caso": 4}
seg = {w: tuple(w) + ("</w>",) for w in corpus}
L = [longitud(seg, corpus)]
for _ in range(6):
    cnt = pares(seg, corpus)
    m = max(cnt.values())
    par = min(p for p, v in cnt.items() if v == m)
    antes = longitud(seg, corpus)
    nuevo = fusionar(seg, par)
    k_ef = sum(corpus[w] * (len(seg[w]) - len(nuevo[w])) for w in seg)
    seg = nuevo
    L.append(longitud(seg, corpus))
    ok(f"C11 paso {len(L)-1}: reducción = sustituciones efectivas ponderadas", antes - L[-1] == k_ef, f"{par} -> {k_ef}")
ok("C11 longitudes 105,89,78,67,58,49,43", L == [105, 89, 78, 67, 58, 49, 43])
s5 = fusionar({"x": tuple("aaaaa")}, ("a", "a"))["x"]
ok("C11 aaaaa: 4 pares solapados, 2 sustituciones, longitud 3", len(s5) == 3)

# contraejemplo fijo; la ruta óptima (a,c) y luego (e,b) da 59-8-8=43
pares_ini = pares(seg_ce := {w: tuple(w) for w in {"bdac": 4, "ebac": 4, "bad": 5, "feb": 4}}, {"bdac": 4, "ebac": 4, "bad": 5, "feb": 4})
ok("C11 frecuencias iniciales: (b,a)=9 único máximo, (a,c)=8, (e,b)=8",
   pares_ini[("b", "a")] == 9 and pares_ini[("a", "c")] == 8 and pares_ini[("e", "b")] == 8
   and sorted(pares_ini.values())[-2] == 8)
# contraejemplo fijo (encontrado por búsqueda exhaustiva y documentado en C11)
ce = {"bdac": 4, "ebac": 4, "bad": 5, "feb": 4}
seg_ce = {w: tuple(w) for w in ce}
g2, o2 = voraz(seg_ce, ce, 2), optimo(seg_ce, ce, 2)
ok("C11 contraejemplo {bdac:4, ebac:4, bad:5, feb:4}, 2 fusiones: inicial 59, voraz 45 > óptimo 43",
   (longitud(seg_ce, ce), g2, o2) == (59, 45, 43),
   f"inicial {longitud(seg_ce, ce)}, voraz {g2}, óptimo {o2}")

print(f"\n{len(fallos)} fallo(s)")
raise SystemExit(1 if fallos else 0)

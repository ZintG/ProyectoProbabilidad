#!/usr/bin/env python3
"""codigo/modelos.py
Modelos de n-gramas: conteos de contextos y pares (contexto, símbolo).
"""

import math
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_ENTRENAMIENTO = BASE_DIR / "datos" / "entrenamiento.txt"


class ModeloNgramas:
    def __init__(self, texto, n):
        self.n = n
        self.texto = texto
        self.V = sorted(set(texto))
        self.K = len(self.V)
        self.N = len(texto)

        self.c_h = Counter()                  # c(h)
        self.c_hy = defaultdict(Counter)      # c(h, y)

        for t in range(self.N - n + 1):
            h = texto[t : t + n - 1]          # n=1 -> ""
            y = texto[t + n - 1]
            self.c_h[h] += 1
            self.c_hy[h][y] += 1

    def conteo_contexto(self, h):
        return self.c_h.get(h, 0)

    def conteo_par(self, h, y):
        return self.c_hy.get(h, {}).get(y, 0)

    def prob_mle(self, y, h):
        """q_MLE(y | h) = c(h, y) / c(h)."""
        ch = self.conteo_contexto(h)
        if ch == 0:
            return 0.0
        return self.conteo_par(h, y) / ch

    def log_prob_mle(self, y, h):
        """log2 q_MLE(y | h); -inf si q = 0."""
        p = self.prob_mle(y, h)
        if p == 0.0:
            return float("-inf")
        return math.log2(p)

    def log_verosimilitud(self, q_especial=None):
        """Log-verosimilitud total del entrenamiento (log natural).

        Si q_especial = (h0, q0), usa q0 para el contexto h0
        y la MLE para los demás contextos.
        """
        total = 0.0
        for h, continuaciones in self.c_hy.items():
            ch = self.c_h[h]
            for y, c in continuaciones.items():
                if q_especial is not None and h == q_especial[0]:
                    q = q_especial[1][y]
                else:
                    q = c / ch
                total += c * math.log(q)
        return total

    def prob_suavizada(self, y, h, alpha):
        """q_alpha(y | h) = (c(h, y) + alpha) / (c(h) + alpha * K)."""
        if alpha <= 0:
            raise ValueError("alpha debe ser > 0")
        return (self.conteo_par(h, y) + alpha) / (
            self.conteo_contexto(h) + alpha * self.K
        )

    def log_prob_suavizada(self, y, h, alpha):
        """log2 q_alpha(y | h)."""
        return math.log2(self.prob_suavizada(y, h, alpha))


def main():
    texto = RUTA_ENTRENAMIENTO.read_text(encoding="utf-8")

    print(f"Entrenamiento: {len(texto)} caracteres")
    print(f"|V| = {len(set(texto))}")
    print(f"V = {''.join(sorted(set(texto)))!r}")
    print()

    for n in range(1, 6):
        modelo = ModeloNgramas(texto, n)

        max_desv = 0.0
        for h in modelo.c_h:
            suma = sum(modelo.prob_mle(y, h) for y in modelo.V)
            max_desv = max(max_desv, abs(suma - 1.0))

        assert max_desv <= 1e-12, f"n={n}: la suma no da 1"

        print(
            f"n={n}: "
            f"{len(modelo.c_h)} contextos, "
            f"{sum(len(c) for c in modelo.c_hy.values())} n-gramas distintos, "
            f"desv. máx. = {max_desv:.2e}, "
            f"log-ver. = {modelo.log_verosimilitud():.4f}"
        )

    # Verificación de MLE con dos perturbaciones (n=2)
    modelo = ModeloNgramas(texto, 2)
    h0 = " "
    q0 = {y: modelo.prob_mle(y, h0) for y in modelo.V}

    qA = dict(q0)
    qA["e"] -= 0.01
    qA["d"] += 0.01

    y_cero = next(y for y in modelo.V if modelo.conteo_par(h0, y) == 0)
    qB = dict(q0)
    qB["e"] -= 0.01
    qB[y_cero] += 0.01

    ll_mle = modelo.log_verosimilitud()
    ll_A = modelo.log_verosimilitud((h0, qA))
    ll_B = modelo.log_verosimilitud((h0, qB))

    print()
    print("Verificación de MLE con perturbaciones (n=2, contexto ' '):")
    print(f"  MLE            : {ll_mle:.4f}")
    print(f"  Perturbación A : {ll_A:.4f}  (e -> d)")
    print(f"  Perturbación B : {ll_B:.4f}  (e -> {y_cero!r}, conteo 0)")

    assert ll_mle > ll_A, "La MLE no superó a la perturbación A"
    assert ll_mle > ll_B, "La MLE no superó a la perturbación B"
    print("  Correcto: la MLE es mayor en ambos casos.")


if __name__ == "__main__":
    main()
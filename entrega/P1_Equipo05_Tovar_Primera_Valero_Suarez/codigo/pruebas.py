#!/usr/bin/env python3
"""codigo/pruebas.py
Prueba de cordura obligatoria y verificaciones matemáticas básicas
según el enunciado del Proyecto de Probabilidad (Fase 0 y verificaciones).
"""

import math
from collections import Counter


def calcular_unigramas(texto: str):
    """Calcula conteos de unigramas y su distribución de probabilidad."""
    conteos = Counter(texto)
    n_total = len(texto)
    frecuencias = {char: c / n_total for char, c in conteos.items()}
    return conteos, frecuencias


def calcular_entropia_unigramas(frecuencias: dict) -> float:
    """Calcula la entropía de Shannon H(p) en bits para unigramas:
    H(p) = - sum(p_i * log2(p_i))
    """
    return -sum(p * math.log2(p) for p in frecuencias.values() if p > 0)


def calcular_transiciones_bigramas(texto: str):
    """Calcula conteos de contextos c(h) y pares c(h, y) para bigramas."""
    pares = list(zip(texto, texto[1:]))
    conteos_pares = Counter(pares)
    # El contexto de un bigrama es el primer caracter del par
    conteos_contextos = Counter(texto[:-1])
    return conteos_contextos, conteos_pares, len(pares)


def prob_mle_bigrama(h: str, y: str, conteos_contextos: Counter, conteos_pares: Counter) -> float:
    """Probabilidad condicional por máxima verosimilitud (frecuencia relativa):
    q(y | h) = c(h, y) / c(h)
    """
    c_h = conteos_contextos[h]
    if c_h == 0:
        return 0.0
    return conteos_pares[(h, y)] / c_h


def prob_suavizada_bigrama(h: str, y: str, conteos_contextos: Counter, conteos_pares: Counter,
                           alpha: float, tam_vocabulario: int) -> float:
    """Probabilidad condicional con suavizado aditivo (Laplace generalizado):
    q_alpha(y | h) = (c(h, y) + alpha) / (c(h) + alpha * |V|)
    """
    c_h = conteos_contextos[h]
    c_hy = conteos_pares[(h, y)]
    return (c_hy + alpha) / (c_h + alpha * tam_vocabulario)


def calcular_bpc_y_ppl_mle_bigrama(texto: str, conteos_contextos: Counter, conteos_pares: Counter):
    """Calcula el BPC y la perplejidad sobre todas las transiciones del texto:
    BPC = - (1 / N_e) * sum(log2(q(x_t | x_t-1)))
    PPL = 2^(BPC)
    """
    transiciones = list(zip(texto, texto[1:]))
    n_e = len(transiciones)
    bits_totales = 0.0
    for h, y in transiciones:
        p = prob_mle_bigrama(h, y, conteos_contextos, conteos_pares)
        if p == 0.0:
            return float('inf'), float('inf')
        bits_totales -= math.log2(p)
    bpc = bits_totales / n_e
    ppl = 2 ** bpc
    return bpc, ppl


def ejecutar_prueba_cordura():
    """Ejecuta la prueba con la palabra de juguete 'abracadabra'
    y verifica contra los valores de la Tabla 2 del enunciado.
    """
    texto_prueba = "abracadabra"
    vocabulario = sorted(set(texto_prueba))
    tam_vocabulario = len(vocabulario)

    print("=" * 65)
    print(f"PRUEBA DE CORDURA OBLIGATORIA (Texto: '{texto_prueba}')")
    print("=" * 65)

    # 1. Conteos de unigramas
    conteos_uni, frecs_uni = calcular_unigramas(texto_prueba)
    esperado_conteos = {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
    print(f"\n1. Conteos de unigramas:")
    for k, v in esperado_conteos.items():
        obtenido = conteos_uni[k]
        ok = obtenido == v
        print(f"   - Carácter '{k}': {obtenido} (esperado: {v}) -> {'[OK]' if ok else '[FAIL]'}")
        assert ok, f"Error en conteo de {k}"

    # 2. Entropía de unigramas
    entropia = calcular_entropia_unigramas(frecs_uni)
    esperado_entropia = 2.0404
    ok_entropia = abs(entropia - esperado_entropia) < 1e-4
    print(f"\n2. Entropía de unigramas: {entropia:.4f} bits (esperado: {esperado_entropia} bits) -> {'[OK]' if ok_entropia else '[FAIL]'}")
    assert ok_entropia, "Error en entropía"

    # 3. Transiciones y probabilidad MLE q(b | a)
    conteos_ctx, conteos_pares, n_transiciones = calcular_transiciones_bigramas(texto_prueba)
    q_mle = prob_mle_bigrama('a', 'b', conteos_ctx, conteos_pares)
    esperado_q_mle = 0.5
    ok_mle = abs(q_mle - esperado_q_mle) < 1e-6
    print(f"\n3. q_hat(b | a) por MLE: {q_mle:.4f} (esperado: {esperado_q_mle}) -> {'[OK]' if ok_mle else '[FAIL]'}")
    assert ok_mle, "Error en q_hat(b | a) MLE"

    # 4. Probabilidad suavizada q_alpha(b | a) con alpha = 1 y |V| = 5
    q_suavizada = prob_suavizada_bigrama('a', 'b', conteos_ctx, conteos_pares, alpha=1.0, tam_vocabulario=tam_vocabulario)
    esperado_q_suavizada = 1.0 / 3.0
    ok_suavizada = abs(q_suavizada - esperado_q_suavizada) < 1e-4
    print(f"\n4. q_hat_alpha(b | a) con alpha=1 y |V|=5: {q_suavizada:.4f} (esperado: {esperado_q_suavizada:.4f} = 1/3) -> {'[OK]' if ok_suavizada else '[FAIL]'}")
    assert ok_suavizada, "Error en q_hat suavizada"

    # 5. BPC y PPL sobre sus 10 transiciones
    bpc, ppl = calcular_bpc_y_ppl_mle_bigrama(texto_prueba, conteos_ctx, conteos_pares)
    esperado_bpc = 0.6
    esperado_ppl = 1.5157
    ok_bpc = abs(bpc - esperado_bpc) < 1e-4
    ok_ppl = abs(ppl - esperado_ppl) < 1e-4

    print(f"\n5. BPC de bigrama MLE sobre 10 transiciones: {bpc:.4f} bits (esperado: {esperado_bpc:.4f} bits) -> {'[OK]' if ok_bpc else '[FAIL]'}")
    print(f"6. Perplejidad (PPL): {ppl:.4f} (esperada: {esperado_ppl:.4f}) -> {'[OK]' if ok_ppl else '[FAIL]'}")
    assert ok_bpc, "Error en BPC"
    assert ok_ppl, "Error en PPL"

    print("\n" + "=" * 65)
    print("¡TODAS LAS PRUEBAS DE CORDURA PASARON CON ÉXITO AL 100%!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    ejecutar_prueba_cordura()

"""S01: ejemplos matemáticos reproducibles, solo biblioteca estándar de Python.
Datos de demostración SON ILUSTRATIVOS, no evidencias sobre corpus reales.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from math import log2

TRAIN = "abacabbacb"
TEST = "abca"
ALPHABET = tuple(sorted(set(TRAIN + TEST)))
WORDS = {"casa": 5, "casas": 2, "cosa": 6, "cosas": 3, "caso": 4}


def bigram_counts(text: str, alphabet=ALPHABET):
    counts = {a: {b: 0 for b in alphabet} for a in alphabet}
    for a, b in zip(text, text[1:]):
        counts[a][b] += 1
    return counts


def transitions(counts, alpha=1.0):
    if alpha < 0:
        raise ValueError("alpha debe ser no negativo")
    k = len(ALPHABET)
    out = {}
    for a in ALPHABET:
        n = sum(counts[a].values())
        if n + k * alpha == 0:
            raise ValueError("contexto sin observaciones: suavizar o retroceder")
        out[a] = {b: (counts[a][b] + alpha) / (n + k * alpha) for b in ALPHABET}
    return out


def length_and_ppl(text, P, p_initial=1/3):
    # Probabilidad de SECUENCIA ENTERA con p(X_1)=1/3 declarada.
    probs = [p_initial] + [P[a][b] for a, b in zip(text, text[1:])]
    bits = float('inf') if any(p == 0 for p in probs) else -sum(log2(p) for p in probs)
    return {"bits": bits, "bpc": bits / len(text),
            "ppl": 2 ** (bits / len(text)), "eventos": len(probs)}


def bpe(nmerges=6):
    # El símbolo # es un marcador de fin de palabra, representado de forma textual.
    words = {word: list(word) + ["<eow>"] for word in WORDS}
    length = lambda: sum(len(seq) * WORDS[w] for w, seq in words.items())
    steps = []
    for step in range(1, nmerges+1):
        freq = Counter()
        for w, seq in words.items():
            for a, b in zip(seq, seq[1:]):
                freq[(a, b)] += WORDS[w]
        if not freq:
            break
        target = min(k for k, v in freq.items() if v == max(freq.values()))
        before = length()
        reduction = 0
        for w, seq in words.items():
            res, i = [], 0
            while i < len(seq):
                if i+1 < len(seq) and (seq[i], seq[i+1]) == target:
                    res.append(seq[i] + seq[i+1]); i += 2; reduction += WORDS[w]
                else:
                    res.append(seq[i]); i += 1
            words[w] = res
        after = length()
        assert before - after == reduction, (step, before, after, reduction)
        steps.append((step, target, freq[target], reduction, after))
    return steps, words


def kl(p, q):
    """Divergencia KL en bits, incluyendo la convencion de soporte."""
    if len(p) != len(q):
        raise ValueError("dimensiones distintas")
    if any(x < 0 for x in p) or any(x < 0 for x in q):
        raise ValueError("probabilidades negativas")
    if any(a > 0 and b == 0 for a, b in zip(p, q)):
        return float("inf")
    return sum(a * log2(a/b) for a, b in zip(p, q) if a > 0)


def summary():
    C = bigram_counts(TRAIN)
    mle = transitions(C, 0)
    smooth = transitions(C, 1)
    assert sum(sum(r.values()) for r in C.values()) == len(TRAIN) - 1
    for matrix in (mle, smooth):
        assert all(abs(sum(row.values())-1) < 1e-12 for row in matrix.values())
    assert C == {'a': {'a': 0,'b': 2,'c': 2},'b':{'a':2,'b':1,'c':0},'c':{'a':1,'b':1,'c':0}}
    assert abs(smooth['a']['b'] - 3/7) < 1e-12
    assert abs(smooth['b']['c'] - 1/6) < 1e-12
    assert abs(smooth['c']['a'] - 2/5) < 1e-12
    result = length_and_ppl(TEST, smooth)
    assert abs(result['bits'] - log2(105)) < 1e-12
    assert length_and_ppl(TEST,mle)['bits'] == float('inf')
    assert abs(kl((.5,.25,.25),(.25,.5,.25)) - .25) < 1e-12
    assert abs(kl((.75,.25),(.5,.5)) - (1 - (-(.75*log2(.75)+.25*log2(.25))))) < 1e-12
    steps, words = bpe()
    assert steps[0][4] == 89 and steps[5][4] == 43
    return C, result, steps, words

if __name__ == '__main__':
    C, r, steps, words = summary()
    print('MATRIZ CONTEOS', C)
    print('PRUEBA CON PROB. INICIAL UNIFORME', r)
    print('BPE: paso, par, frecuencia bruta, sustituciones efectivas, longitud')
    for step in steps:
        print(step)
    print('TOKENIZACION FINAL', words)
    print('H(p)=', 1.5, 'H(p,q)=', 1.75, 'KL(p||q)=', .25)
    print('PPL [1/2,1/4,1/8,1/2]=', 2**1.75)
    print('BPC A=', log2(3.2), 'BPC B=', .3*log2(25))

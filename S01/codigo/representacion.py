"""S01 v0.4: representaciones didácticas (Python estándar).
No se trata de un tokenizador neuronal ni de un corpus real.
"""
from collections import Counter

FRASE = "el gato mira al perro"
TOKENS = FRASE.split()
V = list(dict.fromkeys(TOKENS))
IDS = {palabra: i + 1 for i, palabra in enumerate(V)}

def ngramas(toks, n):
    return [tuple(toks[i:i+n]) for i in range(len(toks)-n+1)] if n <= len(toks) else []

def one_hot(token, vocabulary):
    return [int(token == t) for t in vocabulary]

assert len(TOKENS) == 5
assert len(ngramas(TOKENS, 2)) == 4
assert len(ngramas(TOKENS, 3)) == 3
assert ngramas(TOKENS, 2)[0] == ("el", "gato")
assert sum(one_hot("gato", V)) == 1
if __name__ == "__main__":
    print("Texto original:", FRASE)
    print("Tokens:", TOKENS)
    print("Bigrama inicial:", ngramas(TOKENS, 2)[0])
    print("Trigramas:", ngramas(TOKENS, 3))
    print("Identificadores:", IDS)
    print("One-hot(gato):", one_hot("gato", V))
    print("Bolsa:", dict(Counter(TOKENS)))

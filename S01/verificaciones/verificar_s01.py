"""Reproduce cifras de demostracion de S01; requiere Python 3 sin dependencias."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codigo'))
from s01 import summary, length_and_ppl, transitions, bigram_counts, bpe, kl
from math import log2, isclose, sqrt
from fractions import Fraction
from representacion import TOKENS, ngramas, V, one_hot

C, result, steps, segmentation = summary()
assert result['eventos'] == 4
assert isclose(result['bpc'], log2(105)/4, rel_tol=0, abs_tol=1e-12)
assert isclose(result['ppl'], 105 ** (1/4), rel_tol=0, abs_tol=1e-12)
assert [row[4] for row in steps] == [89, 78, 67, 58, 49, 43]
assert all(row[2] == row[3] for row in steps)
assert isclose(kl((.5,.25,.25), (.25,.5,.25)), .25, abs_tol=1e-12)
assert kl((.5,.5), (1.0,0.0)) == float('inf')
assert kl((1.0,0.0), (1.0,0.0)) == 0.0
assert len(TOKENS)==5 and len(ngramas(TOKENS,2))==4 and len(ngramas(TOKENS,3))==3
assert one_hot('gato',V) == [0,1,0,0,0]
assert isclose(-2*.2*log2(.2)-.6*log2(.6),1.3709505944546687,abs_tol=1e-12)
assert isclose(log2(3.2), 1.6780719051126378, abs_tol=1e-12)
assert isclose(.3*log2(25), 1.3931568569324173, abs_tol=1e-12)
# Matriz suavizada y distribucion estacionaria (todas las coordenadas).
P = [[Fraction(1,7), Fraction(3,7), Fraction(3,7)],
     [Fraction(1,2), Fraction(1,3), Fraction(1,6)],
     [Fraction(2,5), Fraction(2,5), Fraction(1,5)]]
pi = [Fraction(98,281), Fraction(108,281), Fraction(75,281)]
assert sum(pi) == 1
assert all(sum(pi[i]*P[i][j] for i in range(3)) == pi[j] for j in range(3))
assert isclose(-(0.9*log2(.9)+.1*log2(.1)), .4689955935892812, abs_tol=1e-12)
assert isclose(.5+.5*log2(2/3), .20751874963942185, abs_tol=1e-12)
assert isclose(sqrt(.05/12), .06454972243679027, abs_tol=1e-12)
assert isclose(.5 * log2(2) + .5 * log2(2/3), .20751874963942185, abs_tol=1e-12)
print('S01 verificada (v0.9): tokens, ngramas, one-hot, MLE, Dirichlet, KL incluyendo soporte, PPL, BPC, BPE')

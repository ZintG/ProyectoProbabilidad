"""Regla 1 (terminología antes del uso) para S01, comprobada automáticamente.

Para cada término: primera aparición (expresión regular de uso) frente a la línea
donde se define (expresión regular de definición). Ignora comentarios LaTeX.
La tabla de notación (\\label{s01:notacion}) cuenta como definición operativa
solo para los símbolos marcados con en_tabla=True.
Escribe REGISTRO_TERMINOLOGIA_S01.csv (término | primera aparición | dónde se
define | tipo de definición) y termina con código 1 si algún término se usa antes
de definirse.  Uso (desde la raíz del proyecto):
    python3 sesiones/S01/verificaciones/verificar_terminologia_s01.py
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "sesiones/S01/contenido_libro.tex"
lineas = SRC.read_text(encoding="utf-8").split("\n")
texto = [("" if l.lstrip().startswith("%") else re.sub(r"(?<!\\)%.*", "", l)) for l in lineas]
# Los encabezados anuncian el tema que se define a continuación: no cuentan como
# uso (la Regla 1 enumera resultados, ejemplos, figuras, tablas, comentarios y
# diapositivas). Sí cuentan como lugar de definición si la regex lo indica.
ENCAB = re.compile(r"^\s*\\(subsection|subsubsection|paragraph|complemento)\b")
uso_texto = [("" if ENCAB.match(l) else l) for l in texto]

ini_tabla = next(i for i, l in enumerate(texto, 1) if r"\label{s01:notacion}" in l)
fin_tabla = next(i for i, l in enumerate(texto, 1) if i > ini_tabla and re.search(r"\\end\{(longtable|tabularx)\}", l))

# (término, regex de uso, regex de definición, tipo, en_tabla)
TERMINOS = [
    ("LLM", r"\bLLM\b", r"\(Large Language Model, LLM\)", "operativa", False),
    ("$n$-grama", r"\$n\$-grama", r"Llamaremos \\emph\{modelo de \$n\$-gramas\}", "operativa; formal en Def. Markov", True),
    ("token / tokenización", r"(?<![\[,])\btokens?\b(?!/\.style|\])|tokenizaci", r"Un \\emph\{token\} es una unidad", "operativa; formal en Def. vocabulario", False),
    ("vocabulario $V$, $|V|$", r"\|V\|", r"vocabulario \$V\$ de tamaño", "operativa; formal en Def. vocabulario", True),
    ("one-hot, $e_i$", r"one-hot", r"\\emph\{codificación one-hot\}", "operativa (formal: $e_i$ canónico)", True),
    ("embedding", r"\bembedding", r"Un \\emph\{embedding\} asignaría", "operativa (formal en S02)", True),
    ("BPE", r"\bBPE\b", r"\(Byte Pair Encoding, BPE\)", "formal (Def. s01:def:bpe)", False),
    ("MLE / máxima verosimilitud", r"\bMLE\b|máxima verosimilitud", r"\(maximum likelihood estimation, MLE\)", "operativa; formal Prop. s01:prop:mle", False),
    ("suavizado / pseudoconteo", r"suavizado", r"motiva el \\emph\{suavizado\}", "operativa", False),
    ("regla de la cadena", r"regla de la cadena", r"\\begin\{proposicion\}\[Regla de la cadena\]", "formal (Prop. s01:prop:cadena)", False),
    ("independencia condicional, $\\perp$", r"\\perp\b|condicionalmente independientes|independencia condicional", r"\\begin\{definicion\}\[Independencia condicional\]", "formal (Def. s01:def:ci)", False),
    ("hipótesis de Markov de orden $m$", r"Markov de orden|hipótesis de Markov", r"\\begin\{definicion\}\[Hipótesis de Markov", "formal (Def. s01:def:markov)", False),
    ("símplex / soporte", r"símplex|\\operatorname\{supp\}", r"\\begin\{definicion\}\[Símplex y soporte\]", "formal (Def. s01:def:simplex)", True),
    ("retroceso (backoff)", r"retroceso", r"\\emph\{retroceso\} \(backoff\)", "operativa", False),
    ("distribución a priori", r"a priori|\bprior", r"distribución \\emph\{a priori\}", "operativa", False),
    ("función Gamma $\\Gamma$", r"\\Gamma", r"\\begin\{definicion\}\[Función Gamma\]", "formal (Def. s01:def:gamma)", True),
    ("Dirichlet", r"Dirichlet", r"\\begin\{definicion\}\[Distribución de Dirichlet\]", "formal (Def. s01:def:dirichlet)", False),
    ("teorema de Bayes (densidades)", r"Bayes", r"\\begin\{teorema\}\[Bayes", "formal (Teo. s01:teo:bayes)", False),
    ("sorpresa / bit", r"sorpresa|\bbits?\b", r"\\emph\{sorpresa\} \(o autoinformación\)", "operativa", True),
    ("entropía $H_2$, $H_e$", r"entropía|\bH_2\b|H_e\b", r"La \\emph\{entropía\} \$H_2\(X\)", "operativa; formal l. de $H_2(p)$", True),
    ("nat", r"\bnats?\b", r"se obtiene la unidad \\emph\{nat\}", "operativa", True),
    ("entropía condicional / información mutua", r"información mutua|H\(X\\mid Y\)|I\(X;Y\)", r"\\begin\{definicion\}\[Entropías de dos variables", "formal (Def. s01:def:condicional)", True),
    ("entropía cruzada / KL", r"entropía cruzada|D_\{\\(?:rm|mathrm)\{?\s?KL|\bKL\b", r"\\begin\{definicion\}\[Entropía cruzada y divergencia", "formal (Def. s01:def:kl)", True),
    ("soportes compatibles", r"soportes compatibles", r"Decimos que tienen \\emph\{soportes compatibles\}", "formal (Def. s01:def:kl)", False),
    ("perplejidad / PPL", r"perplejidad|\bPPL\b", r"definimos la \\emph\{perplejidad\} \(perplexity, PPL\)", "formal", True),
    ("BPC", r"\bBPC\b|bits por carácter", r"\\begin\{definicion\}\[Bits por carácter\]", "formal (Def. s01:def:bpc)", True),
    ("BOS / EOS", r"\bBOS\b|\bEOS\b", r"\(beginning of sequence, BOS\)", "operativa", True),
    ("bootstrap / intervalo percentil", r"bootstrap|intervalo percentil", r"usamos el \\emph\{bootstrap\}", "operativa; formal Def. s01:def:bootstrap", True),
    ("IC10", r"\bIC10\b", r"IC10 es el código, en la matriz de investigación", "operativa", False),
    ("D01, D02", r"\bD0[12]\b", r"D01 \(Wikipedia en español\)", "operativa", False),
    ("desigualdad de Jensen", r"Jensen(?!--Shannon)", r"Usamos la \\emph\{desigualdad de Jensen\}", "enunciado con remisión; formal Lema s01:lem:jensen", False),
    ("desigualdad de Gibbs", r"Gibbs", r"es la \\emph\{desigualdad de Gibbs\}", "enunciado con remisión; formal Teo. s01:teo:gibbs", False),
    ("condiciones KKT", r"KKT|Karush", r"\(condiciones de Karush--Kuhn--Tucker\)", "operativa; formal Teo. s01:teo:kkt", False),
    ("suma logarítmica", r"suma logarítmica", r"\\paragraph\{La desigualdad de la suma logarítmica\}", "formal (Lema s01:lem:sumalog)", False),
    ("distribución estacionaria", r"estacionaria", r"\\emph\{distribución estacionaria\}", "formal (C9)", True),
    ("tasa de entropía $H_\\infty$", r"tasa de entropía|H_\\infty", r"\\begin\{proposicion\}\[Tasa de entropía\]", "formal (Prop. s01:prop:tasa)", True),
    ("desigualdad de Kraft", r"Kraft", r"\\emph\{desigualdad de Kraft\}: existe", "operativa con referencia", False),
]


def primera(regex, desde=1, fuente=None):
    for i, l in enumerate(fuente or texto, 1):
        if i >= desde and re.search(regex, l):
            return i
    return None


registro, fallos = [], []
for nombre, uso, defi, tipo, en_tabla in TERMINOS:
    u = primera(uso, fuente=uso_texto)
    d = primera(defi)
    if en_tabla:
        cand = [x for x in (ini_tabla if any(re.search(uso, l) for l in texto[ini_tabla - 1:fin_tabla]) else None, d) if x]
        d_ef = min(cand) if cand else None
        donde = (f"tabla de notación l. {ini_tabla}–{fin_tabla}" if d_ef == ini_tabla else f"l. {d}") + (f"; l. {d}" if d and d_ef == ini_tabla else "")
    else:
        d_ef, donde = d, (f"l. {d}" if d else "NO ENCONTRADA")
    if u is None:
        estado = "sin uso"
    elif d_ef is None:
        estado = "SIN DEFINICIÓN"
    elif u < d_ef and not (d_ef <= u):
        estado = "USO ANTES DE DEFINIR"
    else:
        estado = "ok"
    if estado not in ("ok", "sin uso"):
        fallos.append(f"{nombre}: uso l. {u}, definición {donde} -> {estado}")
    registro.append([nombre, f"l. {u}" if u else "—", donde, tipo, estado])

salida = ROOT / "sesiones/S01/verificaciones/REGISTRO_TERMINOLOGIA_S01.csv"
with salida.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["término", "primera aparición", "dónde se define", "tipo de definición", "estado"])
    w.writerows(registro)
for fila in registro:
    print(f"{fila[4]:22s} {fila[0]:45s} uso {fila[1]:8s} def {fila[2]}")
print(f"\n{len(fallos)} problema(s)")
for x in fallos:
    print("  " + x)
sys.exit(1 if fallos else 0)

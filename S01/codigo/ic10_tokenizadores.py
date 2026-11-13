"""S01 / IC10: microexperimento didáctico con BPE de palabras.
Corpus sintético. Contrasta tokenizadores, NO calidad predictiva ni LLM.
Se respetan las particiones: solo entrenamiento para aprender fusiones.
"""
from collections import Counter
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'experimentos' / 'corpus_didactico.csv'
OUT = ROOT / 'experimentos'
M = 20
END = '</w>'

def words(s):
    return s.strip().lower().split()

def initialize(texts):
    freq = Counter(w for t in texts for w in words(t))
    return {w: (tuple(w) + (END,), n) for w, n in freq.items()}

def replace_pair(symbols, pair):
    out=[]; i=0
    while i < len(symbols):
        if i+1 < len(symbols) and (symbols[i],symbols[i+1])==pair:
            out.append(symbols[i]+symbols[i+1]); i+=2
        else:
            out.append(symbols[i]); i+=1
    return tuple(out)

def train(texts, budget=M):
    vocab=initialize(texts)
    learned=[]
    for _ in range(budget):
        pairs=Counter()
        for symbols,n in vocab.values():
            for pair in zip(symbols,symbols[1:]): pairs[pair]+=n
        if not pairs: break
        best=min((pair for pair,f in pairs.items() if f==max(pairs.values())))
        # Escoger el par mas frecuente; si hay empate, orden lexicografico Unicode.
        vocab={w:(replace_pair(sym,best),n) for w,(sym,n) in vocab.items()}
        learned.append((best[0],best[1],pairs[best]))
    return learned

def tokenize(w, learned):
    symbols=tuple(w)+(END,)
    for a,b,_ in learned: symbols=replace_pair(symbols,(a,b))
    return symbols

def count_text(t,learned):
    tokens=[tokenize(w,learned) for w in words(t)]
    return sum(len(x) for x in tokens), len(tokens)

def main():
    with DATA.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    general=[r['texto'] for r in rows if r['grupo']=='general' and r['particion']=='entrenamiento']
    tecnico=[r['texto'] for r in rows if r['grupo']=='tecnico' and r['particion']=='entrenamiento']
    test=[r for r in rows if r['particion']=='prueba']
    assert len(general)==len(tecnico)==8 and len(test)==6
    merges={'general':train(general),'tecnico':train(tecnico)}
    assert len(merges['general'])==len(merges['tecnico'])==M
    assert len(set(r['id'] for r in test))==len(test)
    result=[]
    for r in test:
        ng,w=count_text(r['texto'],merges['general'])
        nt,wt=count_text(r['texto'],merges['tecnico'])
        assert w==wt and w>0
        result.append({'id':r['id'],'palabras':w,'tokens_bpe_general':ng,'tokens_bpe_tecnico':nt,'tokens_por_palabra_general':round(ng/w,6),'tokens_por_palabra_tecnico':round(nt/w,6),'diferencia_tokens_por_palabra':round((nt-ng)/w,6)})
    names=list(result[0].keys())
    with (OUT/'resultados_ic10_tokenizacion.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=names);writer.writeheader();writer.writerows(result)
    summary={'datos':'SINTETICOS_DIDACTICOS','pregunta':'cambiar entrenamiento del tokenizador con igual numero de fusiones','tipo':'BPE didactico por palabras con marcador </w>','presupuesto_fusiones':M,'numero_documentos_prueba':len(test),'palabras_prueba':sum(r['palabras'] for r in result), 'tokens_general_total':sum(r['tokens_bpe_general'] for r in result),'tokens_tecnico_total':sum(r['tokens_bpe_tecnico'] for r in result),'razon_tokens_por_palabra_general':round(sum(r['tokens_bpe_general'] for r in result)/sum(r['palabras'] for r in result),6),'razon_tokens_por_palabra_tecnico':round(sum(r['tokens_bpe_tecnico'] for r in result)/sum(r['palabras'] for r in result),6),'conclusion':'NO hay medida de BPC predictiva ni prueba de generalizacion, solo longitud tokenizada','separacion':'aprendizaje de fusiones solo en entrenamiento','desempate':'orden lexicografico Unicode de pares','normalizacion':'strip, lower, split sobre espacios; no se eliminaron acentos','marcador_final':END}
    (OUT/'resumen_ic10_tokenizacion.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'fusiones_ic10.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['origen','paso','izquierda','derecha','frecuencia'])
        for origen,arr in merges.items():
            for i,(a,b,freq) in enumerate(arr,1):writer.writerow([origen,i,a,b,freq])
    assert sum(r['tokens_bpe_general'] for r in result)>0
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return result,summary
if __name__=='__main__':main()

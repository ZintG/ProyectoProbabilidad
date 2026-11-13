"""S01: experimento didactico PAREADO, con datos fabricados (NO Q1).
Unidades: puntos de codigo Unicode, minúsculas, probabilidades incluyen EOS.
Los simbolos posibles se fijan SOLO desde los conjuntos de entrenamiento.
La variable de contraste es BPC(tecnico) - BPC(general) por documento.
La distribucion bootstrap se enumera exactamente para n<=7 (n**n muestras).
No usar como afirmacion empirica de desempeño de modelos reales.
"""
from __future__ import annotations
import csv, itertools, json, math, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'experimentos'/'corpus_didactico.csv'
OUT=ROOT/'experimentos'/'resultados_python.csv'
ALPHA=1.0
BOS='^'
EOS='$'

def normalizar(s):
    return s.strip().lower()

def ajustar(textos, vocabulario, alpha=ALPHA):
    pred = tuple(vocabulario)+(EOS,)
    ctx = tuple(vocabulario)+(BOS,)
    C={a:{b:0 for b in pred} for a in ctx}
    for text in textos:
        anterior=BOS
        for s in (*text,EOS):
            if s not in pred: raise ValueError('caracter fuera del vocabulario de entrenamiento: '+repr(s))
            C[anterior][s]+=1
            anterior=s
    P={a:{b:(C[a][b]+alpha)/(sum(C[a].values())+alpha*len(pred)) for b in pred} for a in ctx}
    assert all(abs(sum(fila.values())-1)<1e-12 for fila in P.values())
    return P

def bits(text,P):
    anterior=BOS; total=0.0
    for ch in (*text,EOS):
        if ch not in P[anterior]: raise ValueError('fuera de vocabulario '+repr(ch))
        total-=math.log2(P[anterior][ch]); anterior=ch
    return total

def cuantiles(valores,probs=(.025,.975)):
    s=sorted(valores)
    def q(p):
        h=(len(s)-1)*p; lo=int(h); hi=min(lo+1,len(s)-1)
        return s[lo]+(h-lo)*(s[hi]-s[lo])
    return [q(p) for p in probs]

def bootstrap_exacto(deltas):
    n=len(deltas)
    if n>7: raise ValueError('enumeracion solo para un piloto pequeno')
    valores=(sum(deltas[i] for i in combo)/n for combo in itertools.product(range(n), repeat=n))
    return cuantiles(valores)

def main():
    with DATA.open(newline='',encoding='utf-8') as f: registros=list(csv.DictReader(f))
    general=[normalizar(x['texto']) for x in registros if x['grupo']=='general' and x['particion']=='entrenamiento']
    tecnico=[normalizar(x['texto']) for x in registros if x['grupo']=='tecnico' and x['particion']=='entrenamiento']
    prueba=[(x['id'],normalizar(x['texto'])) for x in registros if x['particion']=='prueba']
    assert len(general)==len(tecnico)==8 and len(prueba)==6
    vocab=tuple(sorted(set(''.join(general+tecnico))))
    assert not (set(''.join(s for _,s in prueba))-set(vocab)), 'prueba tiene caracteres desconocidos'
    pg=ajustar(general,vocab); pt=ajustar(tecnico,vocab)
    resultados=[]
    for clave,text in prueba:
        bpc_g=bits(text,pg)/len(text)
        bpc_t=bits(text,pt)/len(text)
        resultados.append({'id':clave,'caracteres':len(text),'bpc_general':round(bpc_g,8),'bpc_tecnico':round(bpc_t,8),'delta_bpc':round(bpc_t-bpc_g,8)})
    delta=[r['delta_bpc'] for r in resultados]
    ci=bootstrap_exacto(delta)
    # Se evita test de significacion con datos inventados.
    OUT.parent.mkdir(exist_ok=True,parents=True)
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=resultados[0].keys()); w.writeheader(); w.writerows(resultados)
    resumen={'datos':'SINTETICOS_CREADOS_PARA_ENSENAR','modelo':'bigrama_caracter_alpha_1','n_prueba':len(prueba), 'vocabulario_entrenamiento':len(vocab), 'delta_promedio_bpc':round(statistics.mean(delta),8), 'ic_percentil_bootstrap_pareado_95':[round(x,8) for x in ci], 'bootstrap':'enumeracion_exhaustiva_n^n','decision':'SIN_INFERENCIA_POBLACIONAL','normalizacion':'minúsculas y recorte de extremos (corpus UTF-8 precompuesto)','unidad':'puntos_de_codigo_unicode','probabilidad':'cada documento incluye BOS y EOS; BPC divide por longitud sin EOS'}
    (ROOT/'experimentos'/'resumen_python.json').write_text(json.dumps(resumen,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(resumen,ensure_ascii=False,indent=2))
    return resultados,resumen
if __name__=='__main__': main()

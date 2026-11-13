"""Compara resultados generados por R y Python; no genera ni falsifica resultados R.
Uso: python verificaciones/comparar_r_python.py
"""
import csv, math
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'experimentos'

def read(name):
    with (P/name).open(encoding='utf8',newline='') as f: return {x['id']:x for x in csv.DictReader(f)}

def compare(a,b,keys,tolerance=2e-6):
    assert set(a)==set(b),(set(a),set(b))
    max_abs=0.0
    for ident in a:
        for key in keys:
            d=abs(float(a[ident][key])-float(b[ident][key]));max_abs=max(d,max_abs)
            if d>tolerance:raise AssertionError(f'{ident} {key}: {a[ident][key]} frente a {b[ident][key]}, diferencia {d}')
    return max_abs

def main():
    if not (P/'resultados_R.csv').exists() or not (P/'resultados_ic10_R.csv').exists():
        print('PENDIENTE: ejecute Rscript codigo/experimento_s01.R y Rscript codigo/ic10_tokenizadores.R; no se certifica equivalencia R/Python.')
        return 2
    a=compare(read('resultados_python.csv'),read('resultados_R.csv'),['caracteres','bpc_general','bpc_tecnico','delta_bpc'])
    b=compare(read('resultados_ic10_tokenizacion.csv'),read('resultados_ic10_R.csv'),['palabras','tokens_bpe_general','tokens_bpe_tecnico','tokens_por_palabra_general','tokens_por_palabra_tecnico','diferencia_tokens_por_palabra'])
    print(f'OK: concordancia por documento. Desviaciones maximas BPC={a:.8g}, BPE={b:.8g}')
    return 0
if __name__=='__main__':raise SystemExit(main())

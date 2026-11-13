# v0.9: este verificador exige material docente (s01_docente.tex, sol01.pdf, solej01.pdf) y
# por eso falla en el paquete del estudiante. Usar verificaciones/verificar_s01_estudiante.py.
"""Comprobaciones del piloto S01 v0.5; no ejecuta R."""
from pathlib import Path
import csv, json, math, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'codigo'/'experimento_s01.py')],check=True,capture_output=True,text=True)
r=list(csv.DictReader((ROOT/'experimentos'/'resultados_python.csv').open(encoding='utf-8')))
j=json.loads((ROOT/'experimentos'/'resumen_python.json').read_text(encoding='utf-8'))
assert len(r)==j['n_prueba']==6
assert all(int(v['caracteres'])>0 and float(v['bpc_general'])>0 and float(v['bpc_tecnico'])>0 for v in r)
assert math.isclose(sum(float(v['delta_bpc']) for v in r)/6,j['delta_promedio_bpc'],abs_tol=1e-8)
assert math.isclose(j['delta_promedio_bpc'],-0.54024842,abs_tol=1e-8)
assert all(math.isclose(g,e,abs_tol=1e-8) for g,e in zip(j['ic_percentil_bootstrap_pareado_95'],[-0.66770598,-0.42038147]))
assert j['datos']=='SINTETICOS_CREADOS_PARA_ENSENAR'
for f in ('s01_integrada.tex','s01_docente.tex','modulos/20_laboratorio_matematico.tex','modulos/30_laboratorio_computacional.tex','modulos/40_investigacion_y_q1.tex','modulos/50_taller_contenido.tex','modulos/60_suplemento_contenido.tex','reportes/reporte_s01.tex'):
    assert (ROOT/f).exists(),f
for f in ('s01_integrada','s01_docente','labmat01','labcomp01','t01','p01','sup01','ej01','sol01','solej01','reporte_s01','reporte_ejemplo_ejecutado'):
    p=ROOT/'pdf'/f'{f}.pdf'
    assert p.exists() and p.stat().st_size>4000, str(p)
print('S01 v0.5 verificaciones satisfactoria: fuente, corpus, BPC, bootstrap, PDF')

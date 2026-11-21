#!/usr/bin/env python3
"""codigo/experimentos.py

Ejecuta las Fases 1 a 6 del Proyecto de Probabilidad y asegura que todas las
tablas (.csv) y figuras (.png y .pdf) requeridas por el enunciado queden escritas
en la carpeta resultados/ (y sincronizadas con tablas/ y figuras/).

Uso desde la raíz del proyecto:
    python3 codigo/experimentos.py

Opciones:
    --forzar           Fuerza la reevaluación de la Fase 4 (NO recomendado)
    --verificar        Ejecuta además la verificación de las 127 cifras al finalizar
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CODIGO = BASE_DIR / "codigo"
DIR_RESULTADOS = BASE_DIR / "resultados"
DIR_TABLAS = BASE_DIR / "tablas" if (BASE_DIR / "tablas").exists() else DIR_RESULTADOS
DIR_FIGURAS = BASE_DIR / "figuras" if (BASE_DIR / "figuras").exists() else DIR_RESULTADOS
T3_TABLA = DIR_TABLAS / "T3_evaluacion_prueba.csv"
T3_RESULTADO = DIR_RESULTADOS / "T3_evaluacion_prueba.csv"

FASES = [
    ("fase1.py", "Fase 1: Frecuencias, T1 y F1"),
    ("fase2.py", "Fase 2: Ceros de la MLE y T2"),
    ("fase3.py", "Fase 3: Calibración de alpha y F2"),
    ("fase4.py", "Fase 4: Evaluación única en prueba, T3, Gibbs, F3 y F4"),
    ("fase5.py", "Fase 5: Simulación de Markov, distribución estacionaria pi y F5"),
    ("fase6.py", "Fase 6: Bootstrap por bloques, T4 y figura delta"),
]


def sincronizar_resultados():
    """Copia todas las tablas y figuras a resultados/ si provienen de carpetas separadas."""
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    
    # Copiar tablas CSV si no estaban ya en resultados/
    if DIR_TABLAS != DIR_RESULTADOS and DIR_TABLAS.exists():
        for archivo in DIR_TABLAS.glob("*.csv"):
            shutil.copy2(archivo, DIR_RESULTADOS / archivo.name)
            
    # Copiar figuras PNG y PDF si no estaban ya en resultados/
    if DIR_FIGURAS != DIR_RESULTADOS and DIR_FIGURAS.exists():
        for patron in ("*.png", "*.pdf"):
            for archivo in DIR_FIGURAS.glob(patron):
                shutil.copy2(archivo, DIR_RESULTADOS / archivo.name)


def ejecutar_script(script: str, descripcion: str, argumentos: list = None) -> float:
    """Ejecuta un script y devuelve el tiempo transcurrido en segundos."""
    ruta = CODIGO / script
    cmd = [sys.executable, str(ruta)]
    if argumentos:
        cmd.extend(argumentos)

    print("\n" + "=" * 72)
    print(f"EJECUTANDO: {descripcion}")
    print(f"Orden: python3 codigo/{script}{' ' + ' '.join(argumentos) if argumentos else ''}")
    print("=" * 72, flush=True)

    inicio = time.perf_counter()
    subprocess.run(cmd, cwd=BASE_DIR, check=True)
    elapsed = time.perf_counter() - inicio

    print(f"--> {descripcion}: {elapsed:.2f} s", flush=True)
    return elapsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta las Fases 1 a 6 y genera los resultados del reporte."
    )
    parser.add_argument(
        "--forzar", action="store_true",
        help="forzar reevaluación de la fase 4 en el conjunto de prueba",
    )
    parser.add_argument(
        "--verificar", action="store_true",
        help="ejecutar verificar_todo.py al finalizar las fases",
    )
    args = parser.parse_args()

    inicio_total = time.perf_counter()
    print("=" * 72)
    print("PROYECTO DE PROBABILIDAD · FASES 1 A 6 (EXPERIMENTOS)")
    print("=" * 72)
    print(f"Directorio base: {BASE_DIR}")
    print(f"Directorio de resultados: {DIR_RESULTADOS}")

    t3_existe = T3_TABLA.exists() or T3_RESULTADO.exists()
    if t3_existe and not args.forzar:
        print("\nAVISO: T3_evaluacion_prueba.csv ya existe.")
        print("La prueba se evaluó una sola vez. Se omite fase4.py para preservar")
        print("las cifras congeladas (protocolo de evaluación honesta).")

    tiempos = []
    for script, desc in FASES:
        if script == "fase4.py" and t3_existe and not args.forzar:
            print("\n" + "-" * 72)
            print(f"OMITIDA: {desc} (resultado congelado)")
            print("-" * 72)
            continue

        extra_args = ["--forzar"] if (script == "fase4.py" and args.forzar) else None
        t = ejecutar_script(script, desc, extra_args)
        tiempos.append((script, desc, t))

    # Sincronizar todos los artefactos a resultados/
    print("\nSincronizando tablas y figuras hacia resultados/...")
    sincronizar_resultados()
    print(f"Archivos en resultados/: {len(list(DIR_RESULTADOS.iterdir()))}")

    if args.verificar:
        t_verif = ejecutar_script("verificar_todo.py", "Verificación de 127 cifras")
        tiempos.append(("verificar_todo.py", "Verificación", t_verif))

    total = time.perf_counter() - inicio_total
    print("\n" + "=" * 72)
    print("RESUMEN DE EXPERIMENTOS")
    print("=" * 72)
    for script, desc, seg in tiempos:
        print(f"  {script:<18} {seg:8.2f} s   {desc}")
    print("-" * 72)
    print(f"  TIEMPO TOTAL: {total:.2f} s ({total / 60:.2f} min)")
    print("=" * 72)
    print("¡EXPERIMENTOS COMPLETADOS EXITOSAMENTE!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

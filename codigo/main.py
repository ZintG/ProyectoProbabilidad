#!/usr/bin/env python3
"""codigo/main.py

Ejecuta de principio a fin el flujo del Proyecto de Probabilidad desde una
sola orden, en este orden:

    preparar.py -> pruebas.py -> fase1.py -> fase2.py -> fase3.py
    -> fase4.py -> fase5.py -> fase6.py -> verificar_todo.py

La evaluación oficial en prueba se ejecuta una sola vez: si ya existe
``tablas/T3_evaluacion_prueba.csv``, ``fase4.py`` se omite y se conserva el
resultado congelado. Nunca se usa ``--forzar``.

Uso, desde la raíz del repositorio:

    python3 codigo/main.py

Opciones:

    --max-segundos N   límite de tiempo para la verificación (por defecto, 600)
    --sin-limite       mide el tiempo pero no falla si se supera el límite

La salida incluye el tiempo de cada etapa y el total, para comprobar el
requisito de que el flujo completo corre en menos de 10 minutos.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CODIGO = BASE_DIR / "codigo"
T3 = BASE_DIR / "tablas" / "T3_evaluacion_prueba.csv"

ETAPAS = [
    ("preparar.py", "Corpus: limpieza, normalización y partición"),
    ("pruebas.py", "Prueba de cordura con abracadabra"),
    ("fase1.py", "Fase 1: frecuencias, T1 y F1"),
    ("fase2.py", "Fase 2: ceros de la MLE y T2"),
    ("fase3.py", "Fase 3: calibración de alpha y F2"),
    ("fase4.py", "Fase 4: evaluación única, T3, Gibbs, F3 y F4"),
    ("fase5.py", "Fase 5: simulación, pi y F5"),
    ("fase6.py", "Fase 6: bootstrap y T4"),
    ("verificar_todo.py", "Verificación interna de las 127 cifras"),
]


def ejecutar(script: str, descripcion: str) -> float:
    """Ejecuta un script y devuelve los segundos que tardó."""
    ruta = CODIGO / script
    print("\n" + "=" * 72)
    print(f"ETAPA: {descripcion}")
    print(f"Orden: python3 codigo/{script}")
    print("=" * 72, flush=True)

    inicio = time.perf_counter()
    subprocess.run([sys.executable, str(ruta)], cwd=BASE_DIR, check=True)
    elapsed = time.perf_counter() - inicio

    print(f"--> {descripcion}: {elapsed:.2f} s", flush=True)
    return elapsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta el flujo completo del proyecto y mide su duración."
    )
    parser.add_argument(
        "--max-segundos", type=float, default=600.0,
        help="límite de tiempo en segundos (por defecto, 600 = 10 minutos)",
    )
    parser.add_argument(
        "--sin-limite", action="store_true",
        help="medir el tiempo sin fallar si se supera el límite",
    )
    args = parser.parse_args()

    inicio_total = time.perf_counter()
    tiempos = []

    print("=" * 72)
    print("PROYECTO DE PROBABILIDAD · FLUJO COMPLETO")
    print("=" * 72)
    print(f"Raíz del proyecto: {BASE_DIR}")
    print(f"Etapas previstas: {len(ETAPAS)}")
    print(f"Límite de tiempo: {'desactivado' if args.sin_limite else f'{args.max_segundos:.0f} s'}")

    if T3.exists():
        print("\nAVISO: tablas/T3_evaluacion_prueba.csv ya existe.")
        print("La prueba se evaluó una sola vez: se omite fase4.py y se")
        print("conservan T3, T3_gibbs.csv, F3 y F4 tal como están.")

    for script, descripcion in ETAPAS:
        if script == "fase4.py" and T3.exists():
            print("\n" + "-" * 72)
            print(f"ETAPA OMITIDA: {descripcion} (evaluación única ya realizada)")
            print("-" * 72, flush=True)
            continue
        if not (CODIGO / script).exists():
            print(f"\nERROR: no existe codigo/{script}", file=sys.stderr)
            return 1
        tiempos.append(ejecutar(script, descripcion))

    total = time.perf_counter() - inicio_total
    print("\n" + "=" * 72)
    print("RESUMEN")
    print("=" * 72)
    for (script, descripcion), segundos in zip(
        [e for e in ETAPAS if not (e[0] == "fase4.py" and T3.exists())],
        tiempos,
    ):
        print(f"  {script:<20} {segundos:8.2f} s   {descripcion}")
    print("-" * 72)
    print(f"  TIEMPO TOTAL: {total:.2f} s ({total / 60:.2f} min)")

    if T3.exists():
        print("  Evaluación en prueba: no repetida (resultado congelado).")

    if total > args.max_segundos and not args.sin_limite:
        print(
            f"\nERROR: el flujo tardó {total:.2f} s y supera el límite "
            f"de {args.max_segundos:.0f} s.",
            file=sys.stderr,
        )
        return 1

    print("\nFLUJO COMPLETADO CORRECTAMENTE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

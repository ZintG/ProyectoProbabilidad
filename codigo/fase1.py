#!/usr/bin/env python3
"""codigo/fase1.py
Fase 1: Exploración del corpus, conteos de unigramas, cálculo de entropías
y generación de la Tabla T1 y la Gráfica F1.
"""

from collections import Counter
import math
import os
from pathlib import Path
import matplotlib.pyplot as plt

# 1. Definición de rutas del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]
DIR_DATOS = BASE_DIR / "datos"
DIR_RESULTADOS = BASE_DIR / "resultados"
DIR_FIGURAS = BASE_DIR / "figuras" if (BASE_DIR / "figuras").exists() else DIR_RESULTADOS
DIR_TABLAS = BASE_DIR / "tablas" if (BASE_DIR / "tablas").exists() else DIR_RESULTADOS

# Asegurar que existan las carpetas de salida
DIR_FIGURAS.mkdir(exist_ok=True)
DIR_TABLAS.mkdir(exist_ok=True)


def main():
    print("=" * 65)
    print("      FASE 1: EXPLORACIÓN DEL CORPUS Y ANÁLISIS DE ENTROPÍA")
    print("=" * 65)

    # 2. Cargar las tres particiones
    ruta_ent = DIR_DATOS / "entrenamiento.txt"
    ruta_val = DIR_DATOS / "validacion.txt"
    ruta_pru = DIR_DATOS / "prueba.txt"

    with open(ruta_ent, "r", encoding="utf-8") as f:
        texto_ent = f.read()
    with open(ruta_val, "r", encoding="utf-8") as f:
        texto_val = f.read()
    with open(ruta_pru, "r", encoding="utf-8") as f:
        texto_pru = f.read()

    n_ent = len(texto_ent)
    n_val = len(texto_val)
    n_pru = len(texto_pru)
    n_total = n_ent + n_val + n_pru

    # 3. Conteos del vocabulario en Entrenamiento
    conteos = Counter(texto_ent)
    vocabulario = sorted(list(conteos.keys()))
    tam_v = len(vocabulario)

    # =========================================================================
    # TABLA T1: TAMAÑO DE PARTICIONES Y VOCABULARIO
    # =========================================================================
    print("\n--- TABLA T1: PARTICIONES Y TAMAÑO DEL VOCABULARIO ---")
    print(
        f"{'Partición':<16} | {'Caracteres':<12} | {'Porcentaje':<10} | {'Propósito'}"
    )
    print("-" * 65)
    print(
        f"{'Entrenamiento':<16} | {n_ent:<12} | {n_ent/n_total*100:>6.2f} %   | Aprendizaje de frecuencias"
    )
    print(
        f"{'Validación':<16} | {n_val:<12} | {n_val/n_total*100:>6.2f} %   | Calibración de alfa"
    )
    print(
        f"{'Prueba':<16} | {n_pru:<12} | {n_pru/n_total*100:>6.2f} %   | Examen final (1 sola vez)"
    )
    print("-" * 65)
    print(f"{'TOTAL':<16} | {n_total:<12} | 100.00 %   | Libro Niebla limpio")
    print(f"Tamaño del Vocabulario (|V|): {tam_v} caracteres\n")

    # Guardar T1 en CSV para el informe
    with open(DIR_TABLAS / "T1_particiones.csv", "w", encoding="utf-8") as f:
        f.write("Particion,Caracteres,Porcentaje\n")
        f.write(f"Entrenamiento,{n_ent},{n_ent/n_total*100:.2f}\n")
        f.write(f"Validacion,{n_val},{n_val/n_total*100:.2f}\n")
        f.write(f"Prueba,{n_pru},{n_pru/n_total*100:.2f}\n")
        f.write(f"Total,{n_total},100.00\n")

    # =========================================================================
    # CÁLCULO DE ENTROPÍA EMPÍRICA Y MÁXIMA
    # =========================================================================
    # Ordenar símbolos de mayor a menor frecuencia
    ordenados = conteos.most_common()

    # H(p̂) = - sum( p(x) * log2(p(x)) )
    h_empirica = 0.0
    for char, c in ordenados:
        p_x = c / n_ent
        h_empirica -= p_x * math.log2(p_x)

    # H_max = log2(|V|)
    h_max = math.log2(tam_v)

    diferencia_bits = h_max - h_empirica
    redundancia = (1.0 - (h_empirica / h_max)) * 100.0

    print("--- RESULTADOS DE ENTROPÍA ---")
    print(f"Entropía empírica de unigramas H(p̂) : {h_empirica:.4f} bits")
    print(
        f"Entropía máxima teórica log2(|V|)     : {h_max:.4f} bits (con |V| = {tam_v})"
    )
    print(f"Diferencia (ganancia de certeza)    : {diferencia_bits:.4f} bits")
    print(f"Redundancia del español (R)         : {redundancia:.2f} %\n")

    # =========================================================================
    # GRÁFICA F1: DISTRIBUCIÓN DE FRECUENCIAS DE SÍMBOLOS
    # =========================================================================
    simbolos_etiquetas = []
    frecuencias_relativas = []

    for char, count in ordenados:
        # Etiqueta legible para el espacio y numeral
        if char == " ":
            etiqueta = "[esp]"
        elif char == "#":
            etiqueta = "#"
        else:
            etiqueta = char
        simbolos_etiquetas.append(etiqueta)
        frecuencias_relativas.append(count / n_ent)

    # Crear la figura con estilo limpio y profesional
    plt.figure(figsize=(11, 5))
    barras = plt.bar(
        simbolos_etiquetas,
        frecuencias_relativas,
        color="#2b5c8f",
        edgecolor="#1a365d",
    )

    plt.title(
        f"Gráfica F1: Frecuencias de Símbolos en Entrenamiento (N = {n_ent:,})",
        fontsize=13,
        fontweight="bold",
    )
    plt.xlabel("Símbolo (ordenado de mayor a menor)", fontsize=11)
    plt.ylabel("Frecuencia Relativa p̂(x)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Guardar en PDF y PNG para LaTeX
    ruta_fig_png = DIR_FIGURAS / "F1_frecuencias.png"
    ruta_fig_pdf = DIR_FIGURAS / "F1_frecuencias.pdf"
    plt.savefig(ruta_fig_png, dpi=300)
    plt.savefig(ruta_fig_pdf)
    plt.close()

    print("--- ARCHIVOS GENERADOS CON ÉXITO ---")
    print(f"✔ Gráfica F1 guardada en : {ruta_fig_png}")
    print(f"✔ Gráfica F1 (vectorial): {ruta_fig_pdf}")
    print(f"✔ Tabla T1 guardada en   : {DIR_TABLAS / 'T1_particiones.csv'}")
    print("=" * 65)


if __name__ == "__main__":
    main()
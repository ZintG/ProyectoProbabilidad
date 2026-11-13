#!/usr/bin/env python3
"""codigo/preparar.py
Lectura, limpieza editorial, normalización y partición contigua 80/10/10
del libro "Niebla" de Miguel de Unamuno para el Proyecto de Probabilidad.
"""

import re
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_ENTRADA = BASE_DIR / "libro" / "Niebla_limpio.txt"
DIR_DATOS = BASE_DIR / "datos"

# Alfabeto permitido: 26 letras en inglés más el espacio en blanco
ALFABETO_PERMITIDO = set("abcdefghijklmnopqrstuvwxyz ")
SIMBOLO_ESPECIAL = "#"


def cargar_texto(ruta_archivo: Path) -> str:
    """Lee el archivo de texto en formato UTF-8."""
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        return f.read()


def recortar_paratexto_editorial(texto: str) -> str:
    """Elimina notas del digitalizador al inicio y el índice de páginas al final.
    Conserva exclusivamente la obra literaria escrita por Miguel de Unamuno.
    """
    # La novela comienza formalmente con el título y prólogo
    inicio = texto.find("NIEBLA")
    if inicio == -1:
        inicio = 0

    # La novela termina antes del índice analítico añadido al final
    fin = texto.find("ÍNDICE")
    if fin == -1:
        fin = len(texto)

    return texto[inicio:fin]


def normalizar_texto(texto: str) -> str:
    """Aplica las reglas de normalización exigidas por el enunciado:
    1. Paso a minúsculas.
    2. Colapso de espacios múltiples y saltos de línea a un solo espacio.
    3. Sustitución de caracteres fuera del alfabeto permitido por '#'.
    """
    # 1. Convertir todo a minúsculas
    texto_min = texto.lower()

    # 2. Colapsar espacios repetidos, tabuladores y saltos de línea
    texto_espacios = re.sub(r"\s+", " ", texto_min).strip()

    # 3. Reemplazar cualquier carácter no permitido por el numeral '#'
    # (incluye tildes, signos de puntuación, números y la letra ñ)
    texto_normalizado = "".join(
        c if c in ALFABETO_PERMITIDO else SIMBOLO_ESPECIAL
        for c in texto_espacios
    )

    return texto_normalizado


def particionar_contiguo(texto: str, p_train: float = 0.8, p_val: float = 0.1):
    """Divide el texto en tres bloques contiguos y secuenciales:
    80% entrenamiento, 10% validación y 10% prueba.
    No se baraja al azar para respetar la dependencia de Markov contigua.
    """
    n = len(texto)
    corte_train = int(n * p_train)
    corte_val = int(n * (p_train + p_val))

    entrenamiento = texto[:corte_train]
    validacion = texto[corte_train:corte_val]
    prueba = texto[corte_val:]

    return entrenamiento, validacion, prueba


def guardar_archivo(ruta_destino: Path, contenido: str):
    """Guarda una cadena de texto en disco con codificación UTF-8."""
    with open(ruta_destino, "w", encoding="utf-8") as f:
        f.write(contenido)


def main():
    print("=" * 65)
    print("PREPARACIÓN Y NORMALIZACIÓN DEL CORPUS: 'NIEBLA'")
    print("=" * 65)

    # 1. Cargar el texto limpio de Gutenberg
    print(f"\n1. Leyendo archivo: {RUTA_ENTRADA.name}...")
    texto_bruto = cargar_texto(RUTA_ENTRADA)
    print(f"   - Caracteres iniciales leídos: {len(texto_bruto):,}")

    # 2. Quitar notas editoriales (Gutenberg)
    print("\n2. Realizando limpieza editorial (nota del transcriptor e índice)...")
    texto_obra = recortar_paratexto_editorial(texto_bruto)
    print(f"   - Caracteres tras recorte editorial: {len(texto_obra):,}")

    # 3. Normalizar (minúsculas, espacios colapsados y numeral '#')
    print("\n3. Aplicando normalización (minúsculas, espacios simples y '#')...")
    texto_norm = normalizar_texto(texto_obra)
    print(f"   - Caracteres finales normalizados: {len(texto_norm):,}")

    # Verificar vocabulario resultante
    vocabulario = sorted(set(texto_norm))
    print(f"   - Tamaño del vocabulario |V|: {len(vocabulario)} caracteres")
    print(f"   - Símbolos en el vocabulario: {repr(''.join(vocabulario))}")

    # 4. Partición contigua 80 / 10 / 10
    print("\n4. Generando partición contigua (80% / 10% / 10%)...")
    train, val, test = particionar_contiguo(texto_norm, 0.8, 0.1)

    print(f"   - Entrenamiento (80%): {len(train):,} caracteres ({len(train)/len(texto_norm)*100:.1f}%)")
    print(f"   - Validación    (10%):  {len(val):,} caracteres ({len(val)/len(texto_norm)*100:.1f}%)")
    print(f"   - Prueba        (10%):  {len(test):,} caracteres ({len(test)/len(texto_norm)*100:.1f}%)")
    print(f"   - Total particiones:    {len(train) + len(val) + len(test):,} caracteres")

    # 5. Guardar archivos en datos/
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    guardar_archivo(DIR_DATOS / "entrenamiento.txt", train)
    guardar_archivo(DIR_DATOS / "validacion.txt", val)
    guardar_archivo(DIR_DATOS / "prueba.txt", test)
    guardar_archivo(DIR_DATOS / "texto_normalizado.txt", texto_norm)

    print(f"\n5. Archivos generados con éxito en la carpeta '{DIR_DATOS.name}/':")
    print("   - datos/entrenamiento.txt")
    print("   - datos/validacion.txt")
    print("   - datos/prueba.txt")
    print("   - datos/texto_normalizado.txt")

    print("\n" + "=" * 65)
    print("¡PROCESAMIENTO Y NORMALIZACIÓN COMPLETADOS EXITOSAMENTE!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

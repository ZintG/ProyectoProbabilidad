# Reporte ejecutado S01 · piloto didáctico, no investigación de campo

**Estado:** Python ejecutado y verificado, corpus completamente sintético, sin muestreo representativo, no usado para una afirmación Q1. **R:** código aportado, ejecución pendiente.

## Pregunta
¿Un modelo de bigramas de caracteres ajustado sobre textos técnicos **fabricados** obtiene menor pérdida BPC en otras frases técnicas **fabricadas** que otro entrenado en frases generales?

## Datos y método
8 documentos generales de entrenamiento, 8 técnicos de entrenamiento y 6 técnicos de prueba. Minúsculas, recorte de espacios extremos, puntos de código Unicode. Vocabulario único fijado sobre entrenamiento. Modelo categórico de bigramas con suavizado aditivo α=1. Se incluye la probabilidad de EOS, condicionada en BOS, y se divide la pérdida total por los caracteres del texto sin EOS. El conjunto de prueba no interviene en ajuste.

## Resultados ejecutados

| Documento | Caracteres | BPC general | BPC técnico | Δ técnico − general |
|:--|--:|--:|--:|--:|
| E01 | 27 | 4.1672 | 3.6085 | -0.5586 |
| E02 | 34 | 4.2690 | 3.4482 | -0.8207 |
| E03 | 32 | 3.9001 | 3.5333 | -0.3668 |
| E04 | 37 | 4.1885 | 3.6650 | -0.5235 |
| E05 | 36 | 4.1765 | 3.5579 | -0.6185 |
| E06 | 31 | 3.8404 | 3.4871 | -0.3533 |

La diferencia media fue **-0.54024842 bits/carácter**. El intervalo de percentiles bootstrap pareado al 95%, por enumeración de **6^6 = 46 656** muestras con reemplazo, fue **[-0.66770598, -0.42038147]**. Se calculó sobre diferencias por documento y no por carácter.

## Microexperimento IC10: tokenización (Python ejecutado)

Para cambiar efectivamente la variable de tokenización, se entrenaron **dos BPE por palabras** con 20 fusiones cada uno, con desempate lexicográfico, exclusivamente sobre los corpus sintéticos de entrenamiento general y técnico. Se aplicaron a las **mismas 6 frases técnicas reservadas, 35 palabras**:

| Tokenizador | Tokens | Tokens por palabra |
|---|---:|---:|
| BPE general | 148 | 4.228571 |
| BPE técnico | 127 | 3.628571 |

La diferencia es −21 tokens en estos textos y −0,6 tokens por palabra. La reducción **no mide calidad predictiva**, no demuestra menor BPC ni avala generalización. Datos por documento: `experimentos/resultados_ic10_tokenizacion.csv`; reglas aprendidas: `experimentos/fusiones_ic10.csv`.

## Interpretación y limitaciones
La diferencia favorece al modelo ajustado con textos técnicos en estas seis frases construidas. No justifica una inferencia poblacional: las frases no son una muestra aleatoria del dominio, su redacción pudo favorecer al modelo técnico y el experimento no compara algoritmos de tokenización, Transformers ni contextos de producción. El intervalo bootstrap cuantifica variación bajo remuestreo de estos seis ítems, no sesgos de muestreo. **No hay evidencia empírica de una mejora generalizable.**

## Continuidad hacia investigación
Para IC10: precisar novedad bibliográfica, obtener corpus generales y técnicos reales con licencia compatible, congelar particiones por documento y por fuente, controlar tamaños de vocabulario y modelos probabilísticos, comparar baselines fuertes, medir varias semillas y evaluar externamente. En S01 el hito formal del curso continúa siendo proponer dos áreas de interés, no elegir problema ni declarar evidencia publicable.

**Reproducción:** `python codigo/experimento_s01.py` desde la raíz del paquete. El archivo producido es `experimentos/resultados_python.csv`.

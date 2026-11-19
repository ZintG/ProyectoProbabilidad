PREGUNTAS DEL PROYECTO
Modelos de lenguaje de n-gramas · Niebla (Unamuno)
================================================================

Archivo vivo: se completa a medida que avanzan las fases.
Última actualización: 18/11/2026
Estado: Semanas 1 y 2 cerradas. Semana 3: Fases 4 y 5 cerradas.
Pendientes: Fase 6 (bootstrap), Revisión 2, reporte final y defensa.

----------------------------------------------------------------
CÓMO USAR ESTE ARCHIVO
----------------------------------------------------------------
  [x]  respondida y documentada (se indica el número o el archivo)
  [ ]  pendiente de responder
  [!]  pregunta trampa o de defensa oral
  [O]  pregunta oficial del enunciado (obligatoria en la sección 7)

Las preguntas marcadas [O] son las de cursiva del PDF: si no están
respondidas en la discusión del reporte, se pierden puntos.

================================================================
BLOQUE 1. PREGUNTAS OFICIALES DEL ENUNCIADO (sección 7)
================================================================

1.1 [O] Fase 1
    ¿Qué tan lejos está el texto de ser «al azar» sobre su alfabeto?
    Interprete la diferencia en bits.
    [x] H(p̂ entrenamiento) = 4.0592 bits; máximo posible
        log2 |V| = log2 27 = 4.7549 bits. La diferencia es 0.6957
        bits por carácter. Un texto sin estructura gastaría 4.7549
        bits por carácter; Niebla gasta 4.0592. Esos 0.70 bits son
        la estructura del español que el modelo puede explotar.
        Ver decisiones_informe.md, Fase 1.

1.2 [O] Fase 2
    ¿Por qué el BPC de la MLE en validación es infinito en cuanto
    aparece un cero?
    [x] BPC = promedio de −log2 q. Si q(y|h) = 0 para un carácter
        que sí ocurrió, −log2 0 = +∞, y un solo término infinito
        hace infinita la media, aunque los otros 31 577 términos
        sean finitos. No es un fallo numérico: el modelo declara
        imposible algo que ocurrió. De ahí el suavizado.

1.3 [O] Fase 2
    ¿Por qué crece la proporción de ceros con n?
    [x] Porque los contextos posibles crecen como 27^(n−1) (1, 27,
        729, 19 683, 531 441) mientras el entrenamiento es fijo.
        El contexto medio cae de 252 626 a 9 357, 612, 70 y 16
        apariciones. Ceros en validación: 0, 0, 50, 491 y 2 171
        (0 %, 0 %, 0.158 %, 1.555 % y 6.875 %).
        Ojo: el plan suponía ceros desde n=2; los datos muestran
        que el bigrama está cubierto y el fallo empieza en n=3.

1.4 [O] Fase 3
    ¿Por qué el α óptimo cambia con n?
    [x] Porque el costo de suavizar depende de cuántos datos hay por
        contexto. Con c(h) grande (n=1, n=2) la masa de suavizado es
        despreciable y el mínimo cae en el borde pequeño de la
        rejilla. Con c(h)≈16 (n=5) hay más contextos raros, un cero
        cuesta ∞ y α debe subir a 0.03, donde αK = 0.81 cubre casi
        el 5 % de la masa. Es un equilibrio entre tapar ceros y no
        aplanar lo que sí se sabe. Ver sección 12.

1.5 [O] Fase 3
    ¿Qué ocurre con α = 1 en contextos que aparecen pocas veces?
    [x] La distribución se aplana: q = (c(h,y)+1)/(c(h)+27). Con
        c(h)=1, el símbolo observado recibe 2/28 = 0.071 en vez de
        ~1, y el modelo olvida casi todo lo aprendido. Costo medido
        en validación: α=1 empeora el BPC en +0.0019 (n=2), +0.0227
        (n=3), +0.1439 (n=4) y +0.3755 bits (n=5). En n=1 no se nota
        porque no hay contexto.

1.6 [O] Fase 4
    ¿Qué n elige la validación y confirma la prueba ese orden?
    [x] Ambas eligen n=5. Validación: 2.1902 bits; prueba: 2.2514
        bits (diferencia 0.0612 bits, un 2.8 %). No hubo sorpresa y
        no se reajustó nada después de ver la prueba.

1.7 [O] Fase 4
    ¿Por qué el BPC de entrenamiento sigue bajando cuando el de
    prueba ya no?
    [x] Es sobreajuste. Al crecer n el modelo memoriza secuencias
        concretas del entrenamiento: el BPC de entrenamiento cae
        4.0592 → 3.2354 → 2.6872 → 2.1538 → 1.7320. Pero los
        contextos nuevos del texto no visto caen al casi uniforme
        1/27 (4.7549 bits), así que el BPC de prueba se estanca:
        4.0536 → 3.2122 → 2.7223 → 2.3461 → 2.2514. La brecha
        entreno-prueba se abre hasta 0.52 bits en n=5.

1.8 [O] Fase 5
    ¿Por qué π se parece a las frecuencias del texto?
    [x] Porque P es estrictamente positiva (α>0), luego la cadena es
        irreducible y aperiódica, tiene distribución estacionaria
        única y π_j = Σ_i π_i P_ij. Ese sistema tiene por solución el
        vector de frecuencias relativas que generó los conteos de
        pares. Empíricamente: diferencia máxima 3.71×10⁻⁶ y
        distancia L1 9.05×10⁻⁶.

1.9 [O] Fase 5
    ¿Qué propiedades del español capturan las muestras y cuáles no?
    [x] Capturan: frecuencias de letras, combinaciones locales
        frecuentes (sílabas, «de que», «contaba porque no»), la
        proporción de espacios (17.9 %) y de # (8.1 %).
        No capturan: palabras completas, concordancia, sintaxis,
        puntuación con sentido ni coherencia global. En n=5 aparecen
        tramos aleatorios porque el contexto se vuelve desconocido.

1.10 [O] Fase 6
     ¿El intervalo excluye el cero?
     [ ] Pendiente: se responde al ejecutar el bootstrap.

1.11 [O] Fase 6
     ¿Por qué se remuestrean bloques y no caracteres individuales?
     [ ] Pendiente. Pista para redactar: los caracteres de un texto
         no son independientes; el bootstrap i.i.d. rompería la
         dependencia serial y subestimaría la varianza del BPC.
         Los bloques de 2000 conservan la estructura local y son
         aproximadamente independientes entre sí.

================================================================
BLOQUE 2. LA PREGUNTA CENTRAL Y LAS MÉTRICAS
================================================================

2.1 [CLAVE] ¿Cuánto mejora la predicción del siguiente carácter al
    aumentar la memoria del modelo?
    [x] De n=1 a n=5 el BPC de prueba baja 1.8022 bits por carácter:
        4.0536 → 2.2514, un 44.5 % menos. La perplejidad cae de
        16.6 a 4.76. En validación: 4.0515 → 2.1902 (1.8613 bits).
        La mayor parte de la ganancia está en n=1→3; después la
        curva se aplana.

2.2 ¿Qué significa exactamente BPC?
    [x] Bits por carácter: el costo medio, en bits, de codificar cada
        carácter con el modelo q. Es −(1/N) Σ log2 q(y_t | h_t).
        Menos bits = mejor predicción = mejor compresión. Un texto
        uniforme sobre 27 símbolos cuesta log2 27 = 4.7549 BPC.

2.3 ¿Qué es la perplejidad y cómo se relaciona con el BPC?
    [x] PPL = 2^BPC. Se interpreta como el número de alternativas
        equiprobables entre las que el modelo «duda» en promedio.
        Con BPC 2.2514, PPL = 4.76: el modelo equivale a elegir
        entre ~5 símbolos, no entre 27.

2.4 ¿Un BPC de 2.25 es bueno?
    [x] Comparado con las referencias internas del proyecto sí:
        uniforme 4.7549, unigramas 4.0536, bigramas 3.2122. Para
        comparar con la literatura hay que igualar corpus,
        normalización y unidad (carácter vs token); un BPC de otro
        trabajo no es comparable sin eso.

2.5 ¿Por qué la entropía de unigramas no es una cota inferior del
    BPC de n=5?
    [x] Porque condicionar reduce la entropía:
        H(X_t | X_{t−1},…,X_{t−4}) ≤ H(X_t). La cota de Gibbs se
        aplica entre la misma distribución: por eso la desigualdad
        se comprueba solo con unigramas. Comparar el BPC del
        pentagrama contra H de unigramas no viola nada.

================================================================
BLOQUE 3. METODOLOGÍA Y TRAMPAS DE DISEÑO
================================================================

3.1 ¿Por qué la partición es contigua 80/10/10 y no aleatoria?
    [x] El lenguaje tiene dependencia fuerte entre caracteres
        vecinos. Barajar introduciría fuga de información: trozos de
        la misma frase en entrenamiento y en prueba. Contiguo
        reproduce el escenario real de predecir texto nuevo.

3.2 ¿Por qué α y n se eligen con validación y no con prueba?
    [x] Elegir con prueba es elegir mirando el examen: el BPC
        reportado dejaría de ser una estimación honesta. Validación
        es texto no visto pero disponible para decidir; prueba se
        reserva para una única medición final.

3.3 ¿Por qué las primeras n−1 posiciones de un bloque usan el final
    del bloque anterior como contexto?
    [x] Para no desperdiciar posiciones ni inventar contexto. El
        texto es contiguo en el tiempo: las primeras letras de
        validación realmente venían precedidas por las últimas del
        entrenamiento. La alternativa (descartarlas) perdería n−1
        caracteres por bloque y rompería la comparación con N.

3.4 ¿Por qué el denominador del BPC es N−n+1 en entrenamiento y N en
    prueba?
    [x] En entrenamiento se cuentan n-gramas completos: hay N−n+1.
        En prueba se evalúan los N caracteres del bloque, porque el
        contexto se hereda del bloque anterior. Mismo numerador
        conceptual, distinto número de términos; ambos son promedios
        por carácter evaluado.

3.5 ¿Hay fuga de información entre particiones?
    [x] No. Los conteos c(h) y c(h,y) salen solo del entrenamiento.
        α* se elige con validación. Prueba solo se lee para medir.
        El script fase4.py incluso se niega a repetir la evaluación
        si T3 ya existe.

3.6 ¿Qué se puede y qué no se puede hacer después de ver la prueba?
    [x] Se puede: recalcular una figura, corregir un error de
        formato, reportar el resultado tal cual.
        No se puede: cambiar α*, cambiar n, ampliar la rejilla,
        descartar un orden porque «no gustó». Eso invalidaría el
        protocolo y hay que declararlo en el reporte.

3.7 ¿Por qué reportar el BPC de entrenamiento si no sirve para
    elegir?
    [x] Porque su comparación con el de prueba mide sobreajuste. Es
        la evidencia de que el modelo memoriza y deja de
        generalizar, y es justo lo que pide discutir la pregunta 1.7.

3.8 ¿Basta una sola partición de prueba?
    [x] No para concluir con incertidumbre. Un solo número no trae
        intervalo. Por eso la Fase 6 remuestrea bloques para dar un
        IC del 95 % a la diferencia entre modelos.

3.9 ¿Por qué se elige el mejor n por BPC y no por perplejidad?
    [x] Son monótonas entre sí (PPL = 2^BPC): el orden de los modelos
        es idéntico. Se reporta PPL porque es más interpretable, pero
        la decisión se toma con BPC.

================================================================
BLOQUE 4. DETALLES TÉCNICOS POR FASE
================================================================

4.1 ¿Por qué |V| = 27 y por qué falta la w?
    [x] 26 letras + espacio = 27 candidatos, pero Unamuno no usa la
        w, así que el vocabulario efectivo es 25 letras + espacio + #
        = 27 símbolos. Se fija solo con el entrenamiento.

4.2 ¿Qué es el símbolo # y por qué pesa 8.1 %?
    [x] Es el cajón único para todo lo que no sea a–z ni espacio:
        puntos, comas, comillas, guiones, dígitos, ñ, tildes y
        diéresis. Por eso «más» es m#s y «año» es a#o. No son saltos
        de línea: los saltos se colapsaron a un espacio.

4.3 ¿Cómo se comprobó que las condicionales suman 1?
    [x] Sumando q(y|h) sobre los 27 símbolos para todos los
        contextos observados: desviación máxima 1.1×10⁻¹⁶, muy por
        debajo de la tolerancia 10⁻¹². También se comprobó que el
        contexto nunca visto devuelve 1/27.

4.4 ¿Qué es la prueba de «abracadabra»?
    [x] Un caso de juguete con resultado conocido de la Tabla 2 del
        enunciado. Reproduce conteos (a:5, b:2, r:2, c:1, d:1),
        H = 2.0404 bits, q̂(b|a) = 0.5, q̂₁(b|a) = 1/3, BPC 0.6 y
        PPL 1.5157. Sirve para validar el código antes del corpus.

4.5 ¿Qué es la perturbación de 0.01 y qué demuestra?
    [x] Se mueve 0.01 de probabilidad entre dos símbolos de un
        contexto frecuente (h = espacio, c(h) = 45 320). La MLE da
        ℓ = −566 543.6785; las dos perturbaciones dan −566 591.3136
        y −567 021.2821, peores. Confirma la Prop. 1.1.8: la MLE
        maximiza la log-verosimilitud.

4.6 ¿Qué significan c(h) y αK?
    [x] c(h) es cuántas veces apareció el contexto. αK es la masa de
        probabilidad falsa repartida: α para cada uno de los K=27
        símbolos. La fracción de masa de suavizado es αK/(c(h)+αK).
        En n=5, αK=0.81 frente a c(h)≈16: casi el 5 %.

4.7 ¿Por qué el suavizado aditivo equivale a una previa Beta(α,α)?
    [x] Con dos símbolos y previa Beta(α,α), la media predictiva
        posterior es (c₁+α)/(c₁+c₂+2α), que es la fórmula (2) con
        K=2. El suavizado es la versión con simetría e intercambio
        de una previa de Dirichlet(α,…,α).

4.8 ¿Por qué la desigualdad de Gibbs se comprueba solo con
    unigramas?
    [x] Porque H(p) ≤ H(p,q) exige comparar la misma variable. Con
        unigramas, p̂_prueba y q̂ viven sobre el mismo alfabeto.
        Mezclar el BPC de un modelo condicionado con la entropía
        marginal no es una comparación válida (ver 2.5).

4.9 ¿Qué mide la KL en este contexto?
    [x] KL(p‖q) = H(p,q) − H(p) = 0.006433 bits. Es el costo extra
        en bits por usar q̂ en lugar de la distribución empírica
        verdadera. Positiva siempre; cero solo si p = q. Aquí es
        pequeña porque el unigramas suavizado ya reproduce bien las
        frecuencias.

4.10 ¿Por qué la Gráfica F4 va en escala logarítmica?
     [x] Porque S_k cae de 8.9 a 2.25 en los primeros cientos de
         caracteres y luego oscila en un rango minúsculo. En escala
         lineal toda la zona de convergencia queda comprimida. Con
         eje log se ve tanto la caída como la meseta.

4.11 ¿Por qué la matriz 27×27 es positiva y qué garantiza?
     [x] Porque α > 0 suma α a cada par, incluso a los no vistos.
         Entrada mínima 2.207×10⁻⁸. Una matriz estocástica positiva
         implica cadena irreducible y aperiódica; por el teorema
         ergódico tiene estacionaria única y converge a ella desde
         cualquier distribución inicial.

4.12 ¿Cómo funciona la iteración de potencias y por qué bastaron 22
     iteraciones?
     [x] Se parte de π₀ uniforme y se aplica π_{t+1} = π_t P (P es
         estocástica por filas, por eso se multiplica por la
         izquierda). Se para cuando ‖π_{t+1} − π_t‖₁ < 10⁻¹⁰.
         Convergió en 22 iteraciones con última diferencia
         3.35×10⁻¹¹. La velocidad la fija el segundo autovalor de P;
         al ser P positiva, el módulo es < 1 y la convergencia es
         geométrica.

4.13 ¿Por qué el muestreo usa q(·|h) y no el texto original?
     [x] Porque el objetivo de la Fase 5 es simular la cadena
         estimada, no copiar el corpus. Se muestrea de la misma
         distribución que se evaluó, con semilla fija para que el
         experimento sea reproducible.

4.14 ¿Por qué fijar la semilla?
     [x] Para que las tres muestras partan del mismo contexto y los
         números del anexo se puedan reproducir exactamente. Semilla
         2026, contexto inicial «habia », 300 caracteres.

4.15 ¿Por qué comparar π con unigramas y no con bigramas?
     [x] Porque π es una distribución marginal sobre símbolos: dice
         con qué frecuencia aparece cada letra a largo plazo. Su
         análogo empírico son las frecuencias de unigramas. Los
         bigramas son condicionales y no se comparan con un vector
         marginal.

4.16 ¿Por qué las muestras tienen tramos de letras sin sentido?
     [x] Tres causas: (a) el modelo solo ve n−1 caracteres, no tiene
         noción de palabra; (b) al generar se retroalimenta, así que
         un carácter raro contamina el contexto siguiente y el error
         se propaga; (c) si el contexto no se vio en entrenamiento,
         q cae al casi uniforme 1/27 y produce ruido. En n=5, con
         c(h)≈16, eso pasa a menudo.

4.17 ¿Por qué n=5 memoriza fragmentos y aun así gana en BPC?
     [x] Porque el BPC premia la predicción local: en los contextos
         frecuentes el modelo es muy afilado y acierta mucho. La
         memoria de fragmentos es real (por eso salen «contaba
         porque no»), pero no alcanza para generar texto coherente.
         Son dos criterios distintos: ajuste local vs coherencia
         global.

================================================================
BLOQUE 5. DEFENSA ORAL Y PREGUNTAS TRAMPA
================================================================

5.1 [!] Si n=5 es el mejor modelo, ¿por qué genera peor texto que
    n=2?
    [x] Porque el BPC mide predicción con el carácter verdadero
        delante, y la generación encadena errores sin corrección.
        Además n=5 tiene muchos contextos raros que caen al
        uniforme. El mejor BPC no implica el mejor texto: son
        objetivos distintos.

5.2 [!] ¿Qué pasaría con n=10 o n=20?
    [x] El BPC de entrenamiento seguiría bajando (más memoria) y el
        de prueba empeoraría: con 252 626 caracteres, n=10 tiene
        27⁹ contextos posibles y casi todos los vistos aparecen una
        vez. La estimación sería ruido. El corpus fija un techo
        práctico alrededor de n=5.

5.3 [!] ¿Por qué no usar α = 0?
    [x] Porque reproduce la MLE, que asigna cero a lo no visto. Un
        solo cero en prueba hace el BPC infinito. α>0 es lo que
        hace la matriz positiva y la métrica finita.

5.4 [!] ¿Este modelo es de Markov? ¿De qué orden?
    [x] Sí: es una cadena de Markov de orden n−1 sobre caracteres.
        La probabilidad del siguiente símbolo depende solo de los
        n−1 anteriores. Para n=1 es i.i.d.; para n=2 es una cadena
        de Markov ordinaria (la que se usa en la Fase 5).

5.5 [!] ¿Qué supone el modelo sobre el texto?
    [x] Que el proceso es estacionario (las probabilidades no
        cambian a lo largo del libro) y de memoria finita n−1. La
        primera suposición es discutible: cambian los personajes,
        los capítulos y el estilo. Es una limitación a declarar.

5.6 [!] ¿Por qué la perplejidad es 4.76 y no 27?
    [x] Porque 27 sería el modelo sin información (uniforme,
        BPC 4.7549). El modelo aprendido reduce la incertidumbre a
        ~4.76 alternativas efectivas. PPL no es «cuántos símbolos
        hay» sino «entre cuántos duda».

5.7 [!] ¿Cómo se compararía justo con BPE (Fase 7)?
    [x] Con BPC por carácter: bits totales del texto de prueba
        divididos entre el número de caracteres. Así la unidad de
        medida es la misma aunque el modelo trabaje con tokens.

5.8 [!] ¿Qué cambiaría con un modelo neuronal?
    [x] La memoria dejaría de ser fija: una red puede mirar cientos
        de caracteres y generalizar entre contextos parecidos. Eso
        atacaría las dos fallas vistas: contextos no vistos y
        coherencia global. El BPC bajaría, a costa de perder la
        interpretabilidad de los conteos.

5.9 [!] ¿Los resultados dependen del libro elegido?
    [x] Sí, en el nivel absoluto: el estilo, el vocabulario y la
        puntuación de Niebla fijan las frecuencias. Las tendencias
        (BPC baja con n hasta un punto, luego sobreajuste; π ≈
        unigramas) son estructurales y aparecerían con cualquier
        corpus en español.

5.10 [!] ¿Por qué no se barajó el texto para tener particiones más
     «representativas»?
     [x] Porque la dependencia serial es justamente lo que el modelo
         explota. Barajar destruiría la señal y además filtraría
         información entre particiones. La partición contigua es la
         única honesta para este problema.

================================================================
BLOQUE 6. PENDIENTES (Semana 3 en adelante)
================================================================

6.1 [ ] Fase 6: dividir prueba en bloques contiguos de 2000
    caracteres y calcular Δ_j = BPC(mejor n) − BPC(n−1) en cada uno.
    Preguntas a responder al terminar:
      - ¿Cuántos bloques salen? (31 579 / 2000 ≈ 15.8)
      - ¿La media de Δ_j es positiva? ¿De qué tamaño?
      - ¿El IC percentil del 95 % con 10 000 remuestras excluye 0?
      - ¿Qué implica si excluye 0 y qué si no?
      - ¿Por qué la unidad de remuestreo es el bloque?

6.2 [ ] Revisión 2 con el profesor: llevar T3, T3_gibbs, F3, F4, F5,
    las muestras y los α* congelados. Preguntar explícitamente si el
    tratamiento de # y de la ñ/tildes es aceptable.

6.3 [ ] Reporte final (10–14 páginas, 8 secciones obligatorias):
      - Resumen ≤ 200 palabras con el número principal.
      - Marco con notación definida antes de usarla.
      - Datos: obra, URL, fecha, licencia, normalización, |V|.
      - Métodos: modelo, suavizado, elección de α, métricas,
        simulación y bootstrap.
      - Resultados: T2–T4 y F2–F5 citadas y comentadas.
      - Verificaciones: abracadabra, suma de condicionales, MLE.
      - Discusión: las 11 preguntas oficiales del bloque 1.
      - Conclusiones: respuesta a la pregunta central en 3–5 frases.

6.4 [ ] Reproducibilidad: verificar que todo corre desde consola en
    menos de 10 minutos y escribir el README definitivo.

6.5 [ ] Defensa: 20 minutos de preparación y 10 de exposición con
    reparto entre los 4 integrantes. Los bloques 2, 3 y 5 de este
    archivo son el guion de estudio.

6.6 [ ] Preguntas todavía sin respuesta en este archivo: 1.10, 1.11
    y todo el bloque 6.

================================================================
REGISTRO DE AVANCE
================================================================
  Fase 1  Exploración del corpus .................... [x]
  Fase 2  Conteos y MLE ............................. [x]
  Fase 3  Suavizado y elección de α ................. [x]
  Fase 4  Evaluación única, Gibbs, F3 y F4 .......... [x]
  Fase 5  Simulación y π ............................ [x]
  Fase 6  Bootstrap ................................. [ ]
  Fase 7  BPE (opcional) ............................ [ ]
  Reporte final ..................................... [ ]
  Defensa oral ...................................... [ ]

  Preguntas oficiales respondidas: 9 de 11.
  Pendientes: 1.10 y 1.11 (Fase 6).
================================================================

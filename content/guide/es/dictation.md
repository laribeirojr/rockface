# Dictado en el microscopio

## Para qué sirve

En el microscopio los ojos están en los oculares y las manos en la platina. Con el dictado el petrógrafo habla en vez
de escribir: los **campos de la descripción** ("selección moderada, subredondeado, porosidad intergranular primaria
12 por ciento, contactos cóncavo-convexos") y el **conteo de puntos** ("cuarzo monocristalino", "tres", "deshacer").
El habla se reconoce **en este ordenador** — el audio no se guarda ni se envía — y nada se escribe antes de que el
petrógrafo vea lo que se entendió.

![La ventana Dictar con las palabras oídas y las propuestas leídas de ellas](../img/es/dictation.webp)

## Antes de empezar

* Instale una vez las bibliotecas de voz: `pip install rockface[voice]` (whisper.cpp, Vosk y la biblioteca del
  micrófono; todas MIT o Apache-2.0).
* Abra **Dictar → Modelos de voz…** y descargue:
  * **Whisper base** (142 MB) para dictar descripciones — o *Whisper small* (466 MB) con 8 GB de memoria, o
    *Whisper large-v3 turbo* (547 MB) con una tarjeta NVIDIA RTX y una compilación CUDA de pywhispercpp;
  * el modelo **Vosk small** de su idioma (31–40 MB) para contar por voz.
* Elija el micrófono en la misma ventana. Un micrófono de auricular deja fuera el ruido de la sala.

## Paso a paso

**Dictando la descripción**

1. Abra una descripción y haga clic en **Dictar** (pestaña Inicio).
2. Haga clic en **Escuchar** y hable. Haga una pausa después de cada frase: cada pausa envía lo que dijo, que aparece
   en el cuadro de texto. También puede escribir o pegar las palabras y hacer clic en **Interpretar**.
3. Lea la tabla: cada propuesta muestra el campo, el valor, el % o mm, y **las palabras de las que salió**.
   * Una palabra que sirve para varios tipos (*intergranular*: ¿primaria o secundaria?) viene **sin marcar**, con
     una lista para elegir.
   * Una frase negada (*sin fracturas*, *no cement*, *sem porosidade móldica*) aparece como **dicho ausente** y
     nunca añade nada.
   * Decir un campo dos veces se queda con el último: "bien seleccionado… no, moderadamente seleccionado" da
     *moderadamente seleccionado*.
4. Marque lo que está bien y haga clic en **Aplicar las marcadas**. Los valores van a las pestañas Microscópica y
   Sistema poroso; **guarde la descripción** para conservarlos (las verificaciones de siempre se ejecutan entonces).
5. Lo que no se entendió puede ir a las notas de la descripción microscópica (marque la casilla bajo la tabla).

**Contando por voz**

1. En la pestaña **Conteo**, haga la grilla como siempre y haga clic en **Contar por voz**.
2. En cada punto diga el nombre del constituyente (*cuarzo monocristalino*), parte de él cuando solo una línea lo
   tiene (*feldespato*), o el número de su atajo de teclado (*tres*, *número tres*).
3. Comandos: **deshacer**, **volver**, **saltar**, **detener** (*undo, back, skip, stop*; *desfazer, voltar, pular,
   parar*).
4. La línea bajo el botón dice lo que se oyó y lo que se hizo. Una palabra no entendida, o que sirve para dos líneas
   (*cuarzo* con cuarzo mono y policristalino), no cuenta nada: el programa emite un pitido y usted la repite.
5. **La platina nunca se mueve por voz**: muévala con el teclado, el controlador o a mano.

**Preguntando a Mio**

* El botón del micrófono junto al cuadro de pregunta de Mio escucha una pregunta y la pone en el cuadro; léala y
  envíela.
* *"Dicta: selección moderada, porosidad 12 por ciento"* (*anote:*, *note:*) hace que Mio lea los campos en las
  palabras — ella solo los muestra; quien los escribe es la ventana Dictar.

## Campos entendidos

| Campo | Ejemplos |
|---|---|
| Selección | *bien seleccionado*, *selección moderada*, *moderately sorted*, *mal selecionado* |
| Redondez y sus modificadores | *subredondeado*, *anguloso*, *subrounded*, *granos con engolfamientos* |
| Esfericidad | *esfericidad alta*, *low sphericity*, *alargado* |
| Moda granulométrica principal | *arena media*, *fine sand*, *moda principal 0,25 mm*, *moda principal cero coma dos cinco milímetros* |
| Fábrica | *soportada por granos*, *soportado por la matriz*, *imbricada* |
| Contactos intergranulares (con %) | *contactos cóncavo-convexos 40 por ciento*, *suturados*, *contactos puntuales* |
| Porosidad visual total | *porosidad total 18 por ciento*, *porosity 12 %*, *sin porosidad visible* (0 %) |
| Tipos de poro (con %) | *intergranular primaria 12*, *porosidad móldica 3 por ciento*, *microporosidad*, *vugs* |

Los números pueden ser cifras o palabras en los tres idiomas (*veinticinco*, *twenty five*, *vinte e cinco*;
*cero coma dos cinco*).

## Cómo funciona

* **Dos reconocedores, ambos locales.** Whisper (whisper.cpp, MIT) escribe el dictado libre y se orienta hacia el
  vocabulario petrográfico con un texto inicial corto con los términos de la descripción y los constituyentes de la
  composición (sesgo contextual, Lall y Liu 2024). Vosk (Apache-2.0) reconoce al instante el vocabulario cerrado
  del conteo — las líneas, los números y los comandos —, así que una palabra fuera de él se rechaza en vez de
  adivinarse.
* **Solo se oye el habla.** El sonido se corta en frases por su intensidad (una pausa de 0,6 s termina una), de modo
  que el reconocedor nunca oye silencio: Whisper inventa frases en el silencio (*Careless Whisper*, Koenecke et al.
  2024). Se quitan las frases inventadas conocidas ("gracias por ver", "thanks for watching") y las frases repetidas
  en bucle.
* **Cada propuesta muestra sus palabras.** Los errores del reconocimiento de voz parecen plausibles, y quitar o poner
  un "no" es el error clásico (Basma et al. 2011): de ahí las palabras oídas, los tipos ambiguos sin marcar y las
  negaciones que nunca se vuelven presencias.
* **El vocabulario es el de la base de conocimiento**: las etiquetas de los términos y de las escalas en inglés,
  español y portugués, con los géneros y plurales del español y del portugués (*seleccionado/seleccionada*).

## Desde un script

```python
d = prj["ILL-TS-001"]
r = d.dictate("subanguloso, contactos suturados", "es")              # solo las propuestas
[(p["target"], p["code"], p["value"]) for p in r["proposals"]]
d.dictate("subanguloso, contactos suturados", "es", apply=True)      # escritas y guardadas (las verificaciones de siempre)
prj["ILL-TS-002"].voice_count("tres", "es")                          # {"kind": "count", "slot": 3, ...}
rf.dictation("bien seleccionado, porosidad 12 %", "es")              # sin proyecto
rf.speech_models(); rf.speech_status()
rf.transcribe("nota.wav", "es")                                      # un archivo WAV de 16 bits, reconocido localmente
```

## Límites y problemas comunes

* **No se encuentra ningún micrófono**: instale `rockface[voice]` (sounddevice trae PortAudio) y revise el
  dispositivo de entrada del sistema; elíjalo en *Modelos de voz…*.
* Whisper base en un procesador antiguo tarda uno o dos segundos por frase; las frases cortas con pausas funcionan
  mejor. Con una tarjeta RTX, *large-v3 turbo* es más rápido y más preciso.
* El dictado libre entiende los campos de arriba; la composición se cuenta por voz, no se dicta en porcentajes.
* El modelo Vosk pequeño de español tiene alrededor de 16 % de palabras erradas en el habla libre; en el vocabulario
  cerrado del conteo, que es para lo que se usa, es fiable.
* Algunos modelos Vosk son AGPL o no comerciales; solo se ofrecen los Apache-2.0.

## Cobertura

O8 (pedido del dueño del 2026-11-17: las innovaciones, la tercera).

Referencias: Radford et al. (2023), Whisper, PMLR 202; Koenecke et al. (2024), https://doi.org/10.1145/3630106.3658996;
Basma et al. (2011), https://doi.org/10.2214/AJR.11.6691; Lall y Liu (2024), arXiv:2410.18363; Povey et al. (2011),
Kaldi; Al-Dhubaib et al. (2008), US 7.319.961 (captura por voz de datos petrográficos y conteos; expirada).

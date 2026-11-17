# Mio mira la imagen

## Para qué sirve

Mio puede mirar una fotomicrografía de la lámina y proponer los campos de la descripción microscópica y del sistema
poroso — selección, redondez, esfericidad, tamaño de grano, fábrica, contactos, porosidad visible y tipos de poro —,
cada uno con **cuántas de sus respuestas coinciden**. Quien mira es un modelo en su propia computadora; nada viene
marcado y nada se escribe hasta que usted marque lo que ve en la imagen, lo aplique al formulario y guarde la
descripción.

## Antes de empezar

* Un **modelo de visión** en esta computadora (*Mio mira* → *Modelos de visión…*):
  * con una **tarjeta NVIDIA RTX de 12 GB** (RTX 3060 o superior): **Qwen2.5-VL 7B** (Q5_K_M), 6,8 GB de descarga;
  * con una tarjeta de **24–32 GB** (RTX 5090): **Qwen2.5-VL 32B** (Q4_K_H), 19,3 GB;
  * con una tarjeta de 8 GB o sin tarjeta: el 7B más pequeño (Q4_K_M) — en el procesador tarda minutos por imagen.

  La ventana marca el modelo que cabe en la tarjeta encontrada. Cada modelo viene en dos archivos, el modelo de
  lenguaje y su proyector de imagen; ambos son Apache-2.0. Los lee **llama-cpp-python** (compilado con CUDA para usar
  la tarjeta; los instaladores lo traen compilado para el procesador). O use un **servidor local** que ya tenga el modelo — Ollama
  (`ollama pull qwen2.5vl:7b`), LM Studio o llama-server —, indicando su dirección (`http://localhost:11434/v1`) y el
  nombre del modelo.
* Una **imagen** de la lámina: una foto o lámina entera en el Atlas, la imagen del conteo de puntos o un archivo. La
  imagen con nícoles cruzados del mismo campo ayuda (colores de interferencia, extinción).

## Paso a paso

1. Abra la descripción y haga clic en **Mio mira** (pestaña Inicio).
2. Elija la **imagen**. Las fotos del Atlas en luz polarizada plana aparecen primero; su **par con nícoles cruzados**
   se encuentra por el lugar en la lámina o por el nombre (`… PP` / `… XP`) y se muestra al lado. De una lámina
   entera se muestra el centro, 2 mm (un campo de visión). El **ancho del campo** viene de la escala de la imagen;
   escríbalo si se desconoce — con él el modelo juzga el tamaño de grano.
3. Elija cuántas **respuestas** (3 por defecto) y haga clic en **Mirar**. Se pregunta al modelo esas veces; cada
   respuesta es una línea por campo, con las palabras del vocabulario de RockFace en su idioma.
4. Lea la tabla: el campo, el **valor** que dio la mayoría de las respuestas (los otros dichos quedan en su lista, con
   cuántas respuestas los dieron), la cantidad (la mediana, con el rango dicho), **Respuestas que coinciden** (2/3,
   3/3…) y la línea del propio modelo.
5. Mire la imagen y **marque** solo lo que usted mismo ve. *Marcar donde todas coinciden* marca las líneas 3/3 —
   desmarque las que no comparta.
6. **Aplique** y guarde la descripción como siempre. *Respuestas del modelo* muestra las respuestas completas.

**Mio**: *"¿qué ves en la imagen de ILL-TS-001?"* (*"what do you see in …?"*, *"o que você vê na …?"*) mira la
primera imagen en luz plana de la muestra y lista las propuestas con su coincidencia; no escribe nada.

## Cómo funciona

* **El modelo.** Qwen2.5-VL (Bai et al. 2025) lee la imagen con hasta 1024 píxeles en su lado mayor y responde un
  formulario fijo: una línea por campo, “no visible” cuando la imagen no permite juzgar. Sus palabras pasan por el
  mismo lector del dictado (1.0.0rc6), así que las propuestas usan los términos de RockFace; el campo nombrado al
  inicio de la línea decide qué propuestas de esa línea valen.
* **Qué tan seguro.** Lo que un modelo dice de su propia certeza está mal calibrado (Xiong et al. 2024). En su lugar
  se pregunta al modelo varias veces, con temperatura 0,7, y se comparan las respuestas: la confianza de un valor es la
  parte de las respuestas que lo dieron (autoconsistencia, Wang et al. 2023). Las cantidades coinciden cuando están a
  menos de 2 puntos porcentuales o 25 % de la mediana (30 % para un tamaño en mm). Con una sola respuesta, la
  coincidencia no dice nada.
* **Nada marcado.** Las personas siguen consejos automáticos aun cuando están equivocados (sesgo de automatización,
  Goddard et al. 2012): toda propuesta empieza desmarcada y solo se escribe cuando usted la aplica.
* **Solo local.** Las imágenes nunca salen de la computadora; un servidor en otra computadora se rechaza, salvo que
  `vision.allow_remote` se active a propósito.
* **Lo que ya se midió.** Todavía nada en láminas reales: esta versión se probó con respuestas guionadas, sin el modelo
  en marcha. Los trabajos publicados sobre describir láminas con modelos de visión y lenguaje — ThinGPT (Luo et al.
  2025) y un modelo de carbonatos entrenado con 57 000 imágenes (Atolagbe & Koeshidayatullah 2026) — usaron modelos
  entrenados con láminas etiquetadas; el Qwen2.5-VL general usado aquí no, así que espere más seguridad en la textura
  que en la mineralogía y revise cada propuesta.
* **Fuera de esta versión.** Buscar en la biblioteca las láminas más parecidas y proponer a partir de sus
  descripciones espera la decisión del propietario sobre dos patentes (US 12,688,615 B2; US 2022/0207079 A1).

## Desde un script

```python
d = prj["ILL-TS-001"]
r = d.look(samples=3)               # la primera imagen PP de la lámina en el Atlas, y su par XP
[(f["target"], f["code"], f["value"], f["confidence"]) for f in r["findings"]]
r["answers"]                        # lo que escribió el modelo, respuesta por respuesta
d.look(image="campo.png", xpl="campo_xp.png", width_mm=1.3, apply=True, at_least=1.0)  # escribe las 3/3
rf.look("campo.png", lang="es")    # sin proyecto
rf.vision_models(); rf.vision_status()
```

## Límites y problemas comunes

* Un modelo general, no un petrógrafo: puede tomar cemento por grano o granos arrancados por poros, o llamar a toda
  roca moderadamente seleccionada. La coincidencia entre respuestas mide su coherencia, no su acierto.
* La composición mineral no se propone — eso es el conteo de puntos (con el asistente de IA de la 1.0.0rc7).
* Los números ganan a las palabras: una descripción con selección medida (φ) o tamaño de grano medido mantiene la
  clase que sigue al número cuando se aplica la propuesta, y el guardado lo avisa.
* Imagen sin escala: escriba el ancho del campo, o el tamaño de grano se adivinará de la nada.
* En el procesador el modelo 7B tarda minutos para tres respuestas; el 32B necesita una tarjeta de 24–32 GB.
* “Este llama-cpp-python no lee imágenes de Qwen2.5-VL”: actualice llama-cpp-python o use un servidor local.

## Cobertura

O8 (pedido del propietario del 2026-11-17: las innovaciones, la quinta).

Referencias: Bai et al. (2025), Qwen2.5-VL technical report, arXiv:2502.13923; Wang et al. (2023), Self-consistency
improves chain of thought reasoning in language models, ICLR 2023, arXiv:2203.11171; Xiong et al. (2024), Can LLMs
express their uncertainty?, ICLR 2024, arXiv:2306.13063; Goddard, Roudsari & Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089; Luo et al. (2025), ThinGPT, Petroleum Science,
https://doi.org/10.1016/j.petsci.2025.09.009; Atolagbe & Koeshidayatullah (2026), Vision-language models for automated
carbonate petrography and depositional environment interpretation, Artificial Intelligence in Geosciences 7(3)
100230, https://doi.org/10.1016/j.aiig.2026.100230.

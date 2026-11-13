# RockFace IA: instalación, dispositivo y el hub de modelos

## Para qué sirve

RockFace IA añade redes neuronales a Lab y MC: modelos que segmentan imágenes, láminas enteras, volúmenes de micro-CT
y perfiles de imagen, que se pueden entrenar y ajustar con sus propias anotaciones, y un modelo generativo de imágenes
de roca. Es una **opción**: RockFace sin IA tiene todas las demás funciones, y nada más cambia cuando se añade. Esta
página muestra cómo instalarla para la computadora que usted tiene, cómo elegir dónde corren los modelos (el
procesador o una tarjeta gráfica) y cómo los modelos se guardan, se comparten y se comparan en el **hub de modelos**.

## Antes de empezar

* RockFace instalado (0.26 o posterior).
* Para una tarjeta gráfica: el driver de la propia tarjeta (NVIDIA, AMD o Intel). El resto viene con los paquetes.

## Paso a paso

### Instalación: la computadora se identifica, usted elige

1. En una terminal, ejecute `rockface ai setup`. RockFace lista lo que encontró — sistema, procesador, núcleos,
   instrucciones vectoriales, memoria, tarjetas gráficas y los paquetes de IA ya instalados — y las opciones para esta
   computadora:

   | Opción | Cuándo |
   |---|---|
   | RockFace sin IA | Nada más que instalar |
   | IA en el procesador | Cualquier computadora; aplicar un modelo lleva de segundos a minutos, entrenar de minutos a horas |
   | IA en la tarjeta gráfica NVIDIA (CUDA) | Una tarjeta NVIDIA: la más rápida para aplicar y para entrenar |
   | IA en la tarjeta gráfica (DirectML) | Windows con cualquier tarjeta DirectX 12 (NVIDIA, AMD, Intel): los modelos se aplican en la tarjeta, el entrenamiento corre en el procesador |
   | IA en Apple silicon (Core ML y MPS) | Un Mac con procesador M |

   La opción recomendada viene marcada; **usted decide**. Escriba su número (o Enter para la recomendada).
2. RockFace muestra el comando de instalación (`python -m pip install …`) y pregunta antes de ejecutarlo. Con
   `--option cuda --yes` elige e instala sin preguntar; con `--dry-run` sólo muestra el comando.
3. El mismo diálogo está en el programa: **Lab → IA** o **MC → IA**, botón **Hardware y dispositivo…**. Muestra el
   hardware, las opciones con la recomendada en negrita y el comando que instala la seleccionada (con el botón
   **Copiar**). **OK** guarda su elección.

`rockface ai info` muestra el hardware y el dispositivo en uso; `rockface ai models [proyecto]` lista los modelos.

### El hub de modelos

La tabla **Modelos** de la pestaña IA lista todos los modelos que RockFace conoce para esa pestaña, de tres lugares:

* **RockFace** — los modelos que vienen con el programa (vea *Cómo funciona*);
* **Carpeta del hub** — una carpeta compartida por el equipo (una unidad de red, una carpeta sincronizada), elegida la
  primera vez que se hace clic en **Publicar en el hub**, o dada por la variable `ROCKFACE_AI_HUB`;
* **Proyecto** — los modelos entrenados en el proyecto o importados a él.

Seleccione una fila y use:

* **Ficha…** — qué es el modelo: tarea, entradas, clases, los datos con que fue entrenado y sus licencias, las
  métricas en datos reservados, su modelo padre (cuando fue ajustado) y su linaje, y el SHA-256 de la red;
* **Importar… / Exportar…** — un modelo como un archivo `.rfai`, para enviarlo a un colega o guardarlo;
* **Publicar en el hub** — el modelo escrito en la carpeta del hub como `<nombre>/<versión>.rfai`, con un
  `index.json` del hub; una versión nunca se sobrescribe;
* **Eliminar** — un modelo del proyecto (con una línea en la auditoría);
* **Comparar** — las fichas de las filas seleccionadas lado a lado (métricas, datos, padre).

## Opciones

| Campo | Qué cambia |
|---|---|
| Opción (setup) | Qué paquetes se instalan y qué dispositivo corre los modelos |
| `ROCKFACE_AI_DEVICE` | El dispositivo sin la interfaz (`cpu`, `cuda`, `directml`, `coreml`) — para scripts y trabajos |
| `ROCKFACE_AI_HUB` | La carpeta del hub sin la interfaz |

## Cómo funciona

* **Dos capas, instaladas por separado.** Aplicar un modelo usa ONNX Runtime (licencia MIT; extra `ai`), cuyos
  proveedores de ejecución corren la misma red en el procesador, en CUDA, en DirectML o en Core ML; el procesador es
  siempre la alternativa. Entrenar usa PyTorch (licencia BSD; extra `ai-train`) en el procesador, CUDA o el MPS de
  Apple.
* **Un modelo es dato, nunca código.** Un archivo `.rfai` es un zip con `model.onnx` (la red, formato ONNX) y
  `card.json` (su ficha). La ficha guarda el SHA-256 de la red, verificado en cada lectura: un archivo modificado se
  rechaza. Los modelos nunca son objetos Python serializados (pickle).
* **Versiones y linaje.** Cada modelo tiene nombre y versión; ajustar un modelo hace la versión siguiente, con el
  modelo de origen como padre; el mismo nombre y versión no se pueden guardar dos veces.
* **Los modelos que vienen con el programa** se entrenaron sólo con datos cuya licencia lo permite — los datos
  sintéticos de RockFace (verdad exacta) y datos abiertos bajo CC BY 4.0 u ODC-BY — y cada ficha declara los datos y
  las métricas medidas en datos que el modelo no vio. Los datos bajo licencias no comerciales o de compartir igual se
  usan sólo en pruebas internas, nunca para entrenar un modelo distribuido.

## Desde un script

```python
info = prj.ai_hardware()              # hardware, opciones (la recomendada marcada), dispositivo, paquetes
for m in prj.ai_models():             # todos los modelos: origen, nombre, versión, tarea, licencia, métricas
    print(m["name"], m["version"], m["metrics"])
m = prj.ai_model("rockface-thinsection-pores")      # la versión más nueva, donde esté
prj.ai_export(m, "pores.rfai"); rid = prj.ai_import("pores.rfai")
prj.ai_publish(rid, "//servidor/rockface-hub"); print(prj.ai_lineage(rid))
```

## Límites y problemas comunes

* "RockFace IA no está instalado": ejecute `rockface ai setup` (o `pip install -e ".[ai]"` desde el código).
* "El entrenamiento necesita el extra ai-train": aplicar modelos funciona; entrenar necesita PyTorch
  (`pip install -e ".[ai-train]"`).
* En Linux, el paquete PyTorch de PyPI trae las bibliotecas CUDA (unos 3 GB). Para una computadora sólo con
  procesador, instálelo desde el índice CPU de PyTorch
  (`pip install torch --index-url https://download.pytorch.org/whl/cpu`).
* Una tarjeta que no aparece: actualice su driver; en Windows la opción DirectML funciona con cualquier tarjeta
  DirectX 12.

## Cobertura

L13 (hub de modelos), GT18 / GV19 (los modelos preentrenados y la elección del modelo para el hardware encontrado) y
la instalación de la IA de la etapa 0.26 del ROADMAP.

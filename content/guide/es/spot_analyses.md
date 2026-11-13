# Análisis puntuales: geoquímica, datación e inclusiones fluidas

## Para qué sirve

Un **análisis puntual** es una medida hecha en un punto de la lámina: un análisis por ablación láser o microsonda, una
fecha U-Pb, una microtermometría de inclusiones fluidas. RockFace Atlas guarda cada punto en su lugar en el sistema de
la lámina, con sus valores e incertidumbres, el mineral analizado y una foto del área; así el punto se dibuja en el
mismo lugar en todas las imágenes de la lámina, puede volver a encontrarse en el instrumento y se alcanza desde una
consulta o una figura.

## Antes de empezar

* Una descripción guardada cuya lámina esté en Atlas, con una imagen calibrada.
* Para tablas de laboratorio: un archivo CSV con el nombre del punto, x e y, y las columnas de valores.

## Paso a paso

### Añadir un punto a mano

1. En RockFace Atlas, elija la herramienta **Punto** y haga clic donde se hizo el análisis — o **Nuevo…** en la
   pestaña **Puntos**.
2. En **Análisis puntual**, dé el **Tipo** (geoquímica, datación, inclusión fluida, otro), el nombre del **Punto** (dado
   en orden — G01, D01, FI01… — cuando queda vacío), la **Posición (x, y)**, el **Tamaño del punto**, **Método**,
   **Laboratorio**, **Fecha** y **Analista**.
3. El **Mineral** analizado y su **Localización**, de la nomenclatura.
4. **Valores**: **Añadir valor** para cada uno — **Nombre**, **Valor**, **±**, **Nivel** (1s, 2s), **Unidad**, **< LD**
   (bajo el límite de detección). **Campos usuales del tipo** completa los nombres usuales (razones U-Pb, Th y Tm
   hielo…).
5. **Metadatos** (**Añadir metadato**) para lo demás; **Foto del área** liga una foto de detalle; **Notas**.
   **Aceptar**.

### Importar una tabla de laboratorio

1. En la pestaña **Puntos**, **Importar tabla…**.
2. Elija el CSV y las **Coordenadas de la tabla**: sistema de la lámina (mm o µm), píxeles de una imagen calibrada, o
   un marco de instrumento (abajo).
3. **Tipo (si la tabla no lo trae)**.
4. RockFace lee las filas ("N filas; M con errores quedarán fuera") y muestra cada **Línea** con sus **Problemas**. Las
   columnas de valores como `Sr (ppm)` toman la unidad del encabezado; la incertidumbre viene en una columna `±`, `2s`,
   `err` o llamada `Sr 2s`; `<0.5` está bajo el límite de detección; las columnas de texto pasan a ser metadatos.
5. **Aceptar**.

### Marcos de instrumento: volver a encontrar un punto

1. **Marcos…** abre **Marcos de instrumento de la lámina**. Dé el nombre del **Instrumento** y **Su unidad**.
2. Lea las mismas marcas — fiduciales, rayas, esquinas de granos — en el instrumento (**Instrumento x, y**, o **Leer la
   platina**) y en la imagen de la lámina (**Lámina x, y (mm)**). **Añadir marca** para cada una; dos marcas bastan
   para una semejanza, tres para una transformación afín, una cuarta comprueba las demás.
3. **Ajustar**: el RMS de las marcas y el error dejando una fuera.
4. Después, **Platina al punto** envía la platina a un punto seleccionado, en las coordenadas del propio instrumento.
   Calibre de nuevo después de volver a colocar la lámina en el soporte.

### Ver los puntos

* La pestaña **Puntos** los lista por tipo (**Mostrar**: **Todos los tipos** o uno), con sus valores. **Mostrar**
  centra el visor en un punto; **En la imagen** los dibuja; **Editar…**, **Eliminar**.
* **Foto del área…** añade o abre la foto del área del punto.
* **Exportar CSV…** — una fila por punto, una columna por valor con su incertidumbre.
* **Figura de los puntos** — la lámina con los puntos etiquetados, los **Puntos contados de:** una descripción, y
  **Con el mapa mineralógico (si está registrado)**; **Guardar figura…**.

## Opciones

| Campo | Qué es |
|---|---|
| Nivel | El nivel de la incertidumbre: 1s o 2s. |
| < LD | Bajo el límite de detección (el valor es el límite). |
| Coordenadas de la tabla | mm, µm, píxeles de una imagen, o un marco de instrumento. |

## Cómo funciona

Los puntos se guardan en milímetros del sistema de la lámina, nunca solo en las coordenadas del instrumento: un marco
de instrumento es una transformación (semejanza o afín) ajustada sobre marcas, de modo que el mismo punto se encuentra
en cualquier instrumento que tenga su marco. Algunos valores se derivan y se muestran (nunca se guardan), cada uno con
su fuente: la salinidad de una inclusión fluida a partir del Tm hielo (Bodnar 1993) y la edad ²⁰⁶Pb/²³⁸U a partir del
²³⁸U/²⁰⁶Pb (constante de decaimiento de Jaffey et al. 1971, sin corrección de plomo común). Los puntos U-Pb se datan
juntos en RockFace Explorer (página [Datación U-Pb en el diagrama de Tera-Wasserburg](dating.md)).

## Desde un script

```python
d = prj["TS-9"]
d.calibrate_frame("LA-ICP-MS stage", [((41250, 18630), (1.0, 1.0)), ((57240, 18965), (17.0, 1.0)),
                                      ((41020, 29380), (1.0, 11.75))], unit="um")
d.import_spots("TS-9_U-Pb.csv", coords="frame", frame="LA-ICP-MS stage", kind="dating")
fi = d.add_spot("fluid_inclusion", 4.184, 3.488, values=[rf.Value("Th", 118.5, 1.0, "°C", "1s"),
                                                         rf.Value("Tm ice", -12.3, 0.2, "°C", "1s")],
                method="microthermometry", constituent="quartz_dia")
print(rf.spots.derived(fi))                              # salinidad 16,24 % en peso NaCl eq. (Bodnar 1993)
print(d.to_frame("LA-ICP-MS stage", fi.x_mm, fi.y_mm))   # dónde está en el instrumento
d.spot_figure("TS-9_puntos.png")
```

## Límites y problemas comunes

* "Esta lámina no tiene marco de instrumento: añada uno con Marcos… (marcas fiduciales)."
* Se rechaza un nombre ya usado en la lámina; los valores implausibles (un ppm negativo, rho fuera de −1…1) solo dan
  aviso.
* La edad U-Pb derivada no tiene corrección de plomo común: use la datación de Explorer para edades.

## Cobertura

L3 (enlaces con los análisis puntuales, con fotos de las áreas analizadas), L12 en parte (análisis puntuales con
imágenes de detalle y datación).

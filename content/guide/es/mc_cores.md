# RockFace MC: testigos enteros y fotos de cajas de testigos

## Para qué sirve

La pestaña **Testigos** procesa por lotes las tomografías de testigos enteros de un pozo: cada testigo se encuentra en
su tubo (liner) y se centra, recibe su pozo y profundidad, se orienta (por la estratificación del primer testigo o por
un perfil de imagen del pozo), se mueve y gira, se desenrolla como una imagen de su superficie externa, se pone como un
desenrollado del pozo y como un perfil de TC, se rellenan sus fracturas, y se exporta. Las fotografías de cajas de
testigo se cortan en sus testigos y se ponen por profundidad como una sola tira del pozo.

## Antes de empezar

* Las tomografías importadas como volúmenes de gris de una muestra del pozo (página [RockFace MC: volúmenes de micro-CT — importación, vistas y procesamiento](mc_volumes.md)).
* La profundidad del tope del primer testigo y el diámetro del testigo; opcionalmente, una tabla del tope y la base de
  cada testigo (CSV).
* Para orientar por un perfil de imagen: el perfil de imagen del pozo (página [RockFace MC: perfiles de imagen](mc_image_logs.md)).

## Paso a paso

### Procesar las tomografías

1. Abra **Testigos**. En **Tomografías de la muestra**, marque las tomografías.
2. **Pozo**, **Tope del primer testigo**, **Diámetro del testigo**; **Límites (CSV)** (opcional: tope y base de cada
   testigo, en m).
3. **Corregir la atenuación radial (endurecimiento del haz)** si el testigo es más claro en el borde.
4. **Procesar los testigos**. "Buscando y centrando los testigos…", luego "N testigo(s) procesado(s)". Cada testigo
   muestra "Testigo de …: tope–base m, … mm, rotación …°, desplazamiento … m".

### Orientación y posición

1. **Orientar por**: **estratificación del primer testigo** (los demás girados para seguirlo), o **un perfil de
   imagen del pozo** (elija el **Perfil de imagen**).
2. **Orientar los testigos marcados**. "Rotaciones: …".
3. A mano: **Desplazamiento en profundidad** y **Rotación**, luego **Mover y girar el testigo**.

### Desenrollado y perfiles

1. **Profundidad radial** (a qué profundidad, dentro de la superficie, se lee el desenrollado), luego **Desenrollar el
   testigo**: una imagen de la superficie externa, profundidad hacia abajo, azimut de lado, puesta en los perfiles del
   pozo.
2. **Diámetro del pozo** y **Desenrollado del pozo**: los testigos marcados como un desenrollado del pozo, al diámetro
   del pozo.
3. **Perfil de TC**: el valor medio de TC por profundidad, como una curva del pozo.

### Relleno, exportación, flujo

* **Fracturas (volumen segmentado)** y **Rellenar las fracturas**: las fracturas de un testigo segmentado rellenadas
  corte a corte.
* **Exportar los testigos marcados…**: un resumen HTML, la matriz CSV y la forma de Techlog con profundidad, el
  desenrollado en PNG, el volumen en TIFF. "N archivos escritos en …".
* **Flujo de testigo: testigo → segmentación**: importación → testigo → recorte → segmentación y porosidad, de una vez.

### Fotografías de cajas de testigo

1. En **Fotografías de cajas de testigo**, **Añadir fotografías…** y dé a cada una su **Tope (m)** y **Base (m)**.
2. **Canales por caja** (filas de testigos en una caja), o **automático**.
3. **Formar la tira**: las filas de testigos se encuentran por el color del fondo, se cortan y se ponen una tras otra
   por profundidad como una sola tira del pozo.

## Opciones

| Opción | Qué cambia |
|---|---|
| Corregir la atenuación radial | Quita el aclarado del borde causado por el endurecimiento del haz. |
| Orientar por | La estratificación del primer testigo, o un perfil de imagen. |
| Profundidad radial | Profundidad dentro de la superficie a la que se lee el desenrollado (mm). |
| Canales por caja | El número de filas de testigos en cada foto de caja. |

## Cómo funciona

* El tubo y el testigo se encuentran como círculos en los cortes; en el pozo ILUSTRATIVO, el radio del testigo se
  encontró en 49,6–49,7 mm para 50 mm, y en una tomografía real de testigo entero (prueba interna) el testigo dentro
  del tubo en 130,4 mm.
* La orientación por la estratificación ajusta la sinusoide dominante del desenrollado de cada testigo; por un perfil
  de imagen, correlaciona los gradientes de profundidad del desenrollado y del perfil: dentro de 0,1° y 2 mm en el
  pozo ILUSTRATIVO.
* Las fotos de cajas de testigo formaron una tira exacta en el pozo ILUSTRATIVO.

## Desde un script

```python
scans = prj["TS-9"].volumes()                                 # las tomografías de la muestra, de tope a base
cores = [prj.process_core(v, 2500.0 + 0.9 * k, 100.0, well="W-1") for k, v in enumerate(scans)]
print(cores[0].core["diameter_mm"], cores[0].core["top_m"])
prj.orient_cores(cores, "sinusoid")                            # o "image_log", log=prj.log("AMP")
unwrap = cores[0].unwrap(radial_depth_mm=1.0)
well_unwrap = prj.well_unwrap(cores, well_diameter_mm=216)
ct = prj.ct_log(cores)
prj.export_cores(cores, "testigos")
strip = prj.load_core_photos("W-1", [("caja1.jpg", 2500.0, 2503.0), ("caja2.jpg", 2503.0, 2506.0)])
```

## Límites y problemas comunes

* "Marque al menos una tomografía o un testigo."
* "Indique el tope y la base de cada fotografía."
* Un testigo pegado al tubo puede encontrarse como el tubo: revise el diámetro mostrado, y dé el diámetro del testigo.

## Cobertura

GC1 (multitestigo), GC2 (cargador de fotos de testigo), GC3 (recorte), GC4 (transformaciones de multitestigo), GC5
(segmentación), GC6 (relleno de testigo), GC7 (exportación), GC8 (flujos), GI2 (desenrollados de testigos
procesados).

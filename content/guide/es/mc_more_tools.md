# MC → Más: copas, mapa de distancias, vigilancia de carpeta, reconstrucción, cambio de escala y flujo bifásico

## Para qué sirve

Herramientas encontradas en la auditoría del código de GeoSlicer: calibrar los valores de gris con **copas de
referencia**, medir la **distancia** al borde de un segmento, importar tomografías de una **carpeta** mientras el
tomógrafo las escribe, **reconstruir** una adquisición SkyScan, llevar medidas del testigo a las muestras de
profundidad de un **LAS** y medidas de plugs **a lo largo del testigo**; en los perfiles de imagen, segmentar un
**intervalo de profundidad** y trazar un nivel a través de la costura 0/360°; simular **flujo bifásico** en un
volumen segmentado con LBPM.

## Antes de empezar

Una muestra con volúmenes (MC), o un pozo con perfiles de imagen.

## Paso a paso

1. **MC → Más → Copas de referencia**: abra la tomografía con el plug y las copas de teflón, cuarzo y aluminio;
   **Encontrar las copas alrededor del plug**; escriba los valores que deben tener; **Reescalar los valores de gris**
   (un volumen nuevo).
2. **Mapa de distancias**: en un volumen segmentado elija el segmento; **Distancia al borde del segmento (µm)**.
3. **Vigilar una carpeta**: elija la carpeta de salida del tomógrafo; **Empezar a vigilar**: cada tomografía que dejó
   de crecer se importa; los nombres numerados forman una secuencia en el tiempo.
4. **Reconstrucción (FDK)**: una carpeta SkyScan (proyecciones y `.log`); **Reconstruir**.
5. **Flujo bifásico (LBPM)**: abra un volumen segmentado; indique los segmentos del fluido A (etiqueta 1 de LBPM) y
   del fluido B (etiqueta 2), los componentes sólidos que mojan de otro modo, la afinidad de mojado del sólido y la
   malla de procesos; **Escribir el caso** (la carpeta, el comando y un script de SLURM `run_lbpm.sh`), o
   **Ejecutar aquí como trabajo** / **Ejecutar en el ordenador remoto** (el ordenador de MC → Multiescala →
   Trabajos (lote y remotos)); **Leer los resultados** muestra los puntos finales y las curvas.
6. El cambio de escala a LAS, del plug al testigo y las herramientas de perfiles están en la API (abajo).

## Cómo funciona

* Copas: se encuentra el cilindro del plug, los vóxeles alrededor se separan con un Otsu de cuatro clases (aire y las
  tres referencias) y k-medias 1-D; el reescalado es la recta de mínimos cuadrados por las referencias.
* Distancia: la transformada de distancia euclidiana con el vóxel de cada eje.
* Vigilancia de carpeta: un conjunto se importa cuando su tamaño y su hora son los mismos en dos miradas.
* Reconstrucción: Feldkamp–Davis–Kress para haz cónico en órbita circular (Feldkamp et al. 1984; Kak & Slaney 1988) y
  retroproyección filtrada para haz paralelo, en NumPy (la de GeoSlicer usa ASTRA, GPL, que RockFace no puede
  distribuir); atenuación en 1/mm.
* LAS: la media de los valores del testigo dentro de la ventana de cada muestra del LAS; del plug al testigo: un
  bosque aleatorio (o ajuste lineal) de los valores de los plugs sobre los atributos de CT del testigo, verificado por
  dejar-uno-fuera antes de usarlo.
* Perfiles: un intervalo de profundidad escrito como segmento; el trazado de nivel crece la región de valores
  parecidos desde una semilla, conectada a través de la costura de un perfil de vuelta completa.
* Flujo bifásico: LBPM (McClure et al. 2021; GPL-3.0, por eso RockFace no lo contiene — ejecuta la instalación del
  propio usuario). El caso: el volumen como el RAW de 8 bits de LBPM (x más rápido) y el `input.db`, con el `Domain`
  escrito de acuerdo — tamaño, malla de procesos y subdominios, vóxel en µm, los segmentos asignados a 0 (sólido), 1,
  2 y etiquetas negativas para los componentes sólidos con su `ComponentAffinity`; las demás secciones vienen de la
  documentación de LBPM (modelo de color, protocolo de flujo fraccional). Los resultados: `timelog.csv`
  (permeabilidad relativa frente a la saturación) y `subphase.csv` (saturación por los volúmenes de las fases
  conectadas y desconectadas, presión capilar pn − pw, área interfacial, característica de Euler), como los lee el
  Pore Scale Modelling de GeoSlicer.

## Desde un script

```python
c = rf.gs_tools.cups(prj.raw, vol_id); rf.gs_tools.remap(prj.raw, vol_id, c.medians, {"teflon": 1000, "aluminium": 3000})
rf.gs_tools.distance_map(prj.raw, labels_id, 1)
vol, voxel_um = rf.gs_tools.reconstruct_skyscan("carpeta_de_adquisicion")
rf.gs_tools.upscale_to_las(prof, porosidad, "pozo.las", "salida.las", compare="PHIT")
rf.gs_tools.plug_to_core(prof_testigo, atributos, prof_plugs, porosidad_plugs)
rf.log_edit.fill_depth_range(prj.raw, log_id, 1001.0, 1001.2, 2)
rf.log_edit.level_trace(prj.raw, grey_id, labels_id, azimuth=10, depth=1000.5, tolerance=10, value=3)
res = prj.lbpm(labels_id, {1: "fluid_a", 2: "fluid_b"}, "caso-lbpm", nproc=(2, 2, 1))   # requiere LBPM instalado
prj.lbpm(labels_id, {1: "fluid_a"}, "caso-lbpm", run=False)       # solo el caso y el comando
```
`rockface notebook proyecto.rockface` escribe un cuaderno Jupyter que abre el proyecto con la API.

## Límites y problemas comunes

* La reconstrucción espera proyecciones ya corregidas por campo claro (como las escribe SkyScan) y el eje de rotación
  centrado.
* Del plug al testigo necesita plugs que cubran el rango del testigo; el error de dejar-uno-fuera dice cuánto confiar.
* LBPM debe estar instalado donde corre el trabajo (aquí, en el ordenador remoto o en el clúster); cada tamaño del
  volumen debe ser divisible por la malla de procesos. Las presiones están en unidades de red.

## Cobertura

Auditoría de GeoSlicer de 0.28 (GV20–GV28, GI12–GI13).

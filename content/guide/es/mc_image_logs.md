# RockFace MC: perfiles de imagen

## Para qué sirve

La pestaña **Perfiles** guarda los perfiles de imagen de un pozo — amplitud acústica y tiempo de tránsito,
resistividad, conductividad, desenrollados de testigo, perfiles de TC — con sus curvas, en un solo eje de
profundidad. Importa y exporta los formatos usuales, los recorta y procesa (excentricidad, filtro de espiral, calidad y
heterogeneidad, corrección de azimut, CLAHE), rellena sus huecos, los segmenta en vúgulos con sus tamaños por
profundidad, ajusta las sinusoides de rasgos planares y pone desenrollados de testigo sobre el perfil de imagen.

## Antes de empezar

* Los archivos de perfil: LAS 2.0 (con curvas de imagen apiladas), CSV (matriz, Techlog, forma larga; también gzip),
  NetCDF o mallas GMT, DLIS (con el extra opcional `dlis`), una imagen con las profundidades del tope y la base, o una
  carpeta de desenrollados de testigo.
* El nombre del pozo; el diámetro del pozo, para longitudes en milímetros.

## Paso a paso

### Importar

1. Abra **Perfiles**. **Archivo o carpeta** (LAS, CSV, NetCDF/grd, DLIS, imagen, carpeta de desenrollados).
2. **Pozo**, **Diámetro del pozo**, **Medida** (amplitud acústica, tiempo de tránsito, resistividad, conductividad, TC,
   fotografía, otra); para una imagen, su **Tope y base de la imagen**.
3. **Importar**. "N perfil(es) importado(s)." Los pozos y sus perfiles aparecen en el panel izquierdo; las pistas se
   muestran lado a lado en un solo eje de profundidad, con una **Paleta**.

### Recorte y procesamiento

1. **Profundidades** y **Recortar**.
2. **Proceso** — elija uno, con sus parámetros, y luego **Aplicar**:
   * **Excentricidad** — corrige la amplitud de una herramienta fuera del centro del pozo, usando el **Perfil de
     tiempo de tránsito**;
   * **Filtro de espiral** — quita el patrón en espiral de la herramienta (**Longitud de onda mínima** y **máxima
     (m)**); "Filtrado: cambió el …% de la imagen";
   * **Indicador de calidad** e **Índice de heterogeneidad** — curvas por profundidad (**Ventana (m)**);
   * **Corrección de azimut** — gira la imagen por una **Curva de desvío de azimut**;
   * **CLAHE** — contraste local (**Límite de recorte**).

### Registro del desenrollado y relleno

1. **Desenrollado del testigo** y **Mayor desplazamiento**, luego **Colocar el desenrollado sobre el perfil**:
   "Desenrollado movido … m y girado …° (correlación …)".
2. **Relleno**: **lineal (fila por fila)**, **armónico (suave)** o **biarmónico**; **Rellenar también (perfil
   segmentado)** para una máscara; **Rellenar los huecos** — los huecos entre los patines de la herramienta y las
   zonas enmascaradas se rellenan.

### Segmentación, objetos y tamaños de poro

1. **Cortes** (vacío: Otsu), luego **Segmentar**.
2. **Objetos**: los vúgulos como objetos a través de la unión de 0/360° (**Objeto más pequeño**): "N objetos; diámetro
   equivalente medio … mm, mayor … mm", con su tabla.
3. **Tamaños de poro**: el espesor local del espacio poroso en mm y sus histogramas por **Intervalo de profundidad**.

### Rasgos planares

1. **Marcar puntos**: haga clic en al menos tres puntos de un plano de estratificación o fractura en la pista de la
   imagen.
2. **Ajustar la sinusoide**: "Plano en … m: buzamiento …° hacia …°".
3. **Fábrica dominante**: la sinusoide dominante de las profundidades en pantalla.

### Exportar

**Exportar…** escribe LAS, CSV (matriz o Techlog), NetCDF, PNG/TIFF o DLIS (con el dliswriter opcional).

## Opciones

| Opción | Qué cambia |
|---|---|
| Medida | Qué es el perfil; amplitud y tiempo de tránsito van juntos para la excentricidad. |
| Relleno | Lineal (rápido), armónico (suave), biarmónico (sigue los gradientes). |
| Objeto más pequeño | Los vúgulos menores que esto quedan fuera. |

## Cómo funciona

* Los perfiles se guardan por profundidad con una pirámide; así, los pozos largos se muestran al instante.
* En el pozo ILUSTRATIVO (capas inclinadas y vúgulos de verdad conocida): fábrica dominante 25,0°/120,0° exacta; un
  patín oculto rellenado con RMSE 0,043–0,050 frente a 0,083 de la media de la fila; 38 de 40 vúgulos encontrados.
* En un perfil FMI real (prueba interna): un patín oculto rellenado con RMSE 14,97 (lineal) frente a 29,07 de la media
  de la fila; dos pasadas coincidentes dentro de 0,8 mm.
* Editar segmentaciones de perfil con el pincel y revisar objetos: página [Editar la segmentación de un perfil y sus objetos](log_editing.md); modelo de permeabilidad de
  perfiles segmentados: página [Modelo de permeabilidad de perfiles de imagen](permeability_model.md).

## Desde un script

```python
amp, tt = prj.import_log("amplitude.las", "W-1", diameter_mm=216)[:2]
(fixed, tau, _), = amp.eccentricity(tt)
clean, changed = fixed.inpaint(method="biharmonic").spiral_filter(4, 20)
print(clean.dominant_sinusoid(2501, 2510).dip_deg)
vugs, table = clean.segment().objects(min_px=6)
table.to_csv("vugulos.csv")
clean.export("limpio.las")
```

## Límites y problemas comunes

* "Elija un archivo o carpeta."
* "Ningún perfil que mostrar." — el pozo aún no tiene perfiles, o ninguno en las profundidades mostradas.
* DLIS necesita el extra `dlis` (dlisio, LGPL, cargado solo cuando se usa).

## Cobertura

GI1 (importación), GI2 (desenrollado), GI3 (exportación), GI4 (recorte), GI5 (procesamiento), GI6 (registro del
desenrollado), GI7 (relleno), GI8 (segmentación, rasgos planares), GI9 (distribución de tamaños de poro).

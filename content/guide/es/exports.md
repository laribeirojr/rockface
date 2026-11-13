# Exportar pozos a WITSML y muestras a OSDU

## Para qué sirve

* **WITSML** (Energistics) es el formato de datos de pozo que leen los programas de modelado de yacimientos y de
  datos de pozo. Con él, la petrografía de las muestras, y los perfiles de imagen y las curvas de RockFace MC,
  quedan junto a los demás perfiles del pozo.
* **OSDU** es la plataforma abierta de datos de la industria energética. Su manifiesto permite cargar en una
  plataforma OSDU los pozos, muestras, láminas, descripciones, análisis de laboratorio e imágenes de un proyecto,
  incluido el servicio de muestras de roca y fluido (RAFS).

## Antes de empezar

* **Para WITSML:** las muestras necesitan pozo y profundidad. Las curvas son las de la exportación LAS de Explorer.
* **Para OSDU:** pida al gestor de datos de la plataforma la **partición de datos** y la **etiqueta legal** a usar.

## Paso a paso

### WITSML

1. En RockFace Petro, elija **Inicio → Informes e intercambio → Exportar WITSML**.
2. Elija una carpeta. RockFace escribe, para cada pozo:
   * `<pozo>_well.xml` y `<pozo>_wellbore.xml`: el pozo y su trayectoria;
   * `<pozo>_samples_log.xml`: una fila por profundidad de muestra, con porosidad y permeabilidad de laboratorio,
     densidad de granos, porosidad visual y facies;
   * un `<pozo>_<perfil>_log.xml` por cada perfil de RockFace MC. Los perfiles de imagen se vuelven curvas de
     vector, un valor por azimut.
3. Cargue los archivos en el programa de destino como objetos well, wellbore y log de WITSML 1.4.1.1.

### OSDU

1. Elija **Inicio → Informes e intercambio → Exportar manifiesto OSDU**.
2. Elija el nombre del archivo y escriba la **partición de datos** y la **etiqueta legal**. Una etiqueta vacía
   escribe un marcador, a reemplazar antes de la carga.
3. Entregue el archivo JSON a la carga por manifiesto de la plataforma.

## Opciones

Desde un script o la línea de comandos puede elegir:

* las descripciones;
* las curvas del perfil de las muestras y la profundidad usada (medida, corregida, ajustada);
* si se incluyen los perfiles de MC y los perfiles de imagen;
* en OSDU, los grupos de acceso y los países.

## Cómo funciona

* **WITSML.** RockFace escribe WITSML 1.4.1.1 con código propio. El orden de los elementos sigue el esquema WITSML
  1.4.1.1. El índice es la profundidad medida en metros; los valores ausentes quedan vacíos, con `-999.25` como
  valor nulo.
* **OSDU.** Pozos y trayectorias se vuelven `master-data--Well` y `master-data--Wellbore`. Muestras y láminas se
  vuelven `master-data--Sample` (una lámina es una muestra hija de su muestra). Descripciones y análisis de
  laboratorio se vuelven `work-product-component--SamplesAnalysis`, e imágenes
  `work-product-component--SampleImage`.
  * La petrografía — composición con porcentajes, clasificaciones, los códigos de la nomenclatura de RockFace — va
    en `ExtensionProperties.RockFace`, porque OSDU todavía no tiene un esquema de petrografía.
  * La tabla de correspondencia está en `docs/SERVER.md`.

## Desde un script

```python
import rockface.api as rf
with rf.open("proyecto.rockface") as prj:
    prj.export_witsml("carpeta_witsml")
    prj.export_osdu("manifiesto.json", partition="mi-particion", legal_tag="mi-particion-legal")
```

O: `rockface export witsml proyecto.rockface carpeta` y `rockface export osdu proyecto.rockface manifiesto.json
--partition mi-particion --legal-tag mi-particion-legal`.

## Límites y problemas comunes

* **Validación de WITSML.** Los archivos se comprobaron releyéndolos, no contra los archivos oficiales del esquema.
  Si algún programa los rechaza, avise por el formulario de comentarios.
* **Versiones de los esquemas OSDU.** Las versiones usadas están escritas en el manifiesto. Si la plataforma usa
  otras, el gestor de datos puede tener que ajustarlas.
* **Imágenes.** Los registros de imagen de OSDU describen las imágenes; los archivos de imagen quedan en RockFace.
  Exporte las imágenes desde Atlas para adjuntarlas como conjuntos de datos.

## Cobertura

P38 (exportación WITSML), L13 (OSDU).

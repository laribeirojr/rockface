# Aprendizaje federado entre laboratorios

## Para qué sirve

Varios laboratorios entrenan **juntos un modelo del conteo de puntos**, y cada uno guarda sus imágenes, puntos y
descripciones. Solo los números del modelo salen de un laboratorio, en un archivo que puede leer antes de enviarlo. El
modelo compartido ayuda luego a los conteos de todos: con las **propuestas de IA** del conteo de puntos (1.0.0rc7)
propone el constituyente bajo un punto **desde el primer punto**, antes de que un conteo nuevo tenga los 15 puntos que
necesita su propio modelo.

## Antes de empezar

* Conteos con su imagen (pestaña Conteo de puntos → la imagen de la lámina), puntos contados y líneas cuyo
  constituyente está en la base de conocimiento de RockFace. La imagen con nícoles cruzados solo hace falta si la
  federación la pide.
* Al menos 50 puntos contados en los conteos que envíe (con menos puntos es más fácil recuperarlos de una
  actualización).
* Un laboratorio **coordina**: crea la federación y combina las actualizaciones. Cualquier laboratorio puede hacerlo.
* Un medio para intercambiar archivos pequeños (unos 55 kB cada uno): correo, carpeta compartida, disco — lo que
  cada institución permita. RockFace no envía nada por sí mismo.

## Paso a paso

**El coordinador — crear la federación.** Herramientas → **Aprendizaje federado** → *Coordinar*. Dé un nombre, el
número de rondas (20), las pasadas locales por ronda (2), la actualización máxima (5) y, si quiere, ruido (ver abajo).
**Crear la federación…** guarda `<nombre>-r1.rffed`. Envíelo a los laboratorios.

**Cada laboratorio — participar.** *Participar* → **Abrir una federación…** → el `.rffed` recibido. Escriba el nombre
que verán los demás (p. ej. *Lab A*), marque los conteos a usar y haga clic en **Preparar mi actualización**. RockFace
muestra **lo que sale de esta computadora — todo el archivo**: la federación, la ronda, el nombre del laboratorio, el
número de puntos, el cambio de los pesos del modelo (unos diez mil números), su tamaño y cómo le fue al modelo
compartido en el 20 % de sus propios puntos reservados, antes y después de sus pasadas. Debajo, **lo que queda aquí**:
sus puntos por constituyente. **Guardar la actualización…** y envíe el `.rfupd` al coordinador.

**El coordinador — la próxima ronda.** *Coordinar* → **Abrir una federación…** (el `.rffed` actual) → **Añadir las
actualizaciones de los laboratorios…** → **Combinar en la próxima ronda…** guarda `<nombre>-r2.rffed`. El historial
muestra cada ronda: los laboratorios con sus puntos y cuántos de sus puntos reservados acertó el modelo compartido
antes y después. Envíe el nuevo archivo a los laboratorios y repita.

**Todos — usarlo en el conteo.** *Usar en el conteo* → **Elegir el modelo compartido…** (el `.rffed` más reciente).
En la pestaña Conteo de puntos marque **Proponer el constituyente (IA)** y **Modelo compartido**: las propuestas llegan desde el
primer punto, marcadas *(modelo compartido)*; a medida que cuenta, su propio modelo aprende y los dos se mezclan — el
modelo compartido pesa como 30 de sus puntos, y cada vez menos (*este conteo y el modelo compartido*). Nada se cuenta
por usted: Enter acepta una propuesta, como en la 1.0.0rc7, y los puntos a ciegas siguen midiendo la coincidencia con
honestidad.

**Mio**: *"¿cómo va la federación?"* (*"status of the federated model?"*, *"como está a federação?"*) muestra el
modelo compartido en uso, sus rondas, los laboratorios de la última ronda y sus aciertos en los puntos reservados.

## Cómo funciona

* **El modelo.** Una red de una capa oculta sobre las mismas 45 características del asistente del conteo (color,
  dispersión, saturación, matiz, percentiles de brillo, bordes y resina azul en ventanas de 3 × 3 píxeles, 30 µm y
  90 µm alrededor del punto; 90 con la imagen con nícoles cruzados). Sus clases son **todos los constituyentes de la
  base de conocimiento incorporada** (106): una lista fija, así que la lista no dice nada de las rocas de nadie.
* **Cada imagen estandarizada por sí misma.** Antes de que el modelo vea un punto, cada característica se estandariza
  por la media y la dispersión de esa característica en todos los puntos de la malla de la misma imagen, contados o
  no. Eso quita el colorante, la lámpara y la cámara de cada laboratorio y no necesita estadísticas de nadie — la idea
  de mantener local la normalización (FedBN, Li et al. 2021).
* **Promedio federado.** En cada ronda cada laboratorio parte de los pesos compartidos, hace algunas pasadas sobre sus
  propios puntos y envía el cambio; el coordinador suma el promedio de los cambios, cada uno ponderado por su número de
  puntos (FedAvg, McMahan et al. 2017; el término proximal de FedProx está disponible por script, Li et al. 2020).
  Rondas por archivos fue como dos petroleras y una universidad hicieron una prueba federada con rocas
  digitales: los pesos viajaron por transferencia de archivos, y los modelos federados superaron al modelo propio de
  cada participante (Chang et al. 2024).
* **Verificaciones.** Se rechaza una actualización de otra federación, de otra ronda, hecha desde otra versión del
  modelo, de un laboratorio ya presente en la ronda, con un campo que no debería estar o con números no finitos. Cada
  archivo lleva una huella; un archivo modificado se rechaza.
* **Lo que protege y lo que no.** Imágenes, puntos, coordenadas, nombres y los constituyentes contados nunca salen.
  Pero los números de un modelo aún pueden decir algo de los datos de los que aprendió: los gradientes pueden
  invertirse (Zhu et al. 2019) y la pertenencia de un dato adivinarse (Shokri et al. 2017). Una actualización de
  cientos de puntos tras varias pasadas es mucho más difícil de invertir que un gradiente; la **actualización máxima**
  recorta las grandes, y el **ruido** hace cualquiera aún más difícil — con un precio: con dos laboratorios, ruido
  0,01 costó cerca de 1 punto de acierto, 0,02 seis, 0,05 quince (el ensayo abajo). Esto **no es una garantía formal
  de privacidad diferencial** por punto (eso exige recorte por punto y una contabilidad de privacidad, Abadi et al.
  2016), y el coordinador ve la actualización de cada laboratorio (la agregación segura, Bonawitz et al. 2017, no está
  implementada). Elija un coordinador en quien confíen todos los laboratorios.

**El ensayo (ILLUSTRATIVE).** Dos laboratorios inventados, cada uno con tres láminas contadas de unos 260 puntos, su
propio tono de color y la mayor parte de un constituyente sin contar (A casi no contó feldespato, B casi no contó
cemento); 20 rondas de 2 pasadas; aciertos en láminas nunca vistas (media de tres repeticiones,
`tools/bench_federated.py`):

| Modelo | Lab A | Lab B | Lab C (no participó) |
|---|---|---|---|
| Federado | 80 % | 83 % | 83 % |
| Todos los puntos juntos (solo posible con datos inventados) | 81 % | 84 % | 86 % |
| Solo Lab A | 76 % | 74 % | 79 % |
| Solo Lab B | 76 % | 78 % | 79 % |

Un conteo nuevo en el Lab C con el modelo compartido: 83 % de las propuestas correctas desde el primer punto; sin él,
ninguna propuesta antes de 15 puntos, 42 % a los 15, 71 % a los 30, 79 % a los 60 (y 83 % a los 60 con ambos).

## Desde un script

```python
rf.federation_create("areniscas-r1.rffed", "Areniscas", rounds=20)             # el coordinador
r = prj.federated_update("areniscas-r1.rffed", "lab-a.rfupd", site="Lab A")      # cada laboratorio
r["fields"]                                   # todos los campos del archivo que saldría
r["by_class"]                                 # lo que queda: puntos por constituyente
rf.federation_aggregate("areniscas-r1.rffed", ["lab-a.rfupd", "lab-b.rfupd"], "areniscas-r2.rffed")
rf.federation("areniscas-r2.rffed")["history"]
prj["ILL-TS-002"].assist(top=5, shared="areniscas-r2.rffed")   # propuestas con el modelo compartido
```

El módulo `rockface.core.federated` tiene las partes: `create`, `site_data`, `site_update`, `inspect`,
`check_update`, `aggregate`, `simulate`, `centralized`, `local_only`.

## Límites y problemas comunes

* El modelo es tan bueno como los conteos que lo respaldan: un constituyente que nadie cuenta nunca se propone, y uno
  contado con nombres distintos en dos laboratorios lo confunde. Las clases son los constituyentes de la base de
  conocimiento.
* Rocas muy distintas (una federación de carbonatos y un conteo de arenisca) dan propuestas pobres; la columna
  *Aciertos antes* del historial muestra cómo le va al modelo compartido en los puntos de cada laboratorio antes de
  aprender de ellos.
* Un conteo sin imagen, o sin la imagen con nícoles cruzados cuando la federación la pide, queda fuera.
* "Solo N puntos pueden enseñar al modelo": marque más conteos o cuente más puntos.
* Las propuestas del modelo compartido son propuestas: el petrógrafo cuenta, y Enter solo acepta lo que él ve.
* *Patentes.* Google tiene patentes de aprendizaje federado (p. ej. US 10,402,469 B2, US 11,120,102 B2,
  US 10,657,461 B2). RockFace promedia actualizaciones intercambiadas como archivos y no usa actualizaciones
  comprimidas o esbozadas ni optimizador adaptativo en el servidor; es una nota de diseño, no un dictamen jurídico
  (`docs/LICENSE_AUDIT.md`).

## Cobertura

O8 (pedido del propietario del 2026-11-17: las innovaciones, la sexta).

Referencias: McMahan et al. (2017), Communication-efficient learning of deep networks from decentralized data,
AISTATS, arXiv:1602.05629; Li et al. (2020), Federated optimization in heterogeneous networks (FedProx), MLSys,
arXiv:1812.06127; Li et al. (2021), FedBN, ICLR, arXiv:2102.07623; McMahan et al. (2018), Learning differentially
private recurrent language models, ICLR, arXiv:1710.06963; Abadi et al. (2016), Deep learning with differential
privacy, CCS, https://doi.org/10.1145/2976749.2978318; Zhu, Liu & Han (2019), Deep leakage from gradients, NeurIPS,
arXiv:1906.08935; Shokri et al. (2017), Membership inference attacks, IEEE S&P,
https://doi.org/10.1109/SP.2017.41; Bonawitz et al. (2017), Practical secure aggregation, CCS,
https://doi.org/10.1145/3133956.3133982; Kairouz et al. (2021), Advances and open problems in federated learning,
https://doi.org/10.1561/2200000083; Chang et al. (2024), Federated learning test for collaborative machine
learning, SCA2024-1036; RahimiZadeh et al. (2025), FTA-FTL: federated transfer learning for lithology microscopic
images, arXiv:2501.03349.

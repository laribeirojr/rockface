# Trabajos: cómputo por lotes y remoto

## Para qué sirve

Los cálculos largos de RockFace MC — permeabilidad por lattice Boltzmann, curvas Microtom en volúmenes grandes,
realizaciones MPS, extracciones de redes de poros, mapas de porosidad — pueden correr como **trabajos**: en otros
procesos de este ordenador, varios a la vez y sobre muchos volúmenes (lote), o en un **ordenador remoto** (una
estación de trabajo o un clúster con SLURM), mientras el programa queda libre. Cuando un trabajo termina, sus
resultados se traen al proyecto.

## Antes de empezar

* Para trabajos remotos: una cuenta SSH en el ordenador remoto que abra con sus claves (sin pedir contraseña), y
  RockFace instalado allí (la misma versión, o su carpeta de código fuente dada como ruta de Python). RockFace no guarda
  ninguna contraseña.

## Paso a paso

1. Abra el volumen (o el perfil) sobre el que trabaja el cálculo y vaya a la pestaña **Multiescala**, grupo
   **Trabajos**.
2. Elija el **Cálculo** y escriba sus **Parámetros (JSON)**, p. ej. `{"method": "permeability", "tol": 1e-5}` para una
   simulación Microtom. El volumen o el perfil abierto es la entrada.
3. Marque **Un trabajo por volumen de la muestra del mismo tipo (lote)** para correrlo sobre todos los volúmenes como
   este.
4. Para correr aquí: ajuste **Trabajos simultáneos aquí** y pulse **Ejecutar aquí**.
5. Para correr en remoto: escriba el **Ordenador remoto** (`usuario@host` o un alias de su configuración SSH), la
   **Carpeta allí / Python allí**, una **Línea de preparación** opcional (p. ej. `module load python`), el
   **Planificador / opciones** (*ninguno*: un proceso en segundo plano; *SLURM*: `sbatch` con opciones como
   `--time=02:00:00 --mem=16G`) y pulse **Enviar al ordenador remoto**.
6. La tabla sigue los trabajos (estado, progreso, tiempo, error); **Actualizar** vuelve a leer los estados (los trabajos
   remotos se copian de vuelta al terminar). Pulse **Traer los resultados** para añadir al proyecto lo que hizo el
   trabajo terminado más reciente; **Cancelar el trabajo** lo detiene.

## Opciones

| Campo | Qué cambia |
|---|---|
| Cálculo | Uno de: simulación Microtom, mapas de porosidad (segmentación, saturación), permeabilidad de Darcy de un mapa, realizaciones MPS, extracción de la red de poros, red de dos escalas, REV de permeabilidad de una red, modelo de permeabilidad de un perfil de imagen |
| Parámetros (JSON) | Los argumentos del cálculo, como en un script |
| Trabajos simultáneos aquí | Procesos que corren juntos; los demás esperan |
| Planificador / opciones | Proceso en segundo plano, o SLURM con opciones `#SBATCH` |

## Cómo funciona

Un trabajo es una carpeta junto al proyecto (`<proyecto>.jobs`): `job.json` (el cálculo, sus parámetros, sus
entradas), `input.rockface` (un proyecto pequeño solo con los objetos necesarios, con sus muestras y pozos), y luego
`status.json` y `result.json`, escritos por la ejecución. El cálculo es uno de una lista fija de funciones de RockFace
— nunca código enviado con el trabajo. Los trabajos remotos se copian con `scp`, se inician con `ssh` (o `sbatch`), se
siguen leyendo `status.json` y se copian de vuelta. Traer los resultados copia todo objeto que hizo el trabajo
(volúmenes, perfiles, redes, superficies) al proyecto, ligado a las mismas muestras y pozos, con el trabajo registrado
en su historial.

## Desde un script

```python
seg = prj.volume("plug segmentation")
job = prj.prepare_job("microtom", volume_id=seg.id, method="permeability")
prj.run_jobs([job], workers=2)
print(prj.bring_back(job))
host = rf.jobs.Host("me@cluster", workdir="/scratch/me/rf", scheduler="slurm", slurm="--time=04:00:00")
runner = rf.jobs.RemoteRunner(host)
runner.submit(prj.prepare_job("pnm_extract", volume_id=seg.id))
```

## Límites y problemas comunes

* "Permission denied (publickey)": la clave SSH no fue aceptada; abra una terminal y compruebe que `ssh usuario@host`
  funciona sin contraseña.
* Un trabajo remoto falla enseguida cuando RockFace no está allí: ajuste **Python allí** al Python que lo tiene, o la
  carpeta del código en la ruta de Python de un script (`Host(pythonpath=…)`).
* Los resultados se traen cuando usted lo pide, nunca se escriben en el proyecto sin su conocimiento.

## Cobertura

GM10 (cómputo remoto), GM9 (flujos multiescala) y el flujo remoto de la red de poros (GV12).

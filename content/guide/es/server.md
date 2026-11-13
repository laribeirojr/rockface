# Trabajar en equipo en un servidor

## Para qué sirve

Un equipo de petrógrafos describe al mismo tiempo la misma colección de muestras. En lugar de que cada uno guarde
un archivo de proyecto, todos se conectan a una única **base de datos en el servidor**. Cada uno ve lo que los
demás guardan, y nadie sobrescribe el trabajo de nadie. RockFace Petro, Atlas, Explorer, Lab y MC funcionan en el
servidor igual que en un archivo.

## Antes de empezar

* El administrador del equipo preparó el servidor (vea "Preparar un servidor", más abajo) y le dio:
  * la dirección y el puerto del servidor;
  * el nombre de la base de datos;
  * su usuario y su contraseña.
* Su computadora llega al servidor por la red. En una red de laboratorio esto suele funcionar. Entre redes
  distintas, pregunte al administrador por SSL.

## Paso a paso

### Conectarse

1. Abra RockFace Petro. En la página de inicio, o en **Inicio → Servidor**, elija **Conectar al servidor**.
2. Complete **Servidor**, **Puerto** (normalmente 5432), **Base de datos**, **Usuario** y **Contraseña**.
   * Dé un nombre a la conexión en **Conexión** (por ejemplo "Laboratorio").
   * Deje marcado **Recordar esta conexión**, para escribir la próxima vez solo la contraseña. RockFace nunca
     guarda la contraseña.
3. Opcional: pulse **Probar**. Aparecen su usuario y su **nivel**.
4. Pulse **OK**. El título de la ventana muestra `base@servidor — usuario (nivel)`.

### Su nivel

El nivel define lo que puede hacer. Lo asigna el administrador.

| Nivel | Usted puede |
|---|---|
| lector | leer todo, hacer consultas, figuras e informes |
| petrógrafo | además crear descripciones y modificar **las suyas**; añadir imágenes, análisis, volúmenes, perfiles |
| gestor | además modificar las descripciones **de cualquiera** y la base de conocimiento, y quitar bloqueos |
| administrador | además gestionar usuarios, niveles y contraseñas, y hacer copias de seguridad |

### Editar en equipo

* **Abrir una descripción.** Al abrir una descripción para editarla, RockFace la **bloquea** para usted.
* **Otra persona la está editando.** Si otra persona abre la misma descripción, verá un mensaje como "ILL-02 está
  siendo editada por alice (LAB-PC3) desde 10:42: abierta solo para lectura". Su botón Guardar queda apagado.
* **Descripción de otro autor.** Para un petrógrafo, se abre solo para lectura, con un mensaje que dice quién la
  escribió.
* **Cuándo se libera el bloqueo.** Al abrir otra descripción o al cerrar el programa.
  * Una computadora apagada, o que pierde la red, deja de renovar el bloqueo. Después de 10 minutos el bloqueo queda
    libre otra vez.
  * Un gestor puede quitar un bloqueo enseguida (Inicio → Servidor → Usuarios, bloqueos y auditoría →
    **Bloqueos**).
* **Modificada mientras tanto.** Si una descripción que usted tiene abierta fue modificada por otra persona
  mientras tanto (por ejemplo, un gestor que tomó un bloqueo), su guardado se rechaza: "Este registro fue
  modificado en otra estación desde que lo abrió". Abra la descripción de nuevo, vea los cambios y rehaga los
  suyos. RockFace nunca escribe sobre el trabajo de otra persona sin avisar.
* **Lo que hacen los demás.** Cada 15 segundos la barra de estado muestra el último cambio hecho por otra persona
  (por ejemplo "bob: create description:ILL-B2"), y el árbol de la izquierda se actualiza.

### Su perfil y su contraseña

**Inicio → Servidor → Usuarios, bloqueos y auditoría → Mi perfil**: su nombre, institución y correo, y **Cambiar
mi contraseña** (al menos 8 caracteres).

### La auditoría

**Usuarios, bloqueos y auditoría → Auditoría** lista todos los cambios: cuándo (UTC), quién, qué, en qué registro.

* Filtre por usuario, acción o parte del nombre del registro y pulse **Exportar CSV**.
* Nadie puede modificar ni borrar la auditoría, ni siquiera un gestor.

### Publicar un archivo de proyecto en el servidor

Para llevar un proyecto de un archivo al servidor, con sus descripciones, imágenes, análisis, volúmenes y perfiles:

1. Abra el archivo en RockFace Petro.
2. Elija **Inicio → Servidor → Publicar en el servidor**.
3. Pulse **Servidor y base de datos (como administrador)…** e indique la conexión de un administrador a una base
   **nueva y vacía**. Se crea y se prepara si todavía no existe.
4. En la tabla, indique para cada autor encontrado en el archivo el **usuario que tiene en el servidor**, para que
   siga editando sus descripciones.
5. Pulse **OK**. RockFace abre la copia del servidor.

### Copia de seguridad

* **Guardar proyecto como…** de un proyecto en el servidor escribe un archivo de proyecto (`.rockface`) completo, con todo.
* El administrador puede hacer lo mismo desde la línea de comandos (`rockface server backup`).

## Preparar un servidor (administrador)

1. En la computadora servidor, con Docker instalado, copie `docker/.env.example` a `docker/.env` y elija una
   contraseña larga en `ROCKFACE_ADMIN_PASSWORD`.
2. Inicie la base de datos: `docker compose up -d db` (en la carpeta `docker`).
3. Prepárela para RockFace:

   ```
   docker compose --profile admin build
   docker compose run --rm admin init "postgresql+psycopg://rockface_admin@db:5432/rockface"
   ```

4. Añada los usuarios:

   ```
   ROCKFACE_NEW_PASSWORD=… docker compose run --rm admin add-user "postgresql+psycopg://rockface_admin@db:5432/rockface" alice --role petrographer --name "Alice …"
   ```

   También puede añadir usuarios desde el programa: **Usuarios, bloqueos y auditoría → Usuarios → Añadir
   usuario**.
5. Haga copias de seguridad con regularidad:

   ```
   docker compose run --rm admin backup "postgresql+psycopg://rockface_admin@db:5432/rockface" /backups/rockface-AAAA-MM-DD.rockface
   ```

**Sin Docker:** use cualquier PostgreSQL 13 o posterior y una computadora con RockFace instalado
(`pip install ".[server]"`). Los comandos son los mismos, sin `docker compose run --rm admin`: por ejemplo
`rockface server init postgresql+psycopg://admin@servidor:5432/rockface`.

## Opciones

* **Cifrado (SSL)**: "según el servidor" (por defecto), *prefer*, *require* o *verify-full* (comprueba el
  certificado del servidor).
* **Contraseña vacía**: RockFace usa su archivo `pgpass` (`%APPDATA%\postgresql\pgpass.conf` en Windows,
  `~/.pgpass` en los demás sistemas).

## Cómo funciona

* **El servidor.** Es una base de datos PostgreSQL. Su usuario es un usuario de la base. Su nivel es el grupo al
  que pertenece: `rf_<base>_viewer`, `…_petrographer`, `…_manager` o `…_admin`.
* **Permisos.** El programa los comprueba antes de guardar, y la base de datos los comprueba otra vez con sus
  propios privilegios y políticas de seguridad por fila. Una descripción solo puede modificarla su autor o un
  gestor, sea cual sea el programa que escriba en la base.
* **Bloqueos.** Se guardan en la base de datos (tabla `edit_lock`).
* **Versiones.** Cada descripción tiene un número de versión. El guardado lleva la versión que se leyó y se rechaza
  si la base tiene una más nueva.
* **Más.** Vea `docs/SERVER.md` para los detalles y la prueba de aceptación.

## Desde un script

```python
import rockface.api as rf
with rf.connect("postgresql+psycopg://alice@servidor:5432/rockface") as prj:
    print(prj.user, prj.role)
    for entry in prj.audit(limit=10):
        print(entry["when"], entry["user"], entry["action"], entry["target"])
    prj.backup("copia.rockface")
```

## Límites y problemas comunes

* **"No se pudo conectar al servidor"**: revise la dirección, el puerto, el nombre de la base, su usuario y su
  contraseña, y que el servidor acepte su computadora (su `pg_hba.conf`).
* **"Solo puede leer esta base de datos"**: su nivel es lector; hable con el administrador.
* **"… fue escrita por …: solo su autor o un gestor puede modificarla"**: es la descripción de un colega. Pida a un
  gestor, o use **Guardar como…** (en el grupo Descripción) para hacer su propia copia.
* Imágenes, volúmenes y perfiles son registros compartidos: cuando dos personas modifican el mismo, vale el último
  guardado.

## Cobertura

P42 (versión servidor), R4 (almacenamiento central), L13 (contenedores).

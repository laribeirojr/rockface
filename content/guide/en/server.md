# Working together on a server

## What it is for

A team of petrographers describes the same collection of samples at the same time. Instead of each person
keeping a project file, everyone connects to one **server database**. Everyone sees what the others save, and
nobody overwrites anyone else's work. RockFace Petro, Atlas, Explorer, Lab and MC all work the same on a server as
on a file.

## Before you start

* The team's administrator has set up the server (see "Setting up a server" below) and given you:
  * the server address and port;
  * the database name;
  * your user name (login) and password.
* Your computer reaches the server over the network. On a laboratory network this usually works. Across networks,
  ask the administrator about SSL.

## Step by step

### Connecting

1. Open RockFace Petro. On the start page, or in **Home → Server**, choose **Connect to server**.
2. Fill in **Server**, **Port** (usually 5432), **Database**, **User** and **Password**.
   * Give the connection a name in **Connection** (for example "Laboratory").
   * Leave **Remember this connection** ticked, so next time you only type the password. RockFace never stores the
     password.
3. Optional: press **Test**. It shows your user and your **level**.
4. Press **OK**. The window title shows `database@server — user (level)`.

### Your level

Your level decides what you can do. The administrator sets it.

| Level | You can |
|---|---|
| viewer | read everything, run queries, figures and reports |
| petrographer | also create descriptions and change **your own**; add images, analyses, volumes, logs |
| manager | also change **anyone's** descriptions and the knowledge base, and remove locks |
| administrator | also manage users, levels and passwords, and back up |

### Editing together

* **Opening a description.** When you open a description for editing, RockFace **locks** it for you.
* **Someone else is editing it.** If another person opens the same description, they see a message like "ILL-02 is
  being edited by alice (LAB-PC3) since 10:42: opened read-only". Their Save button is off.
* **Another author's description.** It opens read-only for a petrographer, with a message saying who wrote it.
* **When the lock goes.** It is released when you open another description or close the program.
  * A computer that is switched off or loses the network stops renewing its lock. After 10 minutes the lock is
    free again.
  * A manager can remove a lock at once (Home → Server → Users, locks and audit → **Locks**).
* **Changed in between.** If a description you have open was changed by someone else in the meantime (for example
  a manager who took over a lock), your save is refused: "This record was changed on another workstation since you
  opened it". Open the description again, see the changes, and redo yours. RockFace never silently writes over
  someone else's work.
* **What the others do.** Every 15 seconds the status bar shows the last change made by someone else (for example
  "bob: create description:ILL-B2"), and the browser on the left is refreshed.

### Your profile and password

**Home → Server → Users, locks and audit → My profile**: your name, institution and e-mail, and **Change my
password** (at least 8 characters).

### The audit

**Users, locks and audit → Audit** lists every change: when (UTC), who, what, on which record.

* Filter by user, action or part of the record name, then **Export CSV**.
* Nobody can change or delete the audit, not even a manager.

### Publishing a project file to the server

To move a project from a file to the server, with its descriptions, images, analyses, volumes and logs:

1. Open the file in RockFace Petro.
2. Choose **Home → Server → Publish to server**.
3. Press **Server and database (as administrator)…** and give an administrator's connection to a **new, empty**
   database. It is created and prepared if it does not exist.
4. In the table, give each author found in the file the **login he or she has on the server**, so they keep
   editing their descriptions.
5. Press **OK**. RockFace opens the server copy.

### Backing up

* **Save project as…** of a server project writes a complete project file (`.rockface`) with everything in it.
* The administrator can do the same from the command line (`rockface server backup`).

## Setting up a server (administrator)

1. On the server computer, with Docker installed, copy `docker/.env.example` to `docker/.env` and choose a long
   password in `ROCKFACE_ADMIN_PASSWORD`.
2. Start the database: `docker compose up -d db` (in the `docker` folder).
3. Prepare it for RockFace:

   ```
   docker compose --profile admin build
   docker compose run --rm admin init "postgresql+psycopg://rockface_admin@db:5432/rockface"
   ```

4. Add the users:

   ```
   ROCKFACE_NEW_PASSWORD=… docker compose run --rm admin add-user "postgresql+psycopg://rockface_admin@db:5432/rockface" alice --role petrographer --name "Alice …"
   ```

   You can also add users from the program: **Users, locks and audit → Users → Add user**.
5. Back up regularly:

   ```
   docker compose run --rm admin backup "postgresql+psycopg://rockface_admin@db:5432/rockface" /backups/rockface-YYYY-MM-DD.rockface
   ```

**Without Docker:** use any PostgreSQL 13 or later and a computer with RockFace installed
(`pip install ".[server]"`). The commands are the same, without `docker compose run --rm admin`: for example
`rockface server init postgresql+psycopg://admin@server:5432/rockface`.

## Options

* **Encryption (SSL)**: "as the server decides" (default), *prefer*, *require* or *verify-full* (checks the
  server's certificate).
* **Empty password**: RockFace uses your `pgpass` file (`%APPDATA%\postgresql\pgpass.conf` on Windows,
  `~/.pgpass` elsewhere).

## How it works

* **The server.** It is a PostgreSQL database. Your login is a database user. Your level is the group it belongs
  to: `rf_<database>_viewer`, `…_petrographer`, `…_manager` or `…_admin`.
* **Rights.** The program checks them before saving, and the database checks them again with its own privileges
  and row-level security policies. A description can only be changed by its author or by a manager, whatever
  program writes to the database.
* **Locks.** They are kept in the database (table `edit_lock`).
* **Versions.** Every description has a version number. A save carries the version that was read, and is refused
  if the database has a newer one.
* **More.** See `docs/SERVER.md` for the details and the acceptance test.

## From a script

```python
import rockface.api as rf
with rf.connect("postgresql+psycopg://alice@server:5432/rockface") as prj:
    print(prj.user, prj.role)
    for entry in prj.audit(limit=10):
        print(entry["when"], entry["user"], entry["action"], entry["target"])
    prj.backup("copy.rockface")
```

## Limits and common problems

* **"Could not connect to the server"**: check the address, the port, the database name, your user and password,
  and that the server allows your computer (its `pg_hba.conf`).
* **"You can only read this database"**: your level is viewer; ask the administrator.
* **"… was written by …: only its author or a manager may change it"**: it is a colleague's description. Ask a
  manager, or use **Save as…** (in the Description group) to make your own copy.
* Images, volumes and logs are shared records: when two people change the same one, the last save wins.

## Coverage

P42 (server version), R4 (central storage), L13 (containers).

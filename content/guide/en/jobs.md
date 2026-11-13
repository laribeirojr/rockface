# Jobs: batch and remote computing

## What it is for

The long calculations of RockFace MC — lattice-Boltzmann permeability, Microtom curves on large volumes, MPS
realizations, pore-network extractions, porosity maps — can run as **jobs**: in other processes of this computer,
several at a time and over many volumes (batch), or on a **remote computer** (a workstation or a cluster with SLURM),
while the program stays free. When a job is done, its results are brought back into the project.

## Before you start

* For remote jobs: an SSH account on the remote computer that opens with your keys (no password prompt), and RockFace
  installed there (the same version, or its source folder given as the Python path). RockFace keeps no password.

## Step by step

1. Open the volume (or the log) the calculation works on and go to the **Multiscale** tab, group **Jobs**.
2. Choose the **Calculation** and type its **Parameters (JSON)**, e.g. `{"method": "permeability", "tol": 1e-5}` for a
   Microtom simulation. The volume or log open is the input.
3. Tick **One job per volume of the sample of the same kind (batch)** to run it over every volume like this one.
4. To run here: set **Jobs at a time here** and click **Run here**.
5. To run remotely: type the **Remote computer** (`user@host` or an alias of your SSH configuration), the **Folder
   there / Python there**, an optional **Setup line** (e.g. `module load python`), the **Scheduler / options**
   (*none*: a background process; *SLURM*: `sbatch` with options such as `--time=02:00:00 --mem=16G`), and click
   **Send to the remote computer**.
6. The table follows the jobs (state, progress, time, error); **Update** reads the states again (remote jobs are
   copied back when done). Click **Bring the results back** to add what the newest finished job made to the project;
   **Cancel the job** stops it.

## Options

| Field | What it changes |
|---|---|
| Calculation | One of: Microtom simulation, porosity maps (segmentation, saturation), Darcy permeability of a map, MPS realizations, pore network extraction, two-scale network, permeability REV of a network, permeability model of an image log |
| Parameters (JSON) | The arguments of the calculation, as in a script |
| Jobs at a time here | Processes running together; the others wait |
| Scheduler / options | Background process, or SLURM with `#SBATCH` options |

## How it works

A job is a folder next to the project (`<project>.jobs`): `job.json` (the calculation, its parameters, its inputs),
`input.rockface` (a small project with only the objects needed, with their samples and wells), then `status.json`
and `result.json` written by the run. The calculation is one of a fixed list of RockFace functions — never code sent
with the job. Remote jobs are copied with `scp`, started with `ssh` (or `sbatch`), followed by reading `status.json`
and copied back. Bringing back copies every object the job made (volumes, logs, networks, surfaces) into the project,
tied to the same samples and wells, with the job recorded in its history.

## From a script

```python
seg = prj.volume("plug segmentation")
job = prj.prepare_job("microtom", volume_id=seg.id, method="permeability")
prj.run_jobs([job], workers=2)
print(prj.bring_back(job))
host = rf.jobs.Host("me@cluster", workdir="/scratch/me/rf", scheduler="slurm", slurm="--time=04:00:00")
runner = rf.jobs.RemoteRunner(host)
runner.submit(prj.prepare_job("pnm_extract", volume_id=seg.id))
```

## Limits and common problems

* "Permission denied (publickey)": the SSH key is not accepted; open a terminal and check that `ssh user@host` works
  without a password.
* A remote job fails at once when RockFace is missing there: set **Python there** to the Python that has it, or the
  source folder in the Python path of a script (`Host(pythonpath=…)`).
* Results are brought back on demand, never written into the project behind your back.

## Coverage

GM10 (remote computing), GM9 (multiscale flows), and the remote workflow of the pore network (GV12).

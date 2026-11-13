# Trabalhos: computação em lote e remota

## Para que serve

Os cálculos longos do RockFace MC — permeabilidade por lattice Boltzmann, curvas Microtom em volumes grandes,
realizações MPS, extrações de redes de poros, mapas de porosidade — podem rodar como **trabalhos**: em outros
processos deste computador, vários de cada vez e sobre muitos volumes (lote), ou num **computador remoto** (uma
estação de trabalho ou um cluster com SLURM), enquanto o programa fica livre. Quando um trabalho termina, os seus
resultados são trazidos para o projeto.

## Antes de começar

* Para trabalhos remotos: uma conta SSH no computador remoto que abre com as suas chaves (sem pedir senha), e o
  RockFace instalado lá (a mesma versão, ou a sua pasta de código-fonte dada como caminho do Python). O RockFace não
  guarda nenhuma senha.

## Passo a passo

1. Abra o volume (ou o perfil) sobre o qual o cálculo trabalha e vá à aba **Multiescala**, grupo **Trabalhos**.
2. Escolha o **Cálculo** e digite os seus **Parâmetros (JSON)**, p. ex. `{"method": "permeability", "tol": 1e-5}`
   para uma simulação Microtom. O volume ou o perfil aberto é a entrada.
3. Marque **Um trabalho por volume da amostra do mesmo tipo (lote)** para rodar sobre todos os volumes como este.
4. Para rodar aqui: ajuste **Trabalhos simultâneos aqui** e clique em **Executar aqui**.
5. Para rodar remotamente: digite o **Computador remoto** (`usuário@host` ou um alias da sua configuração SSH), a
   **Pasta lá / Python lá**, uma **Linha de preparação** opcional (p. ex. `module load python`), o **Escalonador /
   opções** (*nenhum*: um processo em segundo plano; *SLURM*: `sbatch` com opções como `--time=02:00:00 --mem=16G`) e
   clique em **Enviar ao computador remoto**.
6. A tabela acompanha os trabalhos (estado, progresso, tempo, erro); **Atualizar** relê os estados (os trabalhos
   remotos são copiados de volta quando terminam). Clique em **Trazer os resultados** para acrescentar ao projeto o
   que o trabalho terminado mais recente fez; **Cancelar o trabalho** o interrompe.

## Opções

| Campo | O que muda |
|---|---|
| Cálculo | Um de: simulação Microtom, mapas de porosidade (segmentação, saturação), permeabilidade de Darcy de um mapa, realizações MPS, extração da rede de poros, rede de duas escalas, REV de permeabilidade de uma rede, modelo de permeabilidade de um perfil de imagem |
| Parâmetros (JSON) | Os argumentos do cálculo, como num script |
| Trabalhos simultâneos aqui | Processos rodando juntos; os outros esperam |
| Escalonador / opções | Processo em segundo plano, ou SLURM com opções `#SBATCH` |

## Como funciona

Um trabalho é uma pasta ao lado do projeto (`<projeto>.jobs`): `job.json` (o cálculo, os parâmetros, as entradas),
`input.rockface` (um projeto pequeno só com os objetos necessários, com as suas amostras e poços), depois
`status.json` e `result.json` escritos pela execução. O cálculo é um de uma lista fixa de funções do RockFace — nunca
código enviado com o trabalho. Os trabalhos remotos são copiados com `scp`, iniciados com `ssh` (ou `sbatch`),
acompanhados lendo `status.json` e copiados de volta. Trazer os resultados copia todo objeto que o trabalho fez
(volumes, perfis, redes, superfícies) para o projeto, ligado às mesmas amostras e poços, com o trabalho registrado no
seu histórico.

## Por script

```python
seg = prj.volume("plug segmentation")
job = prj.prepare_job("microtom", volume_id=seg.id, method="permeability")
prj.run_jobs([job], workers=2)
print(prj.bring_back(job))
host = rf.jobs.Host("me@cluster", workdir="/scratch/me/rf", scheduler="slurm", slurm="--time=04:00:00")
runner = rf.jobs.RemoteRunner(host)
runner.submit(prj.prepare_job("pnm_extract", volume_id=seg.id))
```

## Limites e problemas comuns

* "Permission denied (publickey)": a chave SSH não foi aceita; abra um terminal e confira que `ssh usuário@host`
  funciona sem senha.
* Um trabalho remoto falha logo quando o RockFace não está lá: ajuste **Python lá** para o Python que o tem, ou a pasta
  do código no caminho do Python de um script (`Host(pythonpath=…)`).
* Os resultados são trazidos quando você pede, nunca escritos no projeto sem o seu conhecimento.

## Cobertura

GM10 (computação remota), GM9 (fluxos multiescala) e o fluxo remoto da rede de poros (GV12).

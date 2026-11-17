# A Mio olha a imagem

## Para que serve

A Mio pode olhar uma fotomicrografia da lâmina e propor os campos da descrição microscópica e do sistema poroso —
seleção, arredondamento, esfericidade, granulometria, arcabouço, contatos, porosidade visível e tipos de poro —, cada
um com **quantas das respostas dela concordam**. Quem olha é um modelo no seu próprio computador; nada vem marcado e
nada é escrito até você marcar o que você mesmo vê na imagem, aplicar ao formulário e salvar a descrição.

## Antes de começar

* Um **modelo de visão** neste computador (*Mio olha* → *Modelos de visão…*):
  * com uma **placa NVIDIA RTX de 12 GB** (RTX 3060 ou superior): **Qwen2.5-VL 7B** (Q5_K_M), 6,8 GB para baixar;
  * com uma placa de **24–32 GB** (RTX 5090): **Qwen2.5-VL 32B** (Q4_K_H), 19,3 GB;
  * com uma placa de 8 GB ou sem placa: o 7B menor (Q4_K_M) — no processador leva minutos por imagem.

  A janela marca o modelo que cabe na placa encontrada. Cada modelo vem em dois arquivos, o modelo de linguagem e o
  projetor de imagem; os dois são Apache-2.0. Quem os lê é o **llama-cpp-python** (compilado com CUDA para usar a
  placa; os instaladores o trazem compilado para o processador). Ou use um **servidor local** que já tenha o modelo — Ollama
  (`ollama pull qwen2.5vl:7b`), LM Studio ou llama-server —, informando o endereço (`http://localhost:11434/v1`) e o
  nome do modelo.
* Uma **imagem** da lâmina: uma foto ou lâmina inteira no Atlas, a imagem da contagem de pontos ou um arquivo. A
  imagem com nicóis cruzados do mesmo campo ajuda (cores de interferência, extinção).

## Passo a passo

1. Abra a descrição e clique em **Mio olha** (aba Início).
2. Escolha a **imagem**. As fotos do Atlas em luz polarizada plana vêm primeiro; o **par com nicóis cruzados** é
   achado pelo lugar na lâmina ou pelo nome (`… PP` / `… XP`) e aparece ao lado. De uma lâmina inteira, mostra-se o
   centro, 2 mm (um campo de visão). A **largura do campo** vem da escala da imagem; digite-a se for desconhecida —
   é com ela que o modelo julga a granulometria.
3. Escolha quantas **respostas** (3 por padrão) e clique em **Olhar**. O modelo é perguntado essas vezes; cada
   resposta é uma linha por campo, com as palavras do vocabulário do RockFace no seu idioma.
4. Leia a tabela: o campo, o **valor** que a maioria das respostas deu (os outros ditos ficam na lista dele, com
   quantas respostas os deram), a quantidade (a mediana, com a faixa dita), **Respostas que concordam** (2/3, 3/3…) e a
   linha do próprio modelo.
5. Olhe a imagem e **marque** só o que você mesmo vê. *Marcar onde todas concordam* marca as linhas 3/3 —
   desmarque as de que discordar.
6. **Aplique** e salve a descrição como de costume. *Respostas do modelo* mostra as respostas completas.

**Mio**: *"o que você vê na ILL-TS-001?"* (*"what do you see in …?"*, *"¿qué ves en la imagen de …?"*) olha a primeira
imagem em luz plana da amostra e lista as propostas com a concordância; não escreve nada.

## Como funciona

* **O modelo.** O Qwen2.5-VL (Bai et al. 2025) lê a imagem com até 1024 pixels no lado maior e responde a um
  formulário fixo: uma linha por campo, “não visível” quando a imagem não permite julgar. As palavras dele passam pelo
  mesmo leitor do ditado (1.0.0rc6), então as propostas usam os termos do RockFace; o campo nomeado no início da linha
  decide quais propostas daquela linha valem.
* **Quão seguro.** O que um modelo diz sobre a própria certeza é mal calibrado (Xiong et al. 2024). Em vez disso, o
  modelo é perguntado várias vezes, com temperatura 0,7, e as respostas são comparadas: a confiança de um valor é a
  parcela das respostas que o deram (autoconsistência, Wang et al. 2023). Quantidades concordam quando estão a até 2
  pontos percentuais ou 25 % da mediana (30 % para um tamanho em mm). Com uma resposta só, a concordância não diz nada.
* **Nada marcado.** As pessoas seguem conselhos automáticos mesmo quando estão errados (viés de automação, Goddard et
  al. 2012): toda proposta começa desmarcada e só é escrita quando você a aplica.
* **Só local.** As imagens nunca saem do computador; um servidor em outro computador é recusado, a não ser que
  `vision.allow_remote` seja ligado de propósito.
* **O que já foi medido.** Ainda nada em lâminas reais: esta versão foi testada com respostas roteirizadas, sem o
  modelo rodando. Os trabalhos publicados sobre descrever lâminas com modelos de visão e linguagem — ThinGPT (Luo et
  al. 2025) e um modelo de carbonatos treinado com 57 000 imagens (Atolagbe & Koeshidayatullah 2026) — usaram modelos
  treinados com lâminas rotuladas; o Qwen2.5-VL geral usado aqui não foi, então espere mais segurança na textura do
  que na mineralogia e confira cada proposta.
* **Fora desta versão.** Buscar na biblioteca as lâminas mais parecidas e propor a partir das descrições delas
  aguarda a decisão do proprietário sobre duas patentes (US 12,688,615 B2; US 2022/0207079 A1).

## Por script

```python
d = prj["ILL-TS-001"]
r = d.look(samples=3)               # a primeira imagem PP da lâmina no Atlas, e o par XP
[(f["target"], f["code"], f["value"], f["confidence"]) for f in r["findings"]]
r["answers"]                        # o que o modelo escreveu, resposta por resposta
d.look(image="campo.png", xpl="campo_xp.png", width_mm=1.3, apply=True, at_least=1.0)  # escreve as 3/3
rf.look("campo.png", lang="pt")    # sem projeto
rf.vision_models(); rf.vision_status()
```

## Limites e problemas comuns

* Um modelo geral, não um petrógrafo: pode tomar cimento por grão ou grãos arrancados por poros, ou chamar toda rocha
  de moderadamente selecionada. A concordância entre as respostas mede a coerência dele, não o acerto.
* A composição mineral não é proposta — isso é a contagem de pontos (com o assistente de IA da 1.0.0rc7).
* Números vencem palavras: uma descrição com seleção medida (φ) ou granulometria medida mantém a classe que segue o
  número quando a proposta é aplicada, e o salvamento avisa.
* Imagem sem escala: digite a largura do campo, ou a granulometria será adivinhada do nada.
* No processador o modelo 7B leva minutos para três respostas; o 32B precisa de uma placa de 24–32 GB.
* “Este llama-cpp-python não lê imagens do Qwen2.5-VL”: atualize o llama-cpp-python ou use um servidor local.

## Cobertura

O8 (pedido do proprietário de 2026-11-17: as inovações, a quinta).

Referências: Bai et al. (2025), Qwen2.5-VL technical report, arXiv:2502.13923; Wang et al. (2023), Self-consistency
improves chain of thought reasoning in language models, ICLR 2023, arXiv:2203.11171; Xiong et al. (2024), Can LLMs
express their uncertainty?, ICLR 2024, arXiv:2306.13063; Goddard, Roudsari & Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089; Luo et al. (2025), ThinGPT, Petroleum Science,
https://doi.org/10.1016/j.petsci.2025.09.009; Atolagbe & Koeshidayatullah (2026), Vision-language models for automated
carbonate petrography and depositional environment interpretation, Artificial Intelligence in Geosciences 7(3)
100230, https://doi.org/10.1016/j.aiig.2026.100230.

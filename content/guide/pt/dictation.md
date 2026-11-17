# Ditado no microscópio

## Para que serve

No microscópio os olhos estão nas oculares e as mãos na platina. Com o ditado o petrógrafo fala em vez de digitar:
os **campos da descrição** ("seleção moderada, arredondamento subarredondado, porosidade intergranular primária 12
por cento, contatos côncavo-convexos") e a **contagem de pontos** ("quartzo monocristalino", "três", "desfazer"). A
fala é reconhecida **neste computador** — o áudio não é guardado nem enviado — e nada é escrito antes de o petrógrafo
ver o que foi entendido.

## Antes de começar

* Instale uma vez as bibliotecas de voz: `pip install rockface[voice]` (whisper.cpp, Vosk e a biblioteca do
  microfone; todas MIT ou Apache-2.0).
* Abra **Ditar → Modelos de voz…** e baixe:
  * **Whisper base** (142 MB) para ditar descrições — ou o *Whisper small* (466 MB) com 8 GB de memória, ou o
    *Whisper large-v3 turbo* (547 MB) com uma placa NVIDIA RTX e uma compilação CUDA do pywhispercpp;
  * o modelo **Vosk small** do seu idioma (31–40 MB) para contar por voz.
* Escolha o microfone na mesma janela. Um microfone de headset deixa o ruído da sala de fora.

## Passo a passo

**Ditando a descrição**

1. Abra uma descrição e clique em **Ditar** (aba Início).
2. Clique em **Ouvir** e fale. Faça uma pausa depois de cada frase: cada pausa envia o que você disse, que aparece na
   caixa de texto. Você também pode digitar ou colar as palavras e clicar em **Interpretar**.
3. Leia a tabela: cada proposta mostra o campo, o valor, o % ou mm, e **as palavras de onde veio**.
   * Uma palavra que serve para vários tipos (*intergranular*: primária ou secundária?) vem **desmarcada**, com uma
     lista para escolher.
   * Uma frase negada (*sem fraturas*, *no cement*, *sin porosidad móldica*) aparece como **dito ausente** e nunca
     acrescenta nada.
   * Dizer um campo duas vezes fica com o último: "bem selecionado… não, moderadamente selecionado" dá
     *moderadamente selecionado*.
4. Marque o que está certo e clique em **Aplicar as marcadas**. Os valores vão para as abas Microscópica e Sistema
   poroso; **salve a descrição** para mantê-los (as verificações de sempre rodam nesse momento).
5. O que não foi entendido pode ir para as notas da descrição microscópica (marque a caixa embaixo da tabela).

**Contando por voz**

1. Na aba **Contagem**, faça a grade como sempre e clique em **Contar por voz**.
2. Em cada ponto diga o nome do constituinte (*quartzo monocristalino*), parte dele quando só uma linha o tem
   (*feldspato*), ou o número do seu atalho de teclado (*três*, *número três*).
3. Comandos: **desfazer**, **voltar**, **pular**, **parar** (*undo, back, skip, stop*; *deshacer, volver, saltar,
   detener*).
4. A linha embaixo do botão diz o que foi ouvido e o que foi feito. Uma palavra não entendida, ou que serve para duas
   linhas (*quartzo* com quartzo mono e policristalino), não conta nada: o programa apita e você repete.
5. **A platina nunca é movida por voz**: mova-a com o teclado, o controlador ou à mão.

**Perguntando à Mio**

* O botão do microfone ao lado da caixa de pergunta da Mio ouve uma pergunta e a coloca na caixa; leia e envie.
* *"Anote: seleção moderada, porosidade 12 por cento"* (*note:*, *dicta:*) faz a Mio ler os campos nas palavras — ela
  só os mostra; quem escreve é a janela Ditar.

## Campos entendidos

| Campo | Exemplos |
|---|---|
| Seleção | *bem selecionado*, *seleção moderada*, *moderately sorted*, *mal seleccionado* |
| Arredondamento e seus modificadores | *subarredondado*, *angular*, *subrounded*, *grãos com golfos de corrosão* |
| Esfericidade | *esfericidade alta*, *low sphericity*, *alongados* |
| Moda granulométrica principal | *areia média*, *fine sand*, *moda principal 0,25 mm*, *moda principal zero vírgula dois cinco milímetros* |
| Trama | *suportada por grãos*, *suportado pela matriz*, *imbricada* |
| Contatos intergranulares (com %) | *contatos côncavo-convexos 40 por cento*, *suturados*, *contatos pontuais* |
| Porosidade visual total | *porosidade total 18 por cento*, *porosity 12 %*, *sem porosidade visível* (0 %) |
| Tipos de poro (com %) | *intergranular primária 12*, *porosidade móldica 3 por cento*, *microporosidade*, *vugues* |

Os números podem ser algarismos ou palavras nos três idiomas (*vinte e cinco*, *twenty five*, *veinticinco*;
*zero vírgula dois cinco*).

## Como funciona

* **Dois reconhecedores, ambos locais.** O Whisper (whisper.cpp, MIT) escreve o ditado livre e é orientado para o
  vocabulário petrográfico por um texto inicial curto com os termos da descrição e os constituintes da composição
  (viés contextual, Lall & Liu 2024). O Vosk (Apache-2.0) reconhece na hora o vocabulário fechado da contagem — as
  linhas, os números e os comandos —, então uma palavra fora dele é recusada em vez de adivinhada.
* **Só a fala é ouvida.** O som é cortado em falas pela intensidade (uma pausa de 0,6 s encerra uma), de modo que o
  reconhecedor nunca ouve silêncio: o Whisper inventa frases no silêncio (*Careless Whisper*, Koenecke et al. 2024).
  Frases inventadas conhecidas ("obrigado por assistir", "thanks for watching") e frases repetidas em laço são
  retiradas.
* **Cada proposta mostra suas palavras.** Os erros do reconhecimento de voz parecem plausíveis, e tirar ou pôr um
  "não" é o erro clássico (Basma et al. 2011): daí as palavras ouvidas, os tipos ambíguos desmarcados e as negações
  que nunca viram presença.
* **O vocabulário é o da base de conhecimento**: os rótulos dos termos e das escalas em inglês, espanhol e português,
  com os gêneros e plurais do português e do espanhol (*selecionado/selecionada*).

## Por script

```python
d = prj["ILL-TS-001"]
r = d.dictate("subanguloso, contatos suturados", "pt")               # só as propostas
[(p["target"], p["code"], p["value"]) for p in r["proposals"]]
d.dictate("subanguloso, contatos suturados", "pt", apply=True)       # escritas e salvas (as verificações de sempre)
prj["ILL-TS-002"].voice_count("três", "pt")                          # {"kind": "count", "slot": 3, ...}
rf.dictation("bem selecionado, porosidade 12 %", "pt")               # sem projeto
rf.speech_models(); rf.speech_status()
rf.transcribe("nota.wav", "pt")                                      # um arquivo WAV de 16 bits, reconhecido localmente
```

## Limites e problemas comuns

* **Nenhum microfone encontrado**: instale `rockface[voice]` (o sounddevice traz o PortAudio) e confira o dispositivo
  de entrada do sistema; escolha-o em *Modelos de voz…*.
* O Whisper base num processador antigo leva um ou dois segundos por frase; frases curtas com pausas funcionam
  melhor. Com uma placa RTX, o *large-v3 turbo* é mais rápido e mais preciso.
* O ditado livre entende os campos acima; a composição é contada por voz, não ditada em porcentagens.
* O modelo Vosk pequeno de português é fraco na fala livre (cerca de 33 % de palavras erradas no Common Voice), mas
  confiável no vocabulário fechado da contagem, que é para o que ele é usado.
* Alguns modelos Vosk são AGPL ou não comerciais; só os Apache-2.0 são oferecidos.

## Cobertura

O8 (pedido do dono de 2026-11-17: as inovações, a terceira).

Referências: Radford et al. (2023), Whisper, PMLR 202; Koenecke et al. (2024), https://doi.org/10.1145/3630106.3658996;
Basma et al. (2011), https://doi.org/10.2214/AJR.11.6691; Lall & Liu (2024), arXiv:2410.18363; Povey et al. (2011),
Kaldi; Al-Dhubaib et al. (2008), US 7.319.961 (captura por voz de dados petrográficos e contagens; expirada).

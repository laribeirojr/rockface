# Contagem de pontos assistida por IA

## Para que serve

A maior parte dos pontos de uma contagem é fácil: o mesmo quartzo, a mesma resina dos poros, de novo e de novo. O
assistente de IA aprende com os pontos que você conta e propõe a linha do próximo ponto; você confirma com **Enter**
ou conta outra linha. Cada confirmação ou correção ensina o modelo na hora, então depois de algumas dezenas de pontos
a maioria das propostas está certa e a contagem anda mais rápido — e cada ponto continua sendo decidido por você.

## Antes de começar

* Uma **grade** sobre a **imagem** da contagem (Contagem de pontos → Imagem e calibração: *Imagem da lâmina…*, depois *Criar grade*).
* Se quiser, a **imagem com nicóis cruzados** do mesmo campo, do mesmo tamanho e enquadramento (*Imagem com nicóis
  cruzados…*): o modelo aprende também as cores de interferência.
* As bibliotecas de IA do programa (`rockface[lab]`, nas duas edições dos instaladores).

## Passo a passo

1. Conte os primeiros pontos como sempre — pelo menos **15 pontos de duas linhas ou mais**.
2. Marque **Propor o constituinte (IA)**. Embaixo dos botões da contagem aparece a proposta para o ponto atual:
   *IA: Quartzo monocristalino — 92 %*, e as linhas seguintes com suas probabilidades.
3. Aperte **Enter** (ou *Aceitar*) quando a proposta estiver certa; conte outra linha (teclado, lista, voz) quando não
   estiver. O modelo aprende de novo a cada ponto.
4. **Verificação às cegas**: mais ou menos um ponto em cada dez mostra *Verificação às cegas: conte este ponto sem
   proposta*. São sempre os mesmos pontos; neles você conta sem ver a proposta, e a concordância medida ali é honesta.
5. Marque **Pontos mais incertos primeiro** para o modelo escolher o próximo ponto: aquele em que ele está menos
   seguro. É ali que ele aprende mais rápido. **Conte depois todos os pontos** da grade — uma contagem parada no meio
   assim não é uma amostra aleatória da lâmina, e a aba avisa.
6. Leia a linha de baixo: os pontos do modelo e seu acerto fora da amostra, a sua **concordância** com as propostas e
   a concordância nos pontos **às cegas**, com o intervalo de 95 %.

**Mio**: *"como a IA se saiu na contagem da ILL-TS-002?"* dá a concordância, a das cegas e as correções mais
frequentes.

## Como funciona

* **O que o modelo vê.** Em volta de cada ponto, três janelas da imagem: o retículo (3 × 3 pixels), o grão embaixo
  dele (30 µm) e a vizinhança (90 µm). Em cada uma: média e dispersão do vermelho, verde e azul, saturação, brilho,
  matiz, os percentis 10, 50 e 90 do brilho, o gradiente médio (textura, relevo) e o quanto é azul (resina dos poros)
  — 45 números, 90 com a imagem de nicóis cruzados.
* **O modelo** é uma floresta aleatória (Breiman 2001), a mesma do RockFace Lab, treinada com os pontos contados; a
  fração das árvores que vota numa linha é a probabilidade da proposta. Ele é treinado de novo sempre que os pontos
  contados mudam — uma fração de segundo.
* **Aprendizado ativo.** A *margem* entre as duas linhas mais prováveis mede a dúvida; *mais incertos primeiro*
  visita o ponto de menor margem (amostragem por incerteza, Settles 2009).
* **Medido numa lâmina ILLUSTRATIVE com textura** (a rocha sintética do guia, PP e XP, 300 pontos): com 15 pontos
  contados as propostas acertavam 54 % dos pontos ainda por contar; com mais 60, 81 % visitando a grade em ordem e
  **91 % visitando primeiro os mais incertos**. Na lâmina de cores lisas do exemplo (ILL-TS-002), treinada com 100
  pontos, 94,5 % dos outros 200 estavam certos.
* **Por que pontos às cegas.** As pessoas seguem conselhos automáticos mesmo quando estão errados (*viés de
  automação*, Goddard et al. 2012); a concordância medida em pontos cuja proposta você viu fica inflada por isso. Os
  pontos às cegas, com a proposta escondida, medem o modelo como ele é. Cada ponto contado guarda o que foi proposto,
  a probabilidade e se era às cegas.

## Por script

```python
d = prj["ILL-TS-002"]
r = d.assist(top=10)              # os dez pontos ainda não contados mais incertos
r["ready"], r["trained_on"], r["oob"]
[(q["index"], q["uid"], round(q["p"], 2)) for q in r["proposals"]]
d.set_crossed_image("ILL-TS-002-xpl.png")    # o mesmo campo com nicóis cruzados
d.ai_agreement()                  # {"proposed", "agreed", "rate", "blind", "blind_rate", "interval", ...}
```

Os scripts só leem as propostas: quem conta é o petrógrafo.

## Limites e problemas comuns

* O modelo conhece só esta lâmina e as linhas contadas nela: ele aprende do zero em cada contagem, então os primeiros
  pontos são sempre contados à mão. Um constituinte raro, visto uma ou duas vezes, raramente é proposto — conte-o
  você.
* As propostas dependem da imagem: fora de foco, luz desigual ou um aumento diferente do dos pontos contados as pioram.
  Pontos fora da imagem não têm proposta.
* A imagem precisa estar calibrada (µm por pixel) para as janelas terem o tamanho real.
* Visitar primeiro os pontos incertos muda a ordem, não a grade: use só quando for contar todos os pontos.
* O modelo não vem pronto nem é pré-treinado em outras rochas; o banco LITHOS (Chacón et al. 2025, 25 classes de
  minerais) é não comercial e foi usado só para ler sobre o estado da arte.

## Cobertura

O8 (pedido do dono de 2026-11-17: as inovações, a quarta).

Referências: Breiman (2001), https://doi.org/10.1023/A:1010933404324; Settles (2009), Active learning literature
survey, Univ. Wisconsin–Madison TR 1648; Tang, Milliken & Spikes (2020), https://doi.org/10.1016/j.marpetgeo.2020.104518;
Chacón et al. (2025), Towards automated petrography, arXiv:2511.00328; Goddard, Roudsari & Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089.

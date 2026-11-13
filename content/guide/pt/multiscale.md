# Multiescala: geração de imagens (MPS), comparação das realizações e a rede de poros de duas escalas

## Para que serve

Um plugue escaneado em alta resolução cobre alguns milímetros; um perfil de imagem ou um escaneamento de testemunho
cobre metros numa resolução mais grossa. A aba **Multiescala** do RockFace MC junta as escalas: **gera imagens 3D**
da escala fina com as estatísticas de um volume de treinamento, condicionadas pelo que se conhece na escala grossa
(dados duros, ou um perfil de imagem envolvido na parede do poço), **compara** as realizações com a imagem de
treinamento e extrai uma **rede de poros de duas escalas** de um mapa de porosidade, em que os voxels microporosos
se tornam poros não resolvidos.

## Antes de começar

* Para a MPS: um volume de treinamento (uma segmentação, para uma simulação categórica, ou um volume de cinza ou de
  porosidade, para uma contínua). Opcionalmente um volume de dados duros na malha da simulação (0 ou vazio = sem
  dado) ou um perfil de imagem do poço.
* Para a rede de duas escalas: um mapa de porosidade (aba Microporosidade).

## Passo a passo

### Gerar imagens (MPS)

1. Vá à aba **Multiescala**; em **Geração de imagens (MPS)** escolha o **Volume de treinamento**.
2. Opcionalmente escolha **Dados duros (volume)** ou **Dados duros (perfil de imagem num cilindro)**: as colunas do
   perfil são postas na parede de um cilindro vertical da malha, uma linha por fatia.
3. Digite a **Malha (z y x)** da simulação (vazio: a malha do volume de treinamento), o número de **Realizações** e
   a **semente**.
4. Ajuste os **Vizinhos / raio de busca / limiar de distância** da amostragem direta e clique em **Simular**. Cada
   realização é um novo volume da amostra (categoria *simulation*).

### Comparar as realizações

Clique em **Comparar as realizações**: o gráfico mostra a porosidade de cada fatia de cada realização contra a imagem
de treinamento, e a tabela o raio médio de poro de cada uma (distribuição de tamanhos de poro por espessura local).

### Rede de poros de duas escalas

1. Em **Rede de poros de duas escalas** escolha o **Mapa de porosidade**.
2. Escolha o **Raio dos poros não resolvidos**: *fixo* (digite-o), *J de Leverett (a partir de k)* ou *a partir de
   uma curva MICP*, e a **tortuosidade** e o tamanho do **bloco** (voxels de microporosidade reunidos num poro não
   resolvido).
3. Clique em **Extrair e calcular a permeabilidade**. A rede fica guardada no projeto (aba Rede de poros, onde todas
   as simulações da 0.24 rodam sobre ela) com a sua permeabilidade segundo x, y e z.

## Opções

| Campo | O que muda |
|---|---|
| Vizinhos | Número de nós informados mais próximos do nó simulado que formam o seu padrão (24 por padrão) |
| Raio de busca | Até onde se procuram os vizinhos (voxels) |
| Limiar de distância | A imagem de treinamento é percorrida até um padrão diferir menos do que esta fração (0,05: no máximo um vizinho em vinte de outra classe) |
| Raio dos poros não resolvidos | *fixo*: um raio; *Leverett*: r = √(8k/φ) a partir de uma permeabilidade k da fase microporosa; *MICP*: raios sorteados de uma curva de mercúrio, os maiores para os blocos mais porosos |
| Tortuosidade / bloco | τ do modelo de feixe de capilares dos tampões microporosos; a aresta dos cubos de voxels microporosos que formam um poro não resolvido |

## Como funciona

* **Amostragem direta** (Mariethoz, Renard & Straubhaar 2010): os nós são visitados numa ordem aleatória; para cada um,
  o padrão dos seus vizinhos informados é comparado com padrões em lugares aleatórios da imagem de treinamento, e o
  valor do primeiro lugar próximo o bastante (ou do mais próximo percorrido) é colado. Os dados duros são informados
  desde o início e mantidos.
* **A rede de duas escalas** (segundo Bultreys et al. 2015): os poros resolvidos (φ = 1) são extraídos por SNOW como na
  0.24; os voxels microporosos são reunidos em cubos que se tornam poros não resolvidos, de volume Σφ e raio dado pelo
  modelo de subescala. Um conduto que toca um poro não resolvido é um tampão poroso de permeabilidade k = φ r² / (8 τ)
  (um feixe de capilares de raio r e tortuosidade τ), condutância k A / L. Um mapa binário dá exatamente a rede da
  0.24; um bloco microporoso uniforme dá exatamente o k do tampão.

## Por script

```python
seg = prj.volume("plug segmentation")
reals = seg.mps(realizations=5, shape=(64, 128, 128), log=prj.log("AMP image log"), seed=3)
net = prj.volume("plug porosity map").multiscale_network({"kind": "fixed", "radius_um": 0.5}, tortuosity=2.0)
print(net.kabs())
```

## Limites e problemas comuns

* A amostragem direta fica lenta com imagens de treinamento grandes e limiares estritos: comece com uma malha pequena,
  limiar 0,1 e fração percorrida 0,05 (``fraction`` num script), depois refine. Execuções longas podem ir como
  trabalhos.
* A rede generativa (RockSinGAN) do programa de referência é um modelo de IA; vem com a etapa de IA (0.26).
* Os modelos de subescala são simples: os tampões microporosos são feixes de capilares; use uma curva MICP da fase
  microporosa quando o laboratório tiver uma.

## Cobertura

GV13 (multiescala), GM5 (geração de imagens — MPS; a rede generativa na 0.26), GM6 (pós-processamento), GM7 (rede de
poros entre escalas), GM3 (pré-processamento de perfis de imagem: o perfil num cilindro), GM4 e GM8 (pré-processamento
e segmentação das escalas, com as ferramentas da 0.20–0.23).

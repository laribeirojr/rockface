# Microporosidade: mapas de porosidade, permeabilidade de Darcy e as simulações Microtom

## Para que serve

Um volume de micro-CT resolve os poros grandes, mas não os poros menores que o seu voxel: um voxel de cimento ou de
argila microporosa é cinza, entre o poro e o grão. A aba **Microporosidade** do RockFace MC transforma o volume num
**mapa de porosidade** (cada voxel 0 = sólido … 1 = poro resolvido, a microporosidade entre os dois), calcula a
**permeabilidade de Darcy** desse mapa e executa as simulações **Microtom** sobre uma segmentação: distribuições de
tamanho de poro, intrusão de mercúrio e drenagem capilar, embebição e a permeabilidade absoluta por lattice
Boltzmann.

## Antes de começar

* Um volume de micro-CT em cinza e a sua segmentação na mesma malha (aba Segmentação), com um segmento para os poros
  resolvidos, um para a fase microporosa e um para os grãos.
* Para o método por saturação: um escaneamento seco e um do mesmo plugue saturado com um fluido de contraste,
  registrados na mesma malha (aba Registro), e a segmentação.
* As simulações Microtom trabalham numa segmentação com o papel "pore" nos seus segmentos de poro.

## Passo a passo

### Criar um mapa de porosidade

1. Abra o volume em cinza e vá à aba **Microporosidade**.
2. Em **Mapa de porosidade**, escolha **A partir de**: *uma segmentação* ou *um escaneamento seco e um saturado*.
3. Escolha o **Volume de cinza** (ou o **Escaneamento seco** e o **Escaneamento saturado**) e a **Segmentação**.
4. Confira o **Papel de cada segmento**, escrito como `Segmento=papel; …`: `macro` (poro resolvido, porosidade 1),
   `micro` (microporoso: porosidade a partir da atenuação), `solid` (porosidade 0) e `high` (minerais densos,
   porosidade 0). A proposta vem dos nomes e papéis dos segmentos; digite por cima para mudar.
5. Mantenha **Atenuações de poro e sólido a partir das medianas dos seus segmentos**, ou desmarque e digite a
   **Atenuação de poro / sólido**.
6. Clique em **Criar o mapa de porosidade**. O mapa é um novo volume (categoria *porosity*); a tabela dá a
   porosidade total, a parte resolvida e a microporosidade.

### Permeabilidade de Darcy do mapa

1. Abra o mapa de porosidade.
2. Em **Permeabilidade de Darcy do mapa**, escolha a **Permeabilidade de um voxel**: *lei de potência k = a·φ^b*
   (digite a em mD e b) ou *Kozeny–Carman* (digite o **Diâmetro de grão**). Os poros resolvidos recebem a
   permeabilidade de um tubo da largura do voxel.
3. Clique em **Calcular a permeabilidade do mapa atual**: K segundo x, y e z.

### Simulações Microtom

1. Abra a segmentação.
2. Escolha a **Simulação** e as suas opções e clique em **Simular na segmentação atual**. Um mapa feito pela
   simulação (raio de poro, raio de entrada) é guardado como novo volume; o gráfico e a tabela mostram a curva.

## Opções

| Campo | O que muda |
|---|---|
| Simulação | *Distribuição de tamanhos de poro (espessura local)*: o raio da maior esfera que contém cada voxel de poro, como curva acumulada. *Distribuição de tamanhos de poro (esferas sem sobreposição)*: esferas colocadas da maior para a menor sem se sobreporem (contagem hierárquica). *Intrusão de mercúrio (MICP)*: σ 0,485 N/m, θ 140°, a partir de uma face. *Drenagem capilar*: o mesmo com o seu σ e θ. *Embebição* e *Embebição com aprisionamento (Sor)*: o fluido molhante volta pelos poros pequenos; com aprisionamento, o óleo isolado da saída fica (Sor). *Permeabilidade absoluta (lattice Boltzmann)* e o seu *REV* em cubos de aresta crescente |
| Direção de invasão | A face por onde o fluido entra (x, y ou z) |
| Passos de raio | Número de raios das curvas |
| Tensão interfacial / ângulo de contato | σ e θ da drenagem e da embebição |
| Tempo de relaxação / tolerância | τ do modelo de lattice Boltzmann (1,5 por padrão) e a variação relativa da velocidade média em que o escoamento é estacionário |
| No máximo (voxels) | A simulação usa o nível mais fino da pirâmide com no máximo este número de voxels |

## Como funciona

* **Porosidade pela atenuação**: na fase microporosa φ = (I_sólido − I) / (I_sólido − I_poro), limitada a 0…1; os
  poros resolvidos valem 1, o sólido 0. Por um escaneamento seco e um saturado, φ = (Δ − Δ_sólido) / (Δ_poro −
  Δ_sólido) com Δ = I_saturado − I_seco, a diferença dos dois escaneamentos em relação às de um poro resolvido e do
  sólido. Ambos são modelos lineares de mistura da atenuação.
* **Permeabilidade de Darcy do mapa**: cada voxel recebe k(φ) e a equação da pressão ∇·(k ∇p) = 0 é resolvida por
  volumes finitos (médias harmônicas entre voxels), pressão fixa em duas faces opostas; K = Q L / (A Δp). Exata em
  mapas em camadas (médias aritmética e harmônica).
* **Tamanhos de poro**: espessura local (Hildebrand & Rüegsegger 1997) a partir do mapa de distâncias euclidianas.
* **Drenagem e MICP**: invasão morfológica (Hilpert & Miller 2001): no raio r o fluido não molhante preenche as
  esferas de raio r cujos centros se ligam à face de entrada; P = 2σ|cos θ| / r (Washburn 1921).
* **Lattice Boltzmann**: D3Q19, colisão de dois tempos de relaxação (Ginzburg, Verhaeghe & d'Humières 2008) com o parâmetro mágico 1/8, que
  põe a parede de bounce-back a meio caminho entre os nós; uma força de corpo move o escoamento e K = ν ⟨u⟩ / g. A
  amostra é unida à sua imagem espelhada ao longo do escoamento, de modo que as fronteiras são periódicas. Conferido
  no escoamento de Poiseuille plano (exato) e em arranjos de esferas contra Sangani & Acrivos (1982).

## Por script

```python
grey, seg = prj.volume("plug grey"), prj.volume("plug segmentation")
phi, info = grey.porosity_map(seg, {1: "macro", 2: "micro", 3: "solid"})
k = phi.darcy(model="power", a_md=50, b=3)
psd = seg.microtom("psd")
lbm = seg.lbm_permeability(axes=("x", "y", "z"))
```

## Limites e problemas comuns

* A atenuação da fase microporosa deve estar entre as do poro e do sólido; um mineral denso no segmento microporoso
  é lido como sólido. Dê a esses minerais um segmento próprio com o papel `high`.
* O lattice Boltzmann cresce com o número de voxels de poro: um cubo de 128³ de um arenito leva cerca de uma hora em
  dois núcleos de processador. Envie-o como trabalho (aba Multiescala → Trabalhos) ou reduza **No máximo (voxels)**.
* Abaixo de cerca de 4 voxels de largura, uma garganta não é resolvida pelo lattice Boltzmann; o tamanho do voxel
  define o menor poro que escoa.

## Cobertura

GV9 (microporosidade), GV10 (Microtom), GV11 (modelagem de escoamento e permeabilidade).

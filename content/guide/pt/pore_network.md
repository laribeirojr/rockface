# Rede de poros: extração, permeabilidade, intrusão de mercúrio, permeabilidade relativa, produção

## Para que serve

O espaço poroso de um volume de micro-CT transformado numa rede de poros (os corpos) ligados por gargantas (as
constrições), sobre a qual o escoamento é calculado: a permeabilidade absoluta em x, y e z, a curva de intrusão de
mercúrio (MICP) para comparar com o laboratório, as curvas de permeabilidade relativa de óleo e água (drenagem e
depois embebição), a recuperação de óleo de uma injeção de água, e como tudo isso muda com a molhabilidade.

## Antes de começar

* Um volume segmentado da amostra no RockFace MC (aba Segmentação), com os segmentos de poro marcados com o papel
  "poro" — ou um volume de objetos (aba Análises → Objetos do espaço poroso), cujos objetos viram os poros.
* Ou uma rede no formato Statoil (os quatro arquivos `*_node1.dat`, `*_node2.dat`, `*_link1.dat`, `*_link2.dat` do
  pnextract e do pnflow, como as redes do Imperial College).
* Um volume grande é extraído no nível mais fino da sua pirâmide abaixo de 64 milhões de voxels; recorte-o antes
  (Volume → Recortar) para trabalhar na resolução plena.

## Passo a passo

### Extrair a rede

1. Abra o volume segmentado e vá à aba **Rede de poros**.
2. Em **Extração (SNOW)**, mantenha **Suavização do mapa de distâncias** 0,40 e **Raio da busca de picos** 4 voxels
   (os valores do algoritmo SNOW), dê um **Nome** se quiser e clique em **Extrair a rede deste volume**.
3. A rede aparece em **Rede** com os seus números (poros, gargantas, número de coordenação médio, poros isolados, raios
   médios, porosidade da rede), desenhada em 3D: arraste para girar, roda para aproximar; **Cor dos poros** pelo raio
   ou pelo número de coordenação. As regiões dos poros ficam guardadas como um volume de objetos.
4. **Importar Statoil…** lê uma rede feita em outro programa; **Exportar Statoil…** grava a atual (fluxo ao longo do
   eixo escolhido em **Fluxo ao longo de**); **Apagar a rede** a retira do projeto.

### Executar uma simulação

Escolha a **Simulação**, os seus parâmetros, e clique em **Executar**. O gráfico e a tabela mostram o resultado; todo
resultado fica guardado com a rede.

* **Permeabilidade absoluta (uma fase)** — K em x, y, z (ou num eixo) em mD e m².
* **Intrusão de mercúrio (MICP)** — a saturação de mercúrio contra a pressão (log), com o raio de garganta de cada
  passo na tabela.
* **Permeabilidade relativa (duas fases)** — drenagem (óleo entrando na rocha cheia de água) e depois embebição (a
  água voltando): krw e kro contra Sw, Pc de cada passo; Swi, Sor e os pontos extremos na barra de estado.
* **Teste de sensibilidade** — a rodada de duas fases repetida para cada valor de um parâmetro (**Variar**, valores
  separados por `;`): a nuvem de curvas e a sua média, a tabela dos resultados de cada rodada e as correlações do
  parâmetro com cada resultado.
* **Kabs VER** — o volume cortado em cubos centrados de aresta crescente, cada um extraído de novo, e a permeabilidade
  de cada tamanho: onde ela para de mudar, o volume é representativo.

### Depois de uma rodada de duas fases

* **Animar os ciclos** — os poros coloridos pelo fluido em cada passo (óleo vermelho, água azul); o controle deslizante
  escolhe o passo.
* **Previsão de produção** — a injeção de água da curva de embebição (Buckley–Leverett): óleo recuperado contra os
  volumes porosos de água injetados; depois de um teste de sensibilidade, todas as curvas e as previsões pessimista,
  neutra e otimista (P10, P50, P90).
* **Curva de referência (CSV)…** — uma curva krel medida (colunas `Sw`, `krw`, `kro`) desenhada junto da simulada.
* **Relatório (HTML)…** — uma página com a rede, a permeabilidade, MICP, krel, produção e VER.

## Opções

* **Mercúrio**: tensão superficial 0,485 N/m e ângulo de contato 140° por padrão.
* **Tensão interfacial óleo–água** (0,03 N/m), **viscosidades** da água e do óleo.
* **Ângulo de contato de recuo** (drenagem) — o centro e a **amplitude** (os ângulos dos elementos espalhados de modo
  uniforme na amplitude); **Ângulo de avanço − recuo**: o ângulo de avanço da embebição. Abaixo de 90° a rocha é
  molhável à água, acima de 90° ao óleo.
* **Passo de Sw** — a saturação entre dois pontos calculados; **Swi mínima** — onde a drenagem para.
* **Plano inferior / superior da caixa** — a saturação e o fluxo são calculados entre esses planos (0,1 e 0,9 do
  comprimento por padrão, como a caixa de cálculo do pnflow): os poros além deles fixam as pressões.

## Como funciona

* **Extração**: o mapa de distâncias do espaço poroso, suavizado, os seus máximos como marcadores (um marcador mais
  perto de outro mais alto que do sólido é descartado), o watershed: cada região um poro, cada contato de duas regiões
  uma garganta (Gostick 2017). Raio do poro: a maior distância na região; raio da garganta: a maior no contato; fator
  de forma da garganta G = r² / (4 A) pela sua área A.
* **Escoamento**: cada conduto (meio poro, garganta, meio poro) três dutos em série, g = k G A² / μ (k = 3/5 triângulo,
  0,5623 quadrado, 1/2 círculo; Patzek & Silin 2001); as pressões dos poros resolvidas; K = Q μ L / (A ΔP).
* **MICP**: o mercúrio entra por todas as faces, um elemento a P = −2 σ cos θ / r (Washburn 1921) se um vizinho já está
  cheio.
* **Duas fases**: drenagem por percolação invasiva a partir da face de entrada, água retida nos cantos; embebição por
  snap-off nas gargantas, σ (cos θ − sen θ tg β) / r, e preenchimento tipo pistão, 2 σ cos θ / r, o óleo aprisionado
  quando perde o caminho até a saída; kr pelas condutâncias de cada fase (Valvatne & Blunt 2004, simplificado).
* **Produção**: o fluxo fracionário, a tangente de Welge e a recuperação (Buckley & Leverett 1942; Welge 1952).

## Por script

```python
seg = prj.volume("ILLUSTRATIVE sphere pack")
net = seg.extract_network(name="ILLUSTRATIVE network")
print(net.stats()["coordination_mean"])
k = net.kabs()                         # {"x": {"K_mD": …}, …, "mean_mD"}
m = net.micp()
kr = net.two_phase(theta_r=30, separation=20, swi_min=0.2)
pr = net.production(kr, mu_w=1e-3, mu_o=5e-3)
runs = net.sensitivity({"theta_r": [20, 40, 60]})
net.export_statoil("pack")             # pack_node1.dat …
net.report("rede.html")
berea = prj.import_statoil("Berea_node1.dat")
```

## Limites e problemas comuns

* **"Nada flui de face a face"** — os poros não ligam as duas faces nesse eixo: tente outro eixo, ou a segmentação
  perde os poros pequenos.
* O modelo de duas fases é simplificado: sem preenchimento cooperativo dos poros, sem camadas de óleo, sem inchamento
  de filmes; numa rocha muito molhável à água o snap-off domina e kro cai cedo. Compare com curvas medidas (Curva de
  referência) antes de usar os valores.
* Os raios extraídos vêm do mapa de distâncias nos centros dos voxels: gargantas de um voxel de largura não são
  resolvidas.
* Extrair 64 milhões de voxels (400³) leva cerca de 1,5 minuto e 3,5 GB de memória.
* A microporosidade (poros não resolvidos) e as redes multiescala chegam na etapa 0.25.

## Cobertura

GV12 (Pore Network: Extraction, Simulation — uma fase, duas fases, injeção de mercúrio —, Kabs REV, Krel EDA,
Production Prediction, Cycles Visualization, relatório PNM).

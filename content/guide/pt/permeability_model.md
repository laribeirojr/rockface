# Modelo de permeabilidade de perfis de imagem

## Para que serve

Uma curva contínua de permeabilidade ao longo do poço a partir de um **perfil de imagem segmentado** (p. ex.
vugs, matriz microporosa e matriz fechada num perfil de amplitude acústica), de uma **curva de porosidade** e das
**permeabilidades de plugues** medidas no laboratório. É pensado para carbonatos de dupla porosidade, em que os vugs
vistos na imagem levam boa parte do escoamento.

## Antes de começar

* Um perfil de imagem segmentado (aba Perfis de poço → Segmentação), com um segmento para os macroporos (vugs).
* Uma curva de porosidade do mesmo poço (importada de LAS, CSV…; em fração ou em %).
* As permeabilidades de plugues: profundidade (m) e K (mD), pelo menos duas dentro da imagem.

## Passo a passo

1. Abra o perfil de imagem segmentado e vá à aba **Perfis de poço**, grupo **Modelo de permeabilidade (perfil de
   imagem)**.
2. Escolha o **Perfil de imagem segmentado** e a **Curva de porosidade**.
3. Escolha o **Segmento de macroporos** (o seu expoente de porosidade é fixo em 1) e, se preciso, um **Segmento
   ignorado** (uma classe de incerteza ou de imagem ruim).
4. Ajuste a **Janela de profundidade** em que as frações dos segmentos são contadas (0: cada linha da imagem).
5. Cole os **Plugues**, um por linha: profundidade e K (espaços, tabulações ou ponto e vírgula).
6. Opcionalmente digite **Pontos forçados (Kds)** da mesma forma: profundidades e K por perto dos quais a curva deve
   passar, para corrigir uma zona de interesse.
7. Clique em **Ajustar e escrever a curva de permeabilidade**. A curva (unidade mD) é acrescentada ao poço, e o ajuste
   é mostrado: número de plugues, desajuste de log10 K, R² e A e B de cada segmento.

## Opções

| Campo | O que muda |
|---|---|
| Segmento de macroporos | O segmento cujo termo é A·F·Φ (expoente 1) |
| Segmento ignorado | Pixels deixados fora das frações |
| Janela de profundidade | Linhas reunidas numa profundidade da curva |
| Pontos forçados (Kds) | Pontos a mais no ajuste, com dez vezes o peso de um plugue |

## Como funciona

Em cada profundidade (Menezes de Jesus, Compan & Surmas 2016):

K = A1·F1·Φ^B1 + A2·F2·Φ^B2 + … + An·Fn·Φ^Bn + Am·Fm·Φ

em que Fn é a fração do segmento n nas linhas daquela profundidade, Φ a curva de porosidade interpolada nas
profundidades da imagem, Fm a fração do segmento de macroporos. A ≥ 0 e 0 ≤ B ≤ 8 são ajustados aos plugues por
mínimos quadrados em log10 K (a permeabilidade varia por décadas), a partir de vários expoentes iniciais (região de
confiança refletiva). Plugues sintéticos feitos com A e B conhecidos são recuperados exatamente.

## Por script

```python
seg = prj.log("AMP (segmentation)")
k, fit = seg.permeability_model("PHIT", [(2510.35, 120.0), (2512.10, 8.5), (2515.80, 300.0)], macro="Pore",
                                window_m=0.1)
print(fit["A"], fit["B"], fit["rms_log10"])
```

## Limites e problemas comuns

* Com poucos plugues, os termos das classes de pouca influência podem sair 0; confira os A e B mostrados e o
  desajuste.
* O modelo usa só a imagem e a porosidade; os plugues devem amostrar as classes da imagem para o ajuste valer em
  outros trechos.

## Cobertura

GI10 (modelagem de permeabilidade).

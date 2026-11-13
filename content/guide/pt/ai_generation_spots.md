# RockFace IA: modelo gerativo de um volume (SinGAN) e o ciclo de pontos

## Para que serve

**Gerar imagens de rocha.** A partir de um volume de treino — um volume de micro-CT segmentado ou de cinza — uma rede
gerativa aprende a sua textura e faz quantos volumes novos você quiser, do mesmo tamanho ou maiores, com a mesma
porosidade e os mesmos tamanhos de poros, para simulações que precisam de várias realizações ou de um volume maior
que a tomografia. Fica ao lado da geração por MPS da 0.25 (aba Multiescala).

**O ciclo de pontos.** Quando alguns pontos de análise de um projeto (microssonda, LA-ICP-MS, EDS…) têm o seu
constituinte nomeado pelo petrógrafo, um classificador aprende o constituinte a partir dos valores medidos, diz com
que frequência acerta em lâminas que não viu, e propõe um constituinte com a sua probabilidade para os pontos ainda
sem nome. Você aceita, corrige ou rejeita cada proposta; o treino seguinte as usa.

## Antes de começar

* SinGAN: RockFace IA com treino (extra `ai-train`); uma placa de vídeo para treinos 3D de tamanho útil.
* Ciclo de pontos: pontos de análise com valores (Atlas → Pontos, ou importados de CSV), pelo menos 6 pontos nomeados
  de pelo menos 2 constituintes; os constituintes são termos da nomenclatura.

## Passo a passo

### Modelo gerativo (MC → IA)

1. Abra o volume de treino (segmentado ou de cinza).
2. Em **Modelo gerativo (SinGAN)**, ajuste as **Iterações** por escala e o tamanho **Volume de treino até** (o volume
   é lido no nível que cabe nele), e clique **Treinar com o volume**. O resultado compara 4 volumes gerados com ruído
   novo com o volume de treino: porosidade, probabilidade de dois pontos (S2) e comprimento de correlação. O modelo
   fica guardado no projeto com a sua ficha.
3. Selecione o modelo na tabela (tarefa *Geração 3D*), ajuste **Volumes**, **Tamanho × treino** (1,5 faz cada lado
   1,5 vez mais longo) e **Semente**, e clique **Gerar volumes**: eles são acrescentados à amostra, como volumes de
   rótulos com a legenda do volume de treino quando ele era segmentado.
4. Para volumes grandes rode o treino como trabalho: **Multiescala → Trabalhos**, cálculo *IA: treinar um modelo
   gerativo (SinGAN)*, aqui ou num computador remoto com placa de vídeo; **Trazer os resultados** acrescenta o modelo.

### Ciclo de pontos (Lab → IA)

1. Escolha o tipo de **Pontos** e **De** *esta lâmina* ou *todo o projeto*, e clique **Aprender**. O resultado mostra
   a acurácia e as notas por classe em validação cruzada com partes por lâmina (uma lâmina nunca está ao mesmo tempo
   no treino e na validação).
2. Escolha o **Classificador** e **Propor a partir da probabilidade** (p. ex. 0,6), e clique **Propor**: a tabela lista
   os pontos sem nome com o constituinte proposto e a sua probabilidade.
3. Desmarque o que rejeita, escreva por cima de um constituinte para corrigi-lo, e clique **Aceitar marcados**: os
   constituintes são gravados nos pontos, cada um com o modelo e a probabilidade no seu registro (assim sempre se
   distingue um nome dado à mão de uma proposta aceita).
4. Aprenda de novo: o novo classificador usa também os pontos aceitos.

## Opções

| Campo | O que muda |
|---|---|
| Iterações | Passos de treino por escala da pirâmide |
| Volume de treino até | O maior volume de treino (voxels por lado); usa-se o nível do volume que cabe nele |
| Volumes, Tamanho × treino, Semente | Quantos volumes, de que tamanho e com que ruído |
| Propor a partir da probabilidade | Propostas abaixo dela não são listadas |

## Como funciona

* **SinGAN** (Shaham, Dekel & Michaeli 2019), em 3D como no módulo RockSinGAN do GeoSlicer: uma pirâmide de pequenos
  geradores convolucionais e discriminadores de recortes, treinados do grosso ao fino no único volume de treino; cada
  escala é treinada com a perda de Wasserstein com penalidade de gradiente (Gulrajani et al. 2017) mais a
  reconstrução do volume de treino a partir de um ruído fixo; o ruído de cada escala mais fina é escalado pelo erro de
  reconstrução da escala abaixo. A pirâmide inteira é um único grafo ONNX, então a geração roda em qualquer
  dispositivo.
* **Comparação**: porosidade, a probabilidade de dois pontos S2(h) ao longo de x e o comprimento em que S2 percorreu
  1/e do caminho até φ² (Torquato 2002).
* **Classificador de pontos**: a floresta aleatória da 0.23 sobre os valores (abaixo do limite de detecção = 0;
  ausente = mediana dos pontos de treino), em validação cruzada com partes agrupadas por lâmina.

## Por script

```python
vol = prj.volume("segmentação do plugue")
model, comparison = vol.ai_generator(iterations=300, max_voxels=32 ** 3)
new = vol.ai_generate(model, n=4, scale=1.5)
rid, metrics = prj.ai_spots_train(kind="geochemistry")
props = prj.ai_spots_propose(rid, kind="geochemistry", min_probability=0.6)
prj.ai_spots_accept(props, rid)
```

## Limites e problemas comuns

* Um gerador 3D treina em minutos numa placa de vídeo e em horas num processador; comece com um tamanho de treino
  pequeno e poucas iterações para conferir o resultado, depois rode o treino completo como trabalho.
* Um gerador aprende uma textura: um volume de treino com uma tendência (uma camada, uma fratura) é reproduzido como
  textura, não como tendência; use MPS com dados duros quando a disposição importa.
* As propostas de pontos só são tão boas quanto os pontos nomeados: nomeie exemplos de todos os constituintes
  esperados, de mais de uma lâmina.

## Cobertura

GM5 (geração de imagens: a rede gerativa RockSinGAN), L11 (anotação → ML → validação → extrapolação → retreino, para
geoquímica de pontos).

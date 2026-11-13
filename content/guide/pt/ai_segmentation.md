# RockFace IA: segmentar com modelos, treinar, ajustar e validar

## Para que serve

Uma rede neural treinada com muitos exemplos segmenta uma imagem, uma lâmina inteira, um volume de micro-CT ou um
perfil de imagem com um clique, e dá a área de cada classe com a confiança do resultado. Quando um modelo não se
ajusta ao seu material — outra resina, outro corante, outro tomógrafo — você **pinta alguns exemplos** e **ajusta**
o modelo: a nova versão aprende o seu material, e a sua acurácia é medida numa parte da sua anotação que ela nunca
viu. É o ciclo anotação → treino → validação → aplicação → retreino. A segmentação **sem anotação** divide uma imagem
nas suas texturas sem nenhuma anotação, e o **segmentador de instâncias** de perfis de imagem encontra os furos de
amostragem lateral e os vugs como objetos separados.

## Antes de começar

* RockFace IA instalado (veja *RockFace IA: instalação, dispositivo e o hub de modelos*). O treino precisa também do
  extra `ai-train`.
* Uma lâmina com uma imagem (Lab), ou um volume de cinza ou um perfil de imagem (MC).

## Passo a passo

### Lab — uma imagem ou uma lâmina inteira

1. Abra a lâmina no **Lab**, abra a imagem e vá à aba **IA**.
2. **Aplicar**: selecione um modelo da tarefa *Segmentação 2D* (p. ex. `rockface-thinsection-pores`) e clique
   **Segmentar a imagem (lâmina inteira, bloco a bloco)**. A imagem é classificada em resolução completa, bloco a
   bloco, e guardada como mapa de segmentação; o resultado mostra a área de cada classe, a porosidade e a confiança
   média. Um modelo da tarefa *Objetos (instâncias) 2D* treinado em imagens dá um mapa de objetos, com um número por
   grão, medido na aba **Medidas**.
3. **Treinar ou ajustar**:
   * **Anotação**: *Traços da aba Segmentação* (pinte lá exemplos de cada segmento, como para a floresta aleatória) ou
     um mapa de segmentação da imagem (feito por qualquer método, corrigido à mão), ou *Objetos: …* — um mapa de
     objetos da imagem (grãos ou poros separados na aba **Edição e objetos** e corrigidos à mão) para treinar um
     **modelo de instâncias** que separa grãos que se tocam (o modelo textural de instâncias);
   * marque **Ajustar o modelo selecionado** para partir do modelo selecionado na tabela (as classes devem coincidir);
   * escolha o **Tamanho da rede** (small, standard, large), as **Épocas**, os **Passos por época**, a parte
     **Reservado para validação** e um **Nome do modelo**, e clique **Treinar**. O resultado mostra a acurácia, o IoU
     médio e o Dice de cada classe na parte reservada; o modelo fica guardado no projeto.
4. **Validar**: escolha um **Mapa de referência** que não foi usado no treino (desta ou de outra imagem) e clique
   **Validar**: as métricas do modelo selecionado contra ele. As classes são casadas pelo nome.
5. **Sem anotação**: ajuste **No máximo / No mínimo segmentos**, **Iterações** e o **Tamanho de trabalho**, e clique
   **Segmentar sem anotação**. Os segmentos do mapa se chamam *Segment 1…k* por área decrescente; renomeie e junte-os
   na aba **Edição e objetos**.

### MC — um volume ou um perfil de imagem

1. Abra um volume de cinza e vá à aba **IA**.
2. **Aplicar**: selecione um modelo (p. ex. `rockface-microct-pores`; um modelo 2D roda fatia a fatia) e clique
   **Segmentar o volume**: um volume de rótulos com as frações, a porosidade e a confiança média.
3. **Treinar, ajustar e validar**: escolha o **Volume de cinza** e a **Anotação (volume de rótulos)** — pintada na aba
   **Floresta aleatória** ou uma segmentação corrigida à mão —, a **Rede** (2D fatia a fatia, ou 3D) e clique
   **Treinar**. Em 2D, uma parte das fatias anotadas é reservada; em 3D, blocos do volume. **Validar** mede o modelo
   selecionado contra um volume segmentado da mesma malha.
4. **Perfis de imagem**: abra um perfil de amplitude; selecione um modelo da tarefa *Objetos (instâncias) 2D* (p. ex.
   `rockface-imagelog-instances`), escolha o perfil de **Tempo de trânsito** do mesmo poço quando o modelo o recebe, e
   clique **Aplicar ao perfil de imagem**: um perfil de objetos com a tabela dos objetos (tamanhos, profundidades,
   azimutes), editável com o editor de perfis da 0.23. Um modelo de *Segmentação 2D* dá um perfil de rótulos.

## Opções

| Campo | O que muda |
|---|---|
| Tamanho da rede | small (8 filtros na primeira camada), standard (16), large (32): maior aprende mais, precisa de mais memória e tempo |
| Épocas, Passos por época | Quanto dura o treino; a rede com a melhor acurácia nos dados reservados é guardada |
| Reservado para validação | A parte da anotação deixada fora do treino para medir o modelo (blocos de 64 px em 2D, fatias ou blocos de 32 voxels no MC) |
| Ajustar o modelo selecionado | Parte desse modelo (taxa de aprendizado ×0,3); a nova versão o tem como pai |
| No máximo / No mínimo segmentos | Os limites da segmentação sem anotação |
| Menor objeto | Objetos do segmentador de instâncias abaixo desta área são descartados |

## Como funciona

* **Rede**: uma U-Net (Ronneberger, Fischer & Brox 2015) de quatro níveis com normalização por lote, em 2D ou 3D;
  perda = entropia cruzada ponderada pelas classes mais Dice, só nos pixels anotados (Milletari, Navab & Ahmadi 2016);
  AdamW (Loshchilov & Hutter 2019) com cronograma cosseno; espelhamentos e rotações de 90° aleatórios.
* **Métricas** (em dados reservados): acurácia, interseção sobre união e Dice por classe, a matriz de confusão.
* **Imagens e volumes grandes**: blocos com margem, refletidos nas bordas, classificados em lotes; a margem limita as
  emendas entre blocos.
* **Sem anotação**: uma rede pequena treinada na própria imagem, com as classes tornadas constantes nos superpixels
  SLIC e contínuas no espaço (Kanezaki 2018; Kim, Kanezaki & Tanaka 2020; Achanta et al. 2012); o número de classes
  cai à medida que a rede as junta.
* **Instâncias**: a rede classifica fundo, interior e borda dos objetos; os interiores são as sementes de um watershed
  sobre os objetos, através da emenda 0°/360° do perfil.

## Por script

```python
pic = prj.image("ILLUSTRATIVE mosaic PP")
seg, fr, por, conf = pic.ai_segment("rockface-thinsection-pores")          # lâmina inteira, bloco a bloco
model, met = pic.ai_train(map=seg, base="rockface-thinsection-pores", epochs=10)   # ajuste, métricas reservadas
print(pic.ai_validate(model, "mapa de referência"))
seg2, fr2 = pic.ai_unsupervised(max_segments=8)
grains, n = pic.ai_objects(pic.ai_train_objects("objetos dos grãos")[0])      # o modelo textural de instâncias
vol = prj.volume("tomografia do plugue")
labels, fr, por, conf = vol.ai_segment("rockface-microct-pores")
model, met = vol.ai_train("fatias pintadas", base="rockface-microct-pores")
objects, table, n = prj.log("AMP").ai_instances("rockface-imagelog-instances", transit_time="TT")
```

## Limites e problemas comuns

* "A anotação tem k classes e o modelo m": o ajuste mantém as classes do modelo; pinte os mesmos segmentos.
* "Nenhuma classe da referência coincide pelo nome com uma classe do modelo": renomeie os segmentos do mapa de
  referência.
* Um modelo aplicado a imagens de outro aumento: o modelo de lâminas que vem com o programa foi treinado mais ou menos
  na resolução das imagens GO-Forward; ajuste-o com alguns traços das suas imagens.
* Treinar no processador leva minutos para uma imagem e pode levar horas para uma rede 3D; rode treinos longos numa
  placa de vídeo ou como trabalho (MC → Multiescala → Trabalhos: *IA: treinar um segmentador de volumes*).

## Cobertura

GT18 (segmentadores pré-treinados, lâmina), GV19 (segmentadores pré-treinados de volumes), GI11 (segmentador de
instâncias de perfis de imagem), GT20 (segmentação sem anotação), L7 (quantificação da lâmina inteira por ML), L11
(anotação → ML → validação → extrapolação → retreino, para mineralogia e textura).

# Um mapa mineralógico alinhado sem pontos de controle; efeitos em volumes grandes

## Para que serve

Dois detalhes encontrados pela auditoria da 0.23 e fechados na 0.28. **Um mapa mineralógico alinhado sobre uma
segmentação da imagem** sem clicar pares de pontos (o Thin Section Auto Registration do GeoSlicer). **Os efeitos do
editor de segmentos em volumes grandes** — margem, suavização, remoção de bordas e expansão — em resolução plena,
fatia a fatia, em vez de num nível reduzido (os efeitos Big Image do GeoSlicer).

## Antes de começar

* Alinhamento: uma segmentação da imagem (Lab → Segmentação) e o mapa mineralógico da mesma lâmina, ambos com uma
  fase de poro (papel da fase "Poro"), ou com fases que mostrem as mesmas bordas.
* Efeitos: um volume segmentado no MC.

## Passo a passo

1. **Lab → Registro**: escolha a segmentação como *Imagem fixa* e o mapa mineralógico (marcado "mapa") como *Imagem
   móvel*; **Automático** (com *Busca (automática)* "translação", "qualquer giro" ou "giro e escala" quando os dois não têm
   um referencial da lâmina em comum); **Salvar o registro**. O mapa passa a ser sobreposto à imagem no Atlas e no
   Lab.
2. **MC → Segmentação → Efeitos sobre o volume segmentado**: nada muda para o usuário — um volume grande demais para ficar inteiro na memória
   agora é editado em resolução plena, algumas fatias de cada vez.

## Como funciona

* Alinhamento: os poros de cada mapa (ou, sem poros, as bordas entre duas fases quaisquer) viram uma imagem em
  cinza; as duas são alinhadas por ECC sobre seus gradientes numa pirâmide (Evangelidis & Psarakis 2008), partindo
  dos referenciais da lâmina ou da busca, como o Lab alinha duas imagens (0.17).
* Efeitos: cada bloco de fatias é lido com a margem em z que o efeito precisa (a margem ou a largura mais uma fatia,
  o tamanho da suavização mais uma) e cortado de volta depois do efeito — o mesmo resultado que no volume inteiro.
  Na *expansão* o segmento mais próximo é procurado no bloco e em 16 fatias ao redor (`halo`).

## Por script

```python
t = prj.image("Mapa mineralógico").register_on("Segmentação", search="shift")   # dois mapas: pelos poros
rf.lab.register_map(prj.raw, seg_id, map_id, fixed_phases=[1], map_phases=[3])
rf.vol_tools.edit_labels(prj.raw, labels_id, "boundary_removal", width=2)       # volumes grandes: em blocos
```

## Limites e problemas comuns

* As fases escolhidas devem ser a mesma coisa nos dois mapas (os poros da imagem e a porosidade do mapa); com
  conjuntos de fases muito diferentes use pares de pontos.
* Ilhas, operações lógicas, crescer a partir de sementes e traçado de nível continuam num nível reduzido em volumes
  muito grandes: precisam do volume inteiro de uma vez.

## Cobertura

Linhas da auditoria da 0.23 ThinSectionAutoRegistration (GT5), BoundaryRemovalBigImage e ExpandSegmentsBigImage
(GV6, GV8).

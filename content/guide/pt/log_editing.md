# Editar a segmentação de um perfil e os seus objetos

## Para que serve

Uma segmentação automática de um perfil de imagem nunca é perfeita: um vugo fica de fora, a borda de um patim vira
vugo, dois vugos se juntam. Aqui você corrige a segmentação com um pincel e revisa os objetos (vugos, manchas) um a
um: recusa os falsos, junta os pedaços de um mesmo objeto, mantém só os que têm medidas que fazem sentido.

## Antes de começar

Um perfil segmentado (aba Perfis → Segmentação, objetos e tamanhos de poro → Segmentar) ou um perfil de objetos
(… → Objetos), aberto nas trilhas do RockFace MC.

## Passo a passo

### Corrigir uma segmentação

1. Abra o perfil segmentado. Em **Pincel e objetos**, escolha o que **Pintar** (um segmento, ou **— borracha —**) e o
   **Raio do pincel** em milímetros da parede do poço.
2. Clique em **Pintar na trilha** e arraste o mouse sobre a trilha. Um traço atravessa a costura 0/360° pelo lado mais
   curto.
3. **Desfazer** volta o último traço.

### Revisar os objetos

1. Abra o perfil de objetos. A tabela lista cada objeto: profundidade (topo, base, centro), azimute, área, diâmetro
   equivalente, altura, largura, e se ele toca o topo ou a base do perfil.
2. Digite um filtro (`area_mm2 > 50 and not touches_edge`): a tabela mostra os objetos que passam; o histograma
   mostra a coluna escolhida.
3. Escolha objetos na tabela e clique em **Recusar os escolhidos** ou **Juntar os escolhidos**, ou clique em **Manter
   só as linhas mostradas** para recusar todos os objetos que o filtro esconde.
4. Para acrescentar um objeto, escolha **Um objeto novo** em **Pintar** e pinte-o; **Aumentar o objeto escolhido** e
   **Recortar o objeto escolhido** alteram o objeto escolhido na tabela.

## Como funciona

O pincel é um disco do raio dado sobre a parede desenrolada (passo de profundidade × largura da coluna, em mm). As
linhas tocadas são regravadas no lugar, com a sua pirâmide de níveis. As medidas são recalculadas a partir dos objetos
depois de cada alteração.

## Por script

```python
perfil = prj.log("Vugos (ILLUSTRATIVE)")
patch = perfil.paint([(120.0, 2510.30), (126.0, 2510.32)], radius_mm=8, value=2)
perfil.undo(patch)
objetos = prj.log("Vugos (ILLUSTRATIVE) (objects)")
tabela = objetos.instances()
recusados = objetos.keep_only("area_mm2 > 50 & touches_edge == 0")
novo = objetos.paint_instance([(200.0, 2511.0)], radius_mm=10)
```

## Limites e problemas comuns

* **"Escolha antes um objeto na tabela."** Aumentar e recortar precisam de um objeto escolhido.
* A tinta nova nunca cobre outro objeto; recortar só tira pixels do objeto escolhido.
* O segmentador de instâncias treinado do GeoSlicer vem na etapa 0.26.

## Cobertura

GI8 (Segment Editor dos perfis de imagem, Instance Segmenter Editor).

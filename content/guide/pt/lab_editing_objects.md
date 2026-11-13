# RockFace Lab: edição de mapas e objetos

## Para que serve

Uma segmentação raramente é perfeita: um grão pintado como cimento, bolhas na resina tomadas por poros, um risco. A
aba **Edição e objetos** corrige um mapa à mão sobre a sua imagem — pincel, borracha, polígono, tesoura, traçado por
nível, ilhas — e separa um dos seus segmentos em **objetos**: cada grão ou corpo de poro por si, para poder ser medido.
Os objetos podem ser unidos, divididos, cortados e apagados. Toda mudança pode ser desfeita.

## Antes de começar

Um mapa da lâmina: uma segmentação (página [RockFace Lab: segmentação e porosidade](lab_segmentation.md)) ou um mapa mineralógico ("A lâmina ainda não tem
mapas: segmente primeiro uma imagem.").

## Passo a passo

### Corrigir um mapa

1. Abra **Edição e objetos** e escolha o **Mapa**; ajuste a sua **Opacidade** sobre a imagem.
2. Marque **Editar o mapa** e escolha o **Segmento escrito**.
3. Escolha uma ferramenta:
   * **Pincel** — arraste sobre a imagem para pintar o segmento escolhido (**Raio do pincel**);
   * **Borracha** — arraste para apagar (não classificado);
   * **Polígono** — clique nos cantos; um clique duplo ou Enter o preenche;
   * **Tesoura** — desenhe um polígono: o seu interior (ou, com **Tesoura: fora do polígono**, o seu exterior) recebe
     o segmento escolhido;
   * **Traçado por nível** — clique num ponto: os pixels ligados de cor parecida (**Tolerância de cor (ΔE*ab)**)
     recebem o segmento escolhido.
4. **Ilhas menores que** e **Remover as ilhas**: os pedaços pequenos são dados à vizinhança.
5. **Desfazer** e **Refazer** — "Mudanças que podem ser desfeitas: …; refeitas: …".

Cada edição é gravada no mapa em resolução plena e em todos os níveis de zoom de uma vez.

### Objetos

1. Em **Objetos**, escolha o **Segmento a separar** (os grãos, ou os poros).
2. **Separação**:
   * ilhas — cada pedaço ligado é um objeto;
   * watershed — grãos que se tocam são separados nas suas gargantas: **Distância mínima entre centros** e
     **Suavização do mapa de distâncias (σ)**;
   * SNOW — o watershed sobressegmentado de Gostick (2017), para corpos de poro.
3. **Objetos menores que (descartados)**.
4. **Separar em objetos**. "N objetos guardados: …". Os objetos são desenhados cada um com a sua cor.
5. Edite-os com as ferramentas:
   * **Unir** — clique nos objetos e depois em **Unir os objetos marcados** ("Objetos marcados: n (pelo menos 2)");
   * **Dividir** — clique num objeto para dividi-lo por watershed;
   * **Cortar** — clique nas duas pontas de uma linha de corte;
   * **Apagar** — clique num objeto para apagá-lo.
   **Desfazer** e **Refazer** como para o mapa.

## Opções

| Opção | O que muda |
|---|---|
| Tolerância de cor (ΔE*ab) | O quanto uma cor pode diferir e ainda ser traçada. |
| Distância mínima entre centros | Maior: menos objetos, maiores. |
| Suavização do mapa de distâncias | Maior: menos divisão excessiva de grãos irregulares. |
| Objetos menores que | Objetos pequenos são descartados (ruído). |

## Como funciona

As edições são gravadas no lugar, nos blocos do mapa, com todos os níveis da pirâmide refeitos; cada edição devolve um
"remendo" de desfazer, e assim desfazer devolve exatamente o mapa de antes (conferido com mapas gravados de novo). Os
objetos são guardados como um mapa de objetos: cada pixel guarda o número do seu objeto. Em lâminas de verdade exata,
os grãos separados por watershed e SNOW foram achados com revocação de 0,78–0,83 e precisão de 0,96–0,98; com as cores
do XP a revocação subiu para 0,87–0,89 (página [RockFace Lab: medidas e distribuições de tamanho](lab_measurements.md)).

## Por script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP").segment("resin")      # um mapa de segmentação
patch = seg.paint([(100, 100), (300, 120)], 15, 1)      # pincel ao longo de uma linha, raio 15 px, segmento 1
seg.undo(patch)
seg.level_trace(420, 380, tolerance=8, phase=2)
seg.remove_islands(30)
grains = seg.objects(2, "watershed", min_distance=6, sigma=1.0, min_px=40)
print(grains.object_count())
grains.merge_objects([(1421, 842), (1422, 842)])       # um ponto em cada um de dois objetos que se tocam
grains.cut_objects((600, 300), (640, 360))
```

## Limites e problemas comuns

* "Objetos marcados: 1 (pelo menos 2)." — clique num segundo objeto antes de unir.
* Separar um mapa muito grande demora: separe antes um recorte para escolher os parâmetros.
* A tesoura também é alcançada por script para qualquer polígono (`img.scissors`).

## Cobertura

GT7 (segmentação manual: pintar, apagar, tesoura, traçado por nível, ilhas), GT9 (particionamento: ilhas, watershed,
SNOW), GT10 (editor de objetos: unir, dividir, cortar, apagar).

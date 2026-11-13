# Segmentar por exemplos pintados (floresta aleatória)

## Para que serve

Algumas fases não se distinguem por uma cor ou um valor de cinza: um cimento com a cor dos grãos, vugs com o cinza
médio da matriz. Você pinta alguns pixels (ou voxels) de cada segmento, e o programa aprende com a imagem **em volta**
deles — suavidade, textura, bordas — e classifica a imagem ou o volume inteiro. Cada traço novo o treina de novo e a
prévia muda na hora, de modo que você corrige onde ele erra.

Funciona no **RockFace Lab**, em imagens de lâmina, e no **RockFace MC**, em volumes de micro-CT.

## Antes de começar

* Lab: uma imagem de uma lâmina (uma imagem com nicóis cruzados da mesma lâmina pode entrar como segunda imagem, se
  estiver registrada sobre a primeira ou se as duas tiverem o referencial da lâmina).
* MC: um volume em cinza. Num volume grande, recorte antes uma parte representativa (**Volume → Recortar**) para
  pintar e ver rápido; depois o modelo é aplicado ao volume inteiro.

## Passo a passo

### No Lab (imagens)

1. Abra a imagem e vá à aba **Segmentação**.
2. Em **Método**, escolha **Floresta aleatória (exemplos pintados)**. Dois segmentos são propostos (poro e sólido):
   renomeie-os e acrescente outros com **Adicionar segmento**.
3. Aproxime uma parte representativa da imagem: a prévia é calculada sobre a parte que está na tela.
4. Escolha um segmento na tabela, clique em **Pintar exemplos do segmento escolhido** e pinte alguns traços sobre ele.
   Faça o mesmo para cada segmento. Pinte as bordas e os lugares fáceis de confundir.
5. Com **Atualizar a prévia a cada traço (a parte da imagem na tela)** marcado, a prévia acompanha cada traço. Veja
   onde ela erra e pinte ali.
6. Clique em **Aplicar à imagem inteira** para classificar a imagem toda no tamanho de pixel em que treinou, bloco a
   bloco, ou em **Guardar a segmentação como mapa** para guardar só a parte calculada.

### No MC (volumes)

1. Abra o volume em cinza e vá à aba **Floresta aleatória**.
2. Digite os segmentos em **Segmentos (separados por ;)** (por exemplo `Vugo; Matriz`) e clique em **Nova anotação
   neste volume**. A anotação aparece sobre os cortes.
3. Escolha o segmento em **Pintar com**, o **Raio do pincel**, e clique em **Pintar nos cortes**. Arraste o mouse em
   qualquer uma das três vistas de corte. **— borracha —** apaga; **Desfazer** volta o último traço. Marque **Esfera
   (também os cortes vizinhos)** para pintar os cortes vizinhos também.
4. Pinte alguns voxels de cada segmento, em vários cortes.
5. **Treinar e mostrar a prévia (corte z atual)** mostra o resultado numa janela do corte atual; com **Treinar de novo
   e mostrar a prévia a cada traço**, ela acompanha cada traço.
6. Clique em **Aplicar ao volume inteiro**. O resultado é um volume segmentado novo, com a sua porosidade.

## Opções

* **Atributos** — o que a floresta observa, como no Interactive Segmenter do GeoSlicer:
  * *Nítido (detalhes finos)*: o valor, gaussiana σ 1 e 2, variância local 5 × 5;
  * *Equilibrado*: o valor, gaussiana 1, 2, 4, variância 5 e 9 — um bom começo;
  * *Suave* e *Muito suave*: escalas maiores, segmentos mais suaves;
  * *Completo (todos os atributos)*: todos, mais o gradiente e o laplaciano.
* **Árvores** — mais árvores, resultado mais estável (32 basta na maioria dos casos).
* **Segunda imagem / Segundo volume (mesma grade)** — mais canais na mesma grade (a imagem XP de uma lâmina).
* **Método** (MC) — *Floresta aleatória* ou *Inferência bayesiana (gaussiana)* (cada segmento uma distribuição
  normal dos atributos).
* **Modelo** — *Treinar com os exemplos pintados*, ou um modelo guardado no projeto. Todo modelo aplicado fica
  guardado no projeto; **Exportar modelo…** grava-o num arquivo `.rfmodel` e **Importar modelo…** lê um (de um
  colega, por exemplo).

## Como funciona

* Para cada pixel ou voxel, os atributos do conjunto escolhido são calculados em cada canal (L\*, a\*, b\* de uma
  imagem colorida; o cinza de um volume). Uma floresta aleatória (Breiman 2001) de árvores de decisão aprende com os
  pontos pintados quais atributos separam os segmentos; cada ponto recebe o segmento votado pela maioria das árvores.
* Um atributo depende só dos pontos numa margem em volta dele; por isso a imagem é classificada bloco a bloco com essa
  margem e o resultado é igual ao da imagem inteira de uma vez, qualquer que seja o tamanho.
* Um modelo é guardado como números (os nós das árvores), nunca como código de programa: um modelo recebido de outra
  pessoa pode ser aberto com segurança.
* Fonte: L. Breiman (2001), *Random forests*, Machine Learning 45, 5–32; os conjuntos de atributos seguem o manual do
  GeoSlicer.

## Por script

```python
import rockface.api as rf
prj = rf.open("projeto.rockface")
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg, floresta = pp.forest(strokes=[(1, [(120, 80), (140, 90)], 6), (2, [(600, 420)], 6)],
                          segments=["Poro", "Sólido"], preset="balanced")
inteira, frações, porosidade = pp.apply_forest(floresta)
vol = prj.volume("Plugue A")
anot = vol.new_annotation(["Vugo", "Matriz"])
anot.paint("z", 40, [(30, 30), (36, 30)], 2.0, 1)
f3 = vol.train_forest(anot, name="Vugos")
seg3 = vol.apply_forest(f3)
```

## Limites e problemas comuns

* **"Pinte exemplos de pelo menos dois segmentos."** Cada segmento precisa de alguns traços.
* **A prévia está boa e a imagem inteira não.** Os traços vieram de uma parte só; pinte outras partes também.
* **"O modelo foi treinado com … canais"**: um modelo treinado com segunda imagem precisa dela agora.
* No Lab, a prévia e o treino usam os traços que estão na tela; os traços fora dela ficam guardados para depois.
* As redes pré-treinadas do GeoSlicer (U-Net) vêm na etapa 0.26.

## Cobertura

GV6, GT7, GT8 (Interactive Segmenter, Segmenter — métodos floresta aleatória e bayesiano).

# Contagem de pontos

## Para que serve

A aba **Contagem de pontos** conta a composição numa grade de pontos sobre a lâmina — por exemplo 300 pontos — na
imagem da lâmina ou com uma platina motorizada. Cada ponto guarda a sua posição em milímetros no sistema da lâmina:
uma recontagem cai nos mesmos pontos, qualquer ponto contado pode ser revisitado, e o mapa dos pontos contados mostra
a composição da lâmina. As contagens preenchem a coluna Pontos da composição.

## Antes de começar

* Uma descrição com as suas linhas de composição (página [Composição](composition.md)): você conta *como* uma das linhas.
* Salva pelo menos uma vez: a partir daí cada ponto contado é gravado no projeto na hora, e nenhum ponto se perde
  ("Salve a descrição para guardar a contagem…").
* Opcional: uma imagem da lâmina (**Imagem da lâmina…**), ou a imagem da lâmina inteira do RockFace Atlas.

## Passo a passo

### A grade

1. Abra a aba **Contagem de pontos**. Deixe o **Modo** em **Grade**.
2. Ou digite os **Pontos desejados** (por exemplo 300) e a **Área l × a (mm)** e clique em **Distribuir N pontos**, ou
   dê a grade você mesmo: **Origem x, y (mm)**, **Passo x, y (mm)** e **Colunas × linhas**.
3. **Percurso**: **Serpentina** (vai e volta) ou **Linha a linha**. Marque **Lâmina redonda** para ficar só com os
   pontos dentro de uma lâmina redonda.
4. **Criar grade**. O mapa à esquerda mostra os pontos.

### A imagem da lâmina

1. **Imagem da lâmina…** carrega uma foto da lâmina; em **Imagem e calibração** dê o seu **µm por pixel** e a
   **Origem da imagem x, y (px)** (o pixel em 0, 0 mm).
2. Os pontos são desenhados sobre a imagem. Sem imagem, os pontos são desenhados sozinhos.

### Contar

1. **Iniciar** vai ao primeiro ponto. Com **Seguir** ligado, cada contagem passa ao próximo ponto ainda não contado.
2. Escolha a linha em **Contar como** e clique em **Contar**, ou aperte a tecla da linha (1–0 e Ctrl+1–0, definidas
   em **Teclas…** da aba Composição).
3. **Pular** salta um ponto (na resina fora da lâmina, num buraco…); **Descontar** desfaz a contagem do ponto atual;
   **Voltar** volta ao ponto anterior.
4. **Observação no ponto** e **Imagens no ponto…** guardam uma nota e fotos do ponto sob a cruz.
5. O contador mostra "N de M pontos contados"; os pontos da composição acompanham na hora.

### Navegar

* Clique num ponto do mapa para ir até ele; **Ir ao ponto…** pelo número.
* **Ajustar**, **Aproximar**, **Afastar**, a roda do mouse; **Só o mapa** esconde o painel.
* O percurso seguido, o ponto atual e a posição da platina são desenhados no mapa, com os pontos contados na cor da
  sua linha.

### Com uma platina motorizada (modo livre)

1. Escolha a **Platina** (**Simulador (sem equipamento)** para praticar) e clique em **Controlador…** para movê-la
   com o teclado numérico: 8, 2, 4, 6 e as diagonais 7, 9, 1, 3.
2. **Modo → Livre**: dê o **Eixo de contagem**, o **Passo (mm)**, o **Espaçamento das travessias (mm)** e **Inverter
   x · y** para uma platina montada ao contrário. Cada contagem move a platina um passo; no fim da área ela passa à
   próxima travessia.

### Coordenadas

* **Coordenadas…** lista os pontos contados como cada constituinte, com x e y em mm; **Exportar CSV…** grava-os.
* **Importar pontos…** lê pontos de um arquivo CSV (x, y e o rótulo da linha), em mm ou em pixels com o seu tamanho.
* **Zerar contagem** esquece todos os pontos contados e mantém a grade.

## Opções

| Campo | O que muda |
|---|---|
| Pontos desejados, Área | Distribuir N pontos: passos quadrados sobre a área, exatamente N pontos. |
| Percurso | Serpentina ou linha a linha. |
| Lâmina redonda | Só os pontos dentro da elipse inscrita na área da grade. |
| Seguir | Ir ao próximo ponto não contado depois de cada contagem. |
| Eixo de contagem, Passo, Espaçamento das travessias | Modo livre com platina. |

## Como funciona

Os mesmos parâmetros de grade sempre dão os mesmos pontos (pedido L10: posições nunca perdidas,
reprodutíveis). A grade não pode ser mudada quando já há pontos contados ("Já há … pontos contados: a grade é
mantida"); zere a contagem antes. As linhas de composição que a contagem usa recebem exatamente o número de pontos
contados como elas; as outras linhas mantêm os seus pontos. Os pontos contados aparecem também no RockFace Atlas,
sobre a imagem da lâmina inteira, e nas figuras da lâmina.

## Por script

```python
d = prj["TS-9"]
q = d.add_line("quartz_mono")
c = d.add_line("calcite_dia", habit="poikilotopic", location="ig_pore_filling")
d.count.set_grid(rf.ct.grid_for(300, 20.0, 30.0))       # 300 pontos numa área de 20 × 30 mm
d.count.assign(q.uid)                                    # o ponto atual contado como quartzo; passa ao seguinte
d.count.assign(c.uid)
rf.ct.sync_points(d.composition, d.count)                # os pontos da composição acompanham a contagem
d.save()
print(d.count.counted, d.count.coordinates_by_line())
```

## Limites e problemas comuns

* "Ainda não há pontos: crie uma grade ou conte no modo livre."
* "Todos os pontos estão contados ou pulados." — a contagem está completa.
* O RockFace traz o simulador de platina; uma platina motorizada de um dado fabricante precisa do seu driver, escrito
  sobre a interface `Stage` de `rockface.core.counting` (por exemplo como plug-in).

## Cobertura

P25 (botões da platina: Iniciar, Seguir, Pular, Controlador), S1 (modo livre), S2 (registro do movimento, volta aos
pontos, ir a um ponto, zoom, cores por constituinte), S3 (mapa dos pontos contados, porcentagens, volta a qualquer
ponto), L10 (uma grade de pontos com coordenadas em cada lâmina).

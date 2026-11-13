# Mapas mineralógicos: registro, sobreposição, composição e quantificação

## Para que serve

Um mapa mineralógico de QEMSCAN, MLA, TIMA, um mapa de fases de µXRF ou qualquer imagem classificada diz qual mineral
está em cada pixel. O RockFace Atlas o registra sobre a imagem óptica da mesma lâmina, sobrepõe-no à imagem com
qualquer opacidade, gera uma **imagem composta** (o mapa misturado sobre a fotografia, com a sua legenda e escala) e
**quantifica** cada fase sobre o mapa inteiro ou sobre qualquer região — comparando o mapa com a contagem de pontos.

## Antes de começar

* Uma descrição salva cuja lâmina tenha (de preferência) uma imagem óptica da lâmina inteira no Atlas.
* O mapa em PNG ou TIFF (uma imagem de paleta, uma imagem cinza de números de fase ou uma imagem RGB das cores das
  fases) e a sua legenda: CSV ou TXT (com ou sem cabeçalho, por exemplo `Mineral,R,G,B`) ou uma tabela de cores do
  3D Slicer.

## Passo a passo

### Importar o mapa

1. No RockFace Atlas, **Mapa mineralógico…**.
2. Em **Importar um mapa mineralógico**, escolha o mapa, a sua **Legenda** (por padrão, o arquivo de legenda achado
   ao lado do mapa), a **Tolerância de cor** (o quanto uma cor de um mapa RGB pode se afastar da legenda) e o **µm por
   pixel**.
3. O RockFace lê as fases ("… pixels, N fases"). Na aba **Mapa**, confira cada fase:
   * nome da **Fase** e **Cor**;
   * **Papel**: Mineral, Poro, Fundo ou Não classificado;
   * **Conceitos**: códigos de constituintes, grupos ou tipos da nomenclatura, separados por vírgulas (por exemplo
     `quartz, quartz_dia`; `pore`) — eles ligam o mapa à nomenclatura e à contagem de pontos;
   * **Ver** esconde ou mostra uma fase; **Ver todas**, **Ocultar todas**; **Juntar** une as fases selecionadas.
4. **Salvar fases**.

### Registrar o mapa sobre a imagem óptica

1. **Registrar…** abre as duas imagens lado a lado.
2. Clique num ponto da imagem óptica (à esquerda) e depois no mesmo ponto do mapa (à direita): um canto de grão, um
   poro, um risco. Repita. Dois pares bastam para uma **similaridade** (rotação, escala, translação), três para uma
   transformação **afim**; espalhe-os pelo mapa e acrescente mais alguns.
3. A tabela dá cada **Par** com o seu **Resíduo**; **Remover par**, **Remover todos**.
4. Escolha a **Transformação** e **Aplicar**. O RockFace informa o RMS dos pares e o **erro deixando um de fora**
   (cada par previsto pelos outros), a escala e a rotação.
5. O mapa passa a ser desenhado no sistema da lâmina, sobre todas as imagens dela: no visualizador, escolha-o em
   **Por cima:** e ajuste a opacidade. **Lado a lado** mostra as duas imagens com **Mover as duas vistas juntas**.
   **Remover** desfaz o registro (o mapa volta à sua escala na origem da lâmina).

### Quantificar

1. Em **Quantificação**, escolha a **Região**: **Mapa inteiro**, **Área na tela**, ou uma anotação (um retângulo ou
   contorno desenhado em qualquer imagem da lâmina).
2. Escolha uma descrição em **Comparar com** para pôr a sua contagem de pontos ao lado do mapa.
3. **Quantificar**. A tabela dá cada fase com a **% mapa**, a **Área (mm²)**, a **% contagem** e a **Diferença**, e o
   resumo: área analisada, a parte de minerais e poros, porosidade. Os pixels de fundo e não classificados ficam fora
   das %.
4. **Exportar CSV…** grava a tabela.

### A imagem composta

1. **Composição…** abre **Imagem composta**.
2. **Imagem óptica** (por padrão a lâmina em luz polarizada plana), **Mapa desenhado como** (cores misturadas sobre a
   imagem, ou contornos das fases), opacidade, **Largura**, **Região** (imagem inteira ou a área na tela).
3. **Legenda com a % de cada fase, e barra de escala**; **Adicioná-la também à biblioteca de imagens**.
4. **OK** e grave a imagem.

## Opções

| Opção | O que muda |
|---|---|
| Tolerância de cor | Distância RGB dentro da qual uma cor do mapa é tomada como uma cor da legenda. |
| Papel | Fundo e não classificado ficam fora das %; os poros dão a porosidade. |
| Conceitos | A ligação com as linhas da composição para a comparação com a contagem. |
| Transformação | Similaridade (≥ 2 pares) ou afim (≥ 3 pares). |

## Como funciona

O registro é um ajuste de mínimos quadrados dos pares de pontos de controle; o erro deixando um de fora é uma
estimativa conservadora do erro real (cerca do dobro dele, em casos de teste com resposta conhecida: seis pares
marcados no pixel mais próximo dão 2,9 µm de RMS num mapa de 10 µm). Os blocos do mapa guardam números de fase
desenhados por uma tabela de cores, e assim as fases são mostradas, escondidas ou recoloridas na hora. Um mapa também
pode ser alinhado sobre uma segmentação sem pontos de controle (página [Um mapa mineralógico alinhado sem pontos de controle; efeitos em volumes grandes](map_alignment_big_volumes.md)).

## Por script

```python
d = prj["TS-9"]
qem = d.add_map("TS-9_qemscan.tif", legend="TS-9_qemscan.csv", um_per_px=10)
pp = prj.image("TS-9 PP")
fit = qem.register([((140, 120), (380, 288)), ((1250, 90), (1860, 314)), ((700, 520), (1102, 854)),
                    ((180, 880), (390, 1304))], model="similarity", target=pp)
print(f"RMS {fit.rms_um:.1f} µm, deixando um de fora {fit.loo_um:.1f} µm")
for row in qem.compare(d):
    print(row["phase"], round(row["map"], 1), row["count"])
qem.composite("TS-9_composicao.png", base=pp, opacity=0.5)
```

## Limites e problemas comuns

* "Esta lâmina não tem mapa mineralógico. Importe um com Mapa mineralógico…"
* "N pares: são necessários pelo menos …."
* "Não registrado e sem escala: registre-o sobre a imagem óptica."
* Um mapa RGB com cores longe da legenda: aumente a tolerância de cor, ou dê uma legenda com as cores exatas.

## Cobertura

GT2 (mapas QEMSCAN), GT5 (registro com pares de pontos de controle), L9 (sobreposição da imagem óptica e do mapa
mineralógico automatizado → imagem composta).

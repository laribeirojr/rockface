# Anotações do Atlas e a busca por conceito

## Para que serve

As anotações marcam o que uma imagem mostra — uma seta num agregado de caulinita, um retângulo em volta de um
feldspato dissolvido, o contorno de um poro, um rótulo — e ligam cada marca à nomenclatura como uma **feição**: um
constituinte com o seu hábito, localização, modificador e relação, como numa linha da composição. O RockFace escreve
a **legenda automática** da imagem a partir delas, exporta figuras com ou sem as marcas, e encontra imagens pelo que
mostram: tipo de rocha → conceito → atributo → valor.

## Antes de começar

Uma imagem aberta no RockFace Atlas (página [RockFace Atlas: lâminas inteiras, fotos de detalhe e a biblioteca de imagens](atlas_viewer.md)).

## Passo a passo

### Desenhar

1. Abra a aba **Anotações** do painel **Imagem, anotações e mapa**.
2. Escolha uma ferramenta:
   * **Seta** — clique onde ela começa, depois para onde aponta;
   * **Retângulo** — clique em dois cantos opostos; **Elipse** — dois cantos do retângulo em volta dela;
   * **Contorno** — clique nos pontos; um clique duplo, Enter ou o primeiro ponto fecha;
   * **Rótulo** — clique onde vai o texto e digite-o.
3. **Selecionar** — clique numa anotação para escolhê-la, arraste-a para movê-la, Delete a remove.
4. **Cor**, espessura da **Linha** e tamanho do **Texto**; **Aplicar estilo** os dá à anotação selecionada.

### Dizer o que ela mostra

1. Selecione uma anotação e clique em **Feição…**. Em **O que a anotação mostra**, escolha o constituinte e o seu
   hábito, localização, modificador e relação (as mesmas listas da composição).
2. **Texto…** muda o texto de um rótulo ou acrescenta um texto a qualquer anotação.
3. As anotações que dizem algo recebem as letras A, B, C… na ordem em que foram desenhadas; as letras são desenhadas
   na imagem e usadas pela legenda.

### A nota e a legenda

1. **Nota da imagem** — um texto sobre a imagem inteira, com **Adicionar feição…** para o que a imagem toda mostra;
   **Salvar a nota**.
2. **Legenda automática** — o nome, o tipo e a luz, a objetiva, a amostra, a profundidade e a lâmina, a posição na
   lâmina, a nota, "(A) …; (B) …" e a escala. **Copiar**, ou **Usar como legenda** da imagem.

### Exportar figuras

1. **Exportar imagens…**
2. **Imagens**: **A imagem aberta**, **Todas as imagens da sua lâmina** ou **As imagens listadas na biblioteca**.
3. **Anotações**: **Com anotações**, **Sem anotações** ou **Ambas (dois arquivos cada)**.
4. **Lado maior no máximo** (pixels) e **Um arquivo de legenda (.txt) junto a cada imagem**.
5. Escolha a pasta.

### Encontrar imagens por conceito

1. Na **Biblioteca de imagens**, abra **Por conceito**.
2. **Procurar em**: **as anotações das imagens**, **as composições das descrições** ou **anotações e composições**.
3. Abra a árvore **Tipo de rocha › conceito › atributo › valor** — por exemplo *Subarcósio › Caulinita › Hábito ›
   Em livros (booklet)* — e selecione um nó: a biblioteca mostra as imagens encontradas, com **Encontrada em: …** (as letras, a
   nota ou a descrição). **Mostrar todas as imagens** limpa a busca.

## Opções

| Opção | O que muda |
|---|---|
| Cor, Linha, Texto | O estilo da anotação (também nas figuras exportadas). |
| Feição | O que a anotação mostra, com a nomenclatura do RockFace. |
| Procurar em | Buscar nas anotações, nas composições das lâminas, ou em ambas. |

## Como funciona

As anotações são guardadas nos pixels de resolução plena da sua imagem, e por isso ficam no lugar em qualquer zoom e
em qualquer exportação. As feições usam os códigos da base de conhecimento; assim, uma legenda é escrita no idioma da
interface (ou da exportação), e a busca acha uma imagem qualquer que seja o idioma em que foi anotada. O tipo de rocha
de uma imagem é a classificação das descrições da sua lâmina.

## Por script

```python
img = prj.image("Field B — kaolinite booklets")
img.annotate("rect", [[820, 410], [1260, 760]], features=[rf.Feature("kaolinite", habit="booklet")])
img.annotate("label", [[1300, 420]], text="Kln")
img.note("Livretos de caulinita preenchem os poros.", [{"constituent": "kaolinite"}])
print(img.caption_auto("pt"))
for found, reasons in prj.search_images(concept="kaolinite", attribute="habit", value="booklet"):
    found.export(f"{found.name}.png", max_side=3000, annotated=True, caption_file=True)
prj.export_images("figuras", annotated=True, caption_file=True, lang="pt")
```

## Limites e problemas comuns

* Uma feição com um código desconhecido pela base de conhecimento é recusada.
* Só uma nota por imagem: uma nova nota substitui a anterior.
* "Excluir esta anotação?" — excluir não pode ser desfeito; as letras das outras acompanham.

## Cobertura

R2 (busca hierárquica: tipo de rocha → conceito → atributo → valor), R3 (editor de imagens: setas, contornos, letras,
notas; feições com a nomenclatura).

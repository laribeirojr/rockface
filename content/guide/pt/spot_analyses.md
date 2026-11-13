# Análises pontuais: geoquímica, datação e inclusões fluidas

## Para que serve

Uma **análise pontual** é uma medida feita num ponto da lâmina: uma análise por ablação a laser ou microssonda, uma
data U-Pb, uma microtermometria de inclusões fluidas. O RockFace Atlas guarda cada ponto no seu lugar no sistema da
lâmina, com os seus valores e incertezas, o mineral analisado e uma foto da área; assim o ponto é desenhado no mesmo
lugar em todas as imagens da lâmina, pode ser reencontrado no instrumento e é alcançado a partir de uma consulta ou de
uma figura.

## Antes de começar

* Uma descrição salva cuja lâmina esteja no Atlas, com uma imagem calibrada.
* Para tabelas de laboratório: um arquivo CSV com o nome do ponto, x e y, e as colunas de valores.

## Passo a passo

### Acrescentar um ponto à mão

1. No RockFace Atlas, escolha a ferramenta **Ponto** e clique onde a análise foi feita — ou **Novo…** na aba
   **Pontos**.
2. Em **Análise pontual**, dê o **Tipo** (geoquímica, datação, inclusão fluida, outro), o nome do **Ponto** (dado em
   ordem — G01, D01, FI01… — quando fica vazio), a **Posição (x, y)**, o **Tamanho do ponto**, **Método**,
   **Laboratório**, **Data** e **Analista**.
3. O **Mineral** analisado e a sua **Localização**, da nomenclatura.
4. **Valores**: **Adicionar valor** para cada um — **Nome**, **Valor**, **±**, **Nível** (1s, 2s), **Unidade**, **< LD**
   (abaixo do limite de detecção). **Campos usuais do tipo** preenche os nomes usuais (razões U-Pb, Th e Tm gelo…).
5. **Metadados** (**Adicionar metadado**) para o resto; **Foto da área** liga uma foto de detalhe; **Notas**. **OK**.

### Importar uma tabela de laboratório

1. Na aba **Pontos**, **Importar tabela…**.
2. Escolha o CSV e as **Coordenadas da tabela**: referencial da lâmina (mm ou µm), pixels de uma imagem calibrada, ou
   um referencial de instrumento (abaixo).
3. **Tipo (quando a tabela não traz)**.
4. O RockFace lê as linhas ("N linhas; M com erros ficarão de fora") e mostra cada **Linha** com os seus
   **Problemas**. Colunas de valores como `Sr (ppm)` tiram a unidade do cabeçalho; a incerteza vem numa coluna `±`,
   `2s`, `err` ou chamada `Sr 2s`; `<0.5` está abaixo do limite de detecção; colunas de texto viram metadados.
5. **OK**.

### Referenciais de instrumento: reencontrar um ponto

1. **Referenciais…** abre **Referenciais de instrumento da lâmina**. Dê o nome do **Instrumento** e a **Sua
   unidade**.
2. Leia as mesmas marcas — fiduciais, riscos, cantos de grãos — no instrumento (**Instrumento x, y**, ou **Ler a
   platina**) e na imagem da lâmina (**Lâmina x, y (mm)**). **Adicionar marca** para cada uma; duas marcas bastam
   para uma similaridade, três para uma transformação afim, uma quarta confere as outras.
3. **Ajustar**: o RMS das marcas e o erro deixando uma de fora.
4. Depois, **Platina ao ponto** manda a platina a um ponto selecionado, nas coordenadas do próprio instrumento.
   Calibre de novo depois de recolocar a lâmina no suporte.

### Ver os pontos

* A aba **Pontos** os lista por tipo (**Mostrar**: **Todos os tipos** ou um), com os seus valores. **Mostrar**
  centraliza o visualizador num ponto; **Na imagem** os desenha; **Editar…**, **Excluir**.
* **Foto da área…** acrescenta ou abre a foto da área do ponto.
* **Exportar CSV…** — uma linha por ponto, uma coluna por valor com a sua incerteza.
* **Figura dos pontos** — a lâmina com os pontos rotulados, os **Pontos contados de:** uma descrição, e **Com o mapa
  mineralógico (se registrado)**; **Salvar figura…**.

## Opções

| Campo | O que é |
|---|---|
| Nível | O nível da incerteza: 1s ou 2s. |
| < LD | Abaixo do limite de detecção (o valor é o limite). |
| Coordenadas da tabela | mm, µm, pixels de uma imagem, ou um referencial de instrumento. |

## Como funciona

Os pontos são guardados em milímetros do sistema da lâmina, nunca só nas coordenadas do instrumento: um referencial
de instrumento é uma transformação (similaridade ou afim) ajustada sobre marcas, e assim o mesmo ponto é achado em
qualquer instrumento que tenha o seu referencial. Alguns valores são derivados e mostrados (nunca guardados), cada um
com a sua fonte: a salinidade de uma inclusão fluida a partir do Tm gelo (Bodnar 1993) e a idade ²⁰⁶Pb/²³⁸U a partir
do ²³⁸U/²⁰⁶Pb (constante de decaimento de Jaffey et al. 1971, sem correção de chumbo comum). Os pontos U-Pb são
datados juntos no RockFace Explorer (página [Datação U-Pb no diagrama de Tera-Wasserburg](dating.md)).

## Por script

```python
d = prj["TS-9"]
d.calibrate_frame("LA-ICP-MS stage", [((41250, 18630), (1.0, 1.0)), ((57240, 18965), (17.0, 1.0)),
                                      ((41020, 29380), (1.0, 11.75))], unit="um")
d.import_spots("TS-9_U-Pb.csv", coords="frame", frame="LA-ICP-MS stage", kind="dating")
fi = d.add_spot("fluid_inclusion", 4.184, 3.488, values=[rf.Value("Th", 118.5, 1.0, "°C", "1s"),
                                                         rf.Value("Tm ice", -12.3, 0.2, "°C", "1s")],
                method="microthermometry", constituent="quartz_dia")
print(rf.spots.derived(fi))                              # salinidade 16,24 % em peso NaCl eq. (Bodnar 1993)
print(d.to_frame("LA-ICP-MS stage", fi.x_mm, fi.y_mm))   # onde ele fica no instrumento
d.spot_figure("TS-9_pontos.png")
```

## Limites e problemas comuns

* "Esta lâmina não tem referencial de instrumento: adicione um com Referenciais… (marcas fiduciais)."
* Um nome já usado na lâmina é recusado; valores implausíveis (um ppm negativo, rho fora de −1…1) só geram aviso.
* A idade U-Pb derivada não tem correção de chumbo comum: use a datação do Explorer para idades.

## Cobertura

L3 (ligações com as análises pontuais, com fotos das áreas analisadas), L12 em parte (análises pontuais com imagens
de detalhe e datação).

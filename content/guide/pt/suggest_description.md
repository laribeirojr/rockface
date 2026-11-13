# Sugerir descrição: do mapa de segmentação à descrição

## Para que serve

Um mapa de segmentação já diz quanto da lâmina cada mineral e os poros ocupam. **Sugerir descrição** transforma isso
em propostas para a descrição da lâmina — uma linha de composição para cada constituinte com seus pontos, a
porosidade visual e, de um mapa de objetos de grãos, a moda granulométrica principal e a seleção — e grava só o que
você marcar. Poupa digitar o que o mapa já mediu e mantém o petrógrafo no comando.

## Antes de começar

* No Lab, uma lâmina com mapa de segmentação: feito em **Lab → Segmentação**, por um modelo de IA em **Lab → IA**, ou
  importado como mapa mineralógico no Atlas.
* Uma descrição dessa lâmina (criada no Petro).
* As fases do mapa nomeadas com conceitos da nomenclatura (a legenda do mapa; Atlas → mapa mineralógico → fases).

## Passo a passo

1. **Lab** → escolha a lâmina; abra o mapa (ou mantenha qualquer imagem: é usado o último mapa da lâmina).
2. Clique em **Sugerir descrição** na barra de ferramentas. Se a lâmina tem várias descrições, escolha uma.
3. A janela mostra a sugestão como uma frase e uma caixa de seleção por item:
   * cada constituinte com sua fração da área contada e seus pontos numa contagem de 300 pontos — quando a fase do
     mapa admite vários constituintes (uma fase chamada "quartzo"), os outros aparecem (*ou …*) para conferir;
   * a porosidade visual (as fases de poro);
   * a moda granulométrica e a seleção, quando um mapa de objetos de grãos é dado (script).
4. Desmarque o que não quer e clique em **Gravar o que está marcado**. Cada linha gravada diz na observação que foi
   sugerida a partir do mapa.

No painel da Mio, `@mio sugira a descrição de ILL-NL-003` (ou a skill *ficha da amostra*) mostra a mesma sugestão
como texto, sem gravar nada.

## Opções

| Item | Gravado em |
|---|---|
| Linha de composição | a composição: uma linha nova com os pontos, ou os pontos do mesmo constituinte substituídos |
| Porosidade visual | o sistema poroso: porosidade total |
| Granulometria | a textura da lâmina: moda principal (mm e classe de Wentworth) |
| Seleção | a textura da lâmina: classe de seleção e σI |

## Como funciona

* O mapa é quantificado sem as fases de fundo e não classificadas (como em Atlas → mapa mineralógico); a fração de
  cada fase vira pontos de uma contagem de 300 pontos, arredondados (uma fração abaixo de um ponto aparece mas não é
  aplicável).
* Os conceitos da fase dão o constituinte: o primeiro constituinte nomeado, ou o primeiro constituinte de um grupo
  nomeado; o tipo (primário, diagenético, poro) vem da base de conhecimento.
* Granulometria e seleção são as medidas gráficas de Folk & Ward (1957) dos diâmetros de Feret máximos dos objetos de
  grão, classificadas por Wentworth (1922) e pelos termos de seleção de Folk & Ward.
* A frase é escrita a partir de um modelo em português, inglês ou espanhol, então todo número é um número do mapa; um
  modelo de linguagem pode reescrevê-la, e a reescrita só é mantida com exatamente os mesmos números.

## Por script

```python
d = prj["ILL-NL-003"]
s = d.suggestion()                                   # o último mapa da sua lâmina
print(rf.suggest.text(s, "pt", prj.kb))
print([(i.key, i.percent, i.points) for i in s.items])
d.apply_suggestion(s, accept=["porosity", "line:calcite_dia"])
s = prj.suggest_description("meu mapa", objects="meus grãos")      # com granulometria e seleção
```

## Limites e problemas comuns

* "Esta lâmina não tem mapa de segmentação": faça um em Lab → Segmentação ou Lab → IA.
* Uma fase nomeada só por um tipo ("Cimento") aparece mas não é aplicável: nomeie-a com um constituinte na legenda do
  mapa.
* Os pontos substituem os do mesmo constituinte na composição (sem hábito nem localização); linhas com hábito ou
  localização ficam como estão.

## Cobertura

"Segmentação transformada em sugestões de descrição" da etapa 0.27 do ROADMAP; L7 (quantificação da lâmina inteira)
levada para a descrição.

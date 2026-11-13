# RockFace Explorer: consultas, tabelas de resultados e exportações

## Para que serve

O RockFace Explorer faz perguntas a uma coleção inteira: *quais amostras têm barita?*, *quais amostras do poço X têm
datação U-Pb?*, *os grainstones com porosidade acima de 15 % e permeabilidade acima de 100 mD*. Uma consulta pode usar
qualquer conceito de uma descrição — identificação, textura, composição com os seus atributos, sistema poroso,
petrofísica, análises, classificações, totais, a interpretação diagenética, imagens, análises pontuais, mapas
mineralógicos — e dá as descrições encontradas, uma tabela de qualquer conceito para elas com as suas fotos, e
exportações.

## Antes de começar

* Um projeto com descrições. Para experimentar o Explorer: Ajuda → **Abrir a coleção ILUSTRATIVA** (48 descrições).
* Uma pergunta também pode ser digitada em linguagem natural na caixa de busca no alto (página [Mio: perguntas em linguagem natural e o modelo de linguagem local](mio.md)).

## Passo a passo

### Abrir o Explorer

**Início → Coleção → Explorer** (Ctrl+Shift+E), ou `rockface explorer projeto.rockface`. A aba **Consulta** se abre.

### Uma consulta simples

1. **Atributos**: um atributo da identificação (poço, campo, formação, zona, fácies, tipo de rocha, profundidades,
   tipo de amostra, usos…).
2. **Valores (descrições)** lista os seus valores com o número de descrições que têm cada um. Marque ou selecione um
   ou mais.
3. Para um número, dê o **Intervalo numérico**: **De** e **Até** (uma ponta pode ficar vazia); "Encontrado: … a …"
   mostra o intervalo na coleção.
4. **Adicionar aos critérios**. O critério aparece em **Critérios de seleção (Del remove)**.
5. Acrescente mais critérios: uma descrição precisa atender a todos. "N de M descrições atendem a todos os
   critérios."

### Uma consulta avançada

1. **Avançada** mostra os **Conceitos**: Identificação, Textura macroscópica e microscópica, Composição primária,
   Composição diagenética, Poros na composição, Sistema poroso, Petrofísica, Análises de laboratório, Classificações,
   Totais, Interpretação diagenética, Imagens, Análises pontuais, Mapas minerais.
2. Escolha um conceito, depois um atributo e os seus valores ou intervalo, e **Adicionar aos critérios**.
3. Dentro de um conceito, os critérios precisam ser atendidos pela **mesma linha**: "constituinte diagenético =
   calcita" e "hábito = poiquilotópico" acham as amostras com calcita poiquilotópica, não as que têm alguma calcita e
   alguma coisa poiquilotópica.

### A tabela de resultados

1. **Descrições encontradas** as lista; escolha algumas para ver só elas na tabela e exportá-las (nenhuma escolhida:
   todas).
2. **Tabela de**: o conceito a mostrar — por exemplo Petrofísica, ou Composição diagenética com a fração de cada
   linha. **Todas as linhas** mostra todas as linhas das descrições encontradas, não só as que atendem aos critérios.
3. A coluna **Fotos** dá o número de imagens de cada lâmina; selecione uma linha para ver a foto, clique duas vezes
   para abrir a descrição no RockFace Petro.
4. Clique no cabeçalho de uma coluna para ordenar.

### Salvar e exportar

* **Salvar consulta…** (dê um nome), **Abrir consulta…**, **Nova consulta**; o diálogo **Consultas salvas** também
  as **Carrega** e **Exclui**. As consultas ficam no projeto.
* **Exportar**:
  * **Tabela de resultados para Excel ou CSV…** — os números continuam números;
  * **Descrições encontradas (HTML, Excel, PDF, Word)…** — pelo diálogo de relatório (página [Relatórios](reports.md));
  * **Descrições selecionadas na tabela para HTML…** ou **para XML…** (um arquivo de intercâmbio, página
    [Exportar e importar descrições](exchange.md));
  * **Poços para LAS (Petrel)…** e **Apresentação da consulta (.pptx)…** (página [Grupos, figuras e apresentações](groups_figures.md)).
* **Ler de novo** recarrega as descrições depois de mudanças feitas no Petro.

## Opções

| Opção | O que muda |
|---|---|
| Avançada | Todos os conceitos em vez de só a identificação. |
| Todas as linhas | Todas as linhas das descrições encontradas, não só as que atendem aos critérios. |
| Descrições encontradas (escolhidas) | Limitam a tabela e as exportações a elas. |

## Como funciona

Cada descrição é lida em *fatos*, por conceito: uma linha por linha de composição, por análise, por ponto, por fase de
mapa… Uma descrição atende à consulta quando, para cada conceito citado, uma mesma linha atende a todos os critérios
daquele conceito, e todos os conceitos são atendidos. Os fatos são lidos em cerca de 8 ms por descrição e uma consulta
é respondida em cerca de 1 ms sobre 480 descrições. Os modelos ficam de fora.

## Por script

```python
with rf.open("colecao.rockface") as prj:
    print([d.name for d in prj.query(("diagenetic", "constituent", "barite"))])          # quais amostras têm barita?
    print([d.name for d in prj.query(("spots", "system", "U-Pb"), well="ILLUSTRATIVE-A2")])   # datadas, no poço A2
    boas = prj.query(("petrophysics", "porosity", 15, None), ("petrophysics", "permeability", 100, None))
    prj.save_query("Bom reservatório", ("petrophysics", "porosity", 15, None))
    header, rows = prj.query_table("petrophysics", facies="Grainstone")
    prj.export_table("boas.xlsx", "petrophysics", ("petrophysics", "porosity", 15, None))
```

## Limites e problemas comuns

* "Marque ou selecione ao menos um valor." / "Digite números para o intervalo (uma ponta pode ficar vazia)."
* "A consulta ainda não tem critérios." / "Dê um nome à consulta."
* "Nada a exportar: nenhuma descrição encontrada ou selecionada."

## Cobertura

Q1 (consulta simples), Q2 (consulta avançada sobre todos os conceitos), Q3 (intervalos numéricos), Q4 (lista de
critérios), Q5 (tabela de resultados), Q6 (consultas salvas), Q7 (exportação para Excel), Q8 (descrições encontradas
para HTML, Excel e PDF), Q9 (descrições selecionadas para HTML e XML), Q10 (configuração da exportação), Q11 (coluna de
fotos), L1 (busca: "quais amostras têm barita?").

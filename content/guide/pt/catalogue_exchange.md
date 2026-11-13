# Catálogo de amostras, tabela para o Touchstone e XML por mapeamento

## Para que serve

**Catálogo de amostras** percorre os poços e amostras de um catálogo corporativo e importa os arquivos escolhidos. A
**Tabela para o Touchstone** grava as grandezas petrográficas que a modelagem diagenética usa. **Importar XML com um
mapeamento** lê descrições gravadas por outro programa.

## Antes de começar

* Catálogo: uma pasta compartilhada `<poço>/<amostra>/` (com um `sample.json` opcional de `top_m`, `base_m`,
  `type`), ou uma plataforma OSDU com token em `ROCKFACE_OSDU_TOKEN`.
* Importar XML: o arquivo XML e um mapeamento (JSON) que diz onde está cada coisa nele.

## Passo a passo

1. **Petro → Início → Catálogo de amostras…**: escolha *Pasta compartilhada* ou *Plataforma OSDU*, o endereço,
   **Conectar**; busque um poço; marque os arquivos das amostras; **Importar os arquivos marcados**. Imagens vão para
   o Atlas, volumes para o MC, LAS para os perfis do poço, laudos em PDF para as análises da amostra.
2. **Petro → Início → Tabela para o Touchstone…**: escolha onde salvar o CSV.
3. **Petro → Início → Importar XML com um mapeamento…**: escolha o XML e depois o mapeamento. Os códigos sem
   correspondência são listados.

## Opções

| Chave do mapeamento (XML) | Significado |
|---|---|
| description | caminho do elemento de uma descrição (ex. `.//description`) |
| name, well, top_depth, thin_section | caminhos dentro dele (`@atributo`, `filho`, `filho/@atributo`) |
| line, code, percent, points | as linhas de composição e seus campos |
| codes | os códigos do outro programa → constituintes do RockFace |

O mapeamento do Touchstone lista as colunas: cada uma um campo (nome, poço, profundidade, granulometria, seleção) ou
uma soma de totais ou constituintes.

## Como funciona

* O catálogo usa conectores com as mesmas três perguntas (poços, amostras, um arquivo): uma pasta, ou o serviço de
  busca do OSDU (`POST /api/search/v2/query`). O poço e a amostra são encontrados ou criados pelo nome e pela
  profundidade.
* O formato de entrada do Touchstone não é publicado: a tabela traz as grandezas do modelo publicado (Lander &
  Walderhaug 1999; Lander et al. 2008) e diz na primeira linha que não é esse formato.
* XML por mapeamento: todo código precisa corresponder a um constituinte da nomenclatura; nada é adivinhado.

## Por script

```python
cat = rf.catalogue.FolderConnector("//servidor/catalogo")
s = cat.samples("ILL-WELL-A")[0]
rf.catalogue.import_items(prj.raw, cat, s, s.items)
prj.touchstone_table("touchstone.csv")
prj.import_mapped_xml("descricoes.xml", mapeamento)
```

## Limites e problemas comuns

* Um conector para um catálogo corporativo de amostras será adicionado quando a sua interface for documentada para o RockFace.
* O XML de outro programa e o "formato do Touchstone" só terão esse nome depois que arquivos reais forem lidos.

## Cobertura

GV16 (navegador de catálogo; conector corporativo pendente), P35 (Touchstone; definitivo com um arquivo real), P37
(importador de XML).

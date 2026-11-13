# Exportar poços para WITSML e amostras para o OSDU

## Para que serve

* **WITSML** (Energistics) é o formato de dados de poço que os programas de modelagem de reservatório e de dados de
  poço leem. Com ele, a petrografia das amostras, e os perfis de imagem e as curvas do RockFace MC, ficam ao lado
  dos outros perfis do poço.
* **OSDU** é a plataforma aberta de dados da indústria de energia. O manifesto dela permite carregar numa
  plataforma OSDU os poços, amostras, lâminas, descrições, análises de laboratório e imagens de um projeto,
  inclusive no serviço de amostras de rocha e fluido (RAFS).

## Antes de começar

* **Para o WITSML:** as amostras precisam de poço e profundidade. As curvas são as da exportação LAS do Explorer.
* **Para o OSDU:** peça ao gestor de dados da plataforma a **partição de dados** e a **etiqueta legal** a usar.

## Passo a passo

### WITSML

1. No RockFace Petro, escolha **Início → Relatórios e intercâmbio → Exportar WITSML**.
2. Escolha uma pasta. O RockFace grava, para cada poço:
   * `<poço>_well.xml` e `<poço>_wellbore.xml`: o poço e a trajetória;
   * `<poço>_samples_log.xml`: uma linha por profundidade de amostra, com porosidade e permeabilidade de
     laboratório, densidade de grãos, porosidade visual e fácies;
   * um `<poço>_<perfil>_log.xml` para cada perfil do RockFace MC. Os perfis de imagem viram curvas de vetor, um
     valor por azimute.
3. Carregue os arquivos no programa de destino como objetos well, wellbore e log do WITSML 1.4.1.1.

### OSDU

1. Escolha **Início → Relatórios e intercâmbio → Exportar manifesto OSDU**.
2. Escolha o nome do arquivo e digite a **partição de dados** e a **etiqueta legal**. Uma etiqueta vazia grava um
   marcador, a ser substituído antes da carga.
3. Entregue o arquivo JSON à carga por manifesto da plataforma.

## Opções

Por script ou pela linha de comando você escolhe:

* as descrições;
* as curvas do perfil das amostras e a profundidade usada (medida, corrigida, ajustada);
* se entram os perfis do MC e os perfis de imagem;
* no OSDU, os grupos de acesso e os países.

## Como funciona

* **WITSML.** O RockFace grava WITSML 1.4.1.1 com código próprio. A ordem dos elementos segue o esquema WITSML
  1.4.1.1. O índice é a profundidade medida em metros; valores ausentes ficam vazios, com `-999.25` como valor nulo.
* **OSDU.** Poços e trajetórias viram `master-data--Well` e `master-data--Wellbore`. Amostras e lâminas viram
  `master-data--Sample` (a lâmina é uma amostra filha da sua amostra). Descrições e análises de laboratório viram
  `work-product-component--SamplesAnalysis`, e imagens `work-product-component--SampleImage`.
  * A petrografia — composição com porcentagens, classificações, os códigos da nomenclatura do RockFace — vai em
    `ExtensionProperties.RockFace`, porque o OSDU ainda não tem um esquema de petrografia.
  * A tabela de correspondência está em `docs/SERVER.md`.

## Por script

```python
import rockface.api as rf
with rf.open("projeto.rockface") as prj:
    prj.export_witsml("pasta_witsml")
    prj.export_osdu("manifesto.json", partition="minha-particao", legal_tag="minha-particao-legal")
```

Ou: `rockface export witsml projeto.rockface pasta` e `rockface export osdu projeto.rockface manifesto.json
--partition minha-particao --legal-tag minha-particao-legal`.

## Limites e problemas comuns

* **Validação do WITSML.** Os arquivos foram conferidos relendo-os, não contra os arquivos oficiais do esquema. Se
  algum programa os recusar, avise pelo formulário de feedback.
* **Versões dos esquemas OSDU.** As versões usadas estão escritas no manifesto. Se a plataforma usar outras, o
  gestor de dados pode precisar ajustá-las.
* **Imagens.** Os registros de imagem do OSDU descrevem as imagens; os arquivos de imagem ficam no RockFace. Exporte
  as imagens pelo Atlas para anexá-las como conjuntos de dados.

## Cobertura

P38 (exportação WITSML), L13 (OSDU).

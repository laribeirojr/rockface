# Importar descrições de outro programa (XML)

## Para que serve

As descrições de lâminas feitas em outro programa de petrografia podem entrar no RockFace sem serem digitadas de
novo, quando esse programa grava cada descrição como um arquivo XML cujo elemento raiz é
`ThinPetrographicDescription`. O RockFace lê a identificação, o cascalho, a areia e a lama, a composição com seus
pontos e porcentagens e o ambiente diagenético interpretado, e acrescenta tudo ao projeto como descrições do RockFace.

## Antes de começar

* **No programa de origem**, exporte as descrições como arquivos XML (um arquivo por descrição). O idioma da
  exportação não importa.
* **Este arquivo não:** uma exportação para o Touchstone (Geocosm) também é XML, mas não é uma descrição. O
  RockFace a reconhece e avisa.
* **No RockFace**, abra o projeto que vai receber as descrições.

## Passo a passo

1. No RockFace Petro, escolha **Início → Relatórios e intercâmbio → Importar descrições de outro programa (XML)…**.
2. Escolha **Arquivos…** (um ou mais XML) ou **Pasta…** (todos os arquivos de descrição da pasta).
3. A tabela de cima lista as descrições encontradas, com o número de linhas de composição e se o nome já existe no
   projeto. Desmarque as que não quiser.
4. A tabela de baixo lista os **números sem correspondência**: cada termo do outro programa tem um número. Para
   cada linha, escolha o termo do RockFace correspondente, ou deixe **(não importar: guardar como texto)**.
5. Deixe marcado **Lembrar estas correspondências neste projeto**, para que os próximos arquivos não precisem de nada.
6. Escolha o que fazer com um nome que já existe no projeto (renomear, pular, substituir) e clique **Importar**.

## Opções

| Opção | O que faz |
|---|---|
| Lembrar estas correspondências | Os números que você ligou ficam no projeto e valem para as próximas importações |
| Nome já no projeto | **Renomear** acrescenta "(2)", **Pular** mantém a existente, **Substituir** apaga e importa de novo |
| (não importar: guardar como texto) | A linha não é importada; vai, com nome, número e quantidade, para as notas da composição |

## Como funciona

* **Os números.** Cada termo no arquivo tem um nome, no idioma da exportação, e um número que não muda
  com o idioma. O RockFace leva os números aos seus próprios termos. Vêm prontos só os números cujo significado foi
  conferido como igual nos dois programas. Os outros você liga uma vez.
* **Nada é adivinhado.** Uma linha cujo termo não tem correspondência fica como texto nas notas da composição. Um
  atributo (localização, hábito, modificador, relação paragenética) sem correspondência, ou que o termo do RockFace não
  aceita, sai da linha e também vai para as notas. Ligue o número e importe de novo com **Substituir**.
* **Identificação.** Descrição, lâmina, testemunho, caixa, plug, poço ou afloramento, profundidades de topo e base,
  campo, unidade, bacia, país, estado, instituição, petrógrafo, observação e usos vão para os seus campos. Lugar,
  projeto, digitador, datas de edição, classe da rocha, suporte e o ambiente interpretado não têm campo no RockFace:
  são gravados, como estão, num bloco das observações com o título "[Importado de XML (ThinPetrographicDescription)]".
* **Pontos e porcentagens.** Quando a descrição foi contada, os pontos são importados e o RockFace calcula as
  porcentagens. Senão, as porcentagens são importadas. Os totais gravados no arquivo não são importados: o RockFace
  calcula os seus.
* O RockFace guarda só os números do outro programa e os seus próprios termos. Não copia nomes, definições nem
  regras desse programa.

## Por script

```python
import rockface.api as rf

print(rf.read_tpd("D-01.xml")["lines"])
with rf.open("projeto.rockface") as prj:
    res = prj.import_tpd(["exportacoes/"])
    print(res["unknown"])                      # números para ligar uma vez
    prj.save_tpd_mapping({"constituent": {"115": "quartz_mono"}})
    prj.import_tpd(["exportacoes/"], on_conflict="replace")
```

## Limites e problemas comuns

* **Imagens e coordenadas dos pontos** não estão nesses arquivos XML.
* **Linhas nas notas.** Ligue os números delas na tabela de baixo e importe de novo com **Substituir**.
* **Outras versões do formato.** Os arquivos lidos até agora foram gravados com a versão 3.3.0 do
  formato. Outras versões são lidas do mesmo modo. Por favor, informe pelo formulário de opinião um arquivo que não
  for lido.
* **O outro sentido** — arquivos gravados pelo RockFace para o outro programa e para o Touchstone — virá numa versão
  posterior, quando houver os arquivos necessários para conferi-lo.

## Cobertura

P37 (importador de XML; os arquivos do próprio programa de origem lidos desde a 0.32).

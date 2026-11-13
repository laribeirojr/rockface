# Composição

## Para que serve

A aba **Composição** é a tabela do que forma a rocha: constituintes primários, constituintes diagenéticos e tipos de
poro, cada um com os seus atributos (localização, hábito, modificador, relação paragenética) e a sua quantidade —
pontos contados, uma porcentagem manual ou uma estimativa visual. Totais, classificações, a interpretação
diagenética, relatórios e consultas são todos calculados a partir dela.

## Antes de começar

Uma descrição aberta. Os constituintes e atributos vêm da base de conhecimento (página
[Nomenclatura, escalas e referências (a base de conhecimento)](nomenclature_knowledge_base.md)).

## Passo a passo

### Acrescentar linhas

1. Abra a aba **Composição**.
2. **Adicionar…** (Ins). No diálogo **Linha de composição**, escolha o **Constituinte** nas listas agrupadas
   (constituintes primários, constituintes diagenéticos, poros); digite no filtro para achá-lo em qualquer idioma.
3. Dê os atributos que o seu tipo admite:
   * primário — **Localização**, **Modificador**;
   * diagenético — **Hábito**, **Localização**, **Modificador**, **Relação** (paragenética), **Constituinte
     relacionado** e **Sua localização**;
   * poro — **Localização**, **Modificador**, **Relação**, **Constituinte relacionado**.
4. Dê a quantidade, uma destas:
   * **Pontos** — pontos contados;
   * **% manual** — uma porcentagem medida de outra forma;
   * **Quantidade nominal** — uma estimativa visual nos degraus dos gráficos de comparação (traço, 1, 2, 3, 5, 7, 10,
     15, 20, 25, 30, 40, 50 %).
5. **Observação** — uma nota sobre esta linha. **OK**.

O mesmo constituinte pode aparecer em várias linhas com atributos diferentes (por exemplo, calcita como cimento
poiquilotópico intergranular e como substituição de feldspato).

### Contar por cliques e teclas

* Um **duplo clique** na célula de Pontos de uma linha acrescenta um ponto; **Alt + duplo clique** tira um.
* **Teclas…** atribui linhas às teclas 1–0 e Ctrl+1–0 (vinte teclas): apertar uma tecla soma um ponto à sua linha.
* A linha abaixo da tabela mostra os pontos e as frações: "… pontos · primários … % · diagenéticos … % · poros … % ·
  total … %".
* **Zerar pontos** põe todas as contagens em zero e mantém as linhas.

Para contar sobre a imagem da lâmina, guardando a posição de cada ponto, use a aba **Contagem de pontos** (página
[Contagem de pontos](point_counting.md)).

### Editar a tabela

| Botão | Tecla | Faz |
|---|---|---|
| Atributos… | Enter | Edita a linha selecionada. F2 edita uma célula só. |
| Excluir | Del | Exclui as linhas selecionadas. |
| Copiar, Colar | Ctrl+C, Ctrl+V | Copia linhas, também para outra descrição. |
| Subir, Descer | Ctrl+↑, Ctrl+↓ | Move as linhas selecionadas. |
| Agrupar, Desagrupar | Ctrl+G, Ctrl+U | Reúne linhas sob um grupo com nome, ou desfaz; **Visão agrupada** mostra os grupos. |
| Cor das linhas selecionadas… | | Uma cor para as linhas (usada também na contagem de pontos e nos relatórios). |
| Desfazer, Refazer | Ctrl+Z, Ctrl+Y | Toda mudança da tabela. |
| Modelo… | | Carrega a composição de um modelo: substituir as linhas, ou acrescentar as que faltam. |
| Preferências… | | **Duplos cliques por ponto** e **Lembrar de salvar a cada** N pontos. |

**Salvar** (Ctrl+S) ao terminar; o lembrete aparece depois do número de pontos definido nas preferências.

## Opções

| Opção | O que muda |
|---|---|
| Duplos cliques por ponto | Quantos duplos cliques fazem um ponto (pelo menos 1). |
| Lembrar de salvar a cada | Um lembrete na barra de status depois de N pontos (0 = nunca). |
| Visão agrupada | Linhas sob os seus grupos, ou como uma lista só. |

## Como funciona

* As linhas com % manual ou quantidade nominal mantêm esse valor ("linhas fixas"); as linhas contadas dividem o que
  sobra, 100 − fixas, na proporção dos seus pontos. Sem nenhum ponto contado, as porcentagens são só os valores
  fixos. Uma linha com pontos e uma % conta pelos pontos (com um aviso).
* Os degraus nominais seguem os gráficos de comparação de Terry & Chilingar (1955); um traço conta como 0 %.
* Os atributos que um constituinte pode receber vêm da base de conhecimento ("Aplica-se a"), e por isso um hábito
  nunca é dado a um grão primário.

## Por script

```python
d = prj["TS-9"]
d.add_line("quartz_mono", points=112, location="framework")
d.add_line("calcite_dia", points=24, habit="poikilotopic", location="ig_pore_filling")
d.add_line("kaolinite", nominal="3", habit="booklet", location="intragranular_replacive",
           relation="replaces", related="k_feldspar")
for line in d.lines():
    print(line["constituent"], round(line["share"], 2))      # quartz_mono 79.88, calcite_dia 17.12, kaolinite 3.0
d.save()
```

## Limites e problemas comuns

* "… não se aplica a …": um atributo que o tipo do constituinte não admite.
* "… aparece duas vezes com os mesmos atributos (veja a linha …)": junte as duas linhas.
* "As porcentagens manuais e nominais somam … %, mais de 100 %."
* "…: sem localização." — um aviso para constituintes diagenéticos.
* "Foi dada a localização do constituinte relacionado sem o constituinte."

## Cobertura

P18 (tabela de composição), P19 (atributos), P20 (pontos, % manual, quantidade nominal, observação), P21 (grupos e
cores), P22 (copiar, colar, mover, desfazer), P23 (teclas), P24 (zerar pontos, modelo, preferências, lembrete de
salvar).

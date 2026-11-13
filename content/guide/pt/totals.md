# Totais

## Para que serve

Um **total** soma as linhas da composição de um tipo: todo o quartzo, os feldspatos, o cimento intergranular, a
porosidade de dissolução, os bioclastos… O RockFace tem 50 totais embutidos e as medidas de compactação IGV, COPL,
CEPL e ICOMPACT, calculados sobre a composição atual e sobre a **original** (antes da diagênese). Um projeto pode
acrescentar os seus próprios totais. As classificações, figuras, consultas e curvas LAS os usam.

## Antes de começar

Uma descrição com a sua composição (página [Composição](composition.md)).

## Passo a passo

### Ler os totais

1. Abra a aba **Classificação**. A tabela **Totais** fica à esquerda.
2. Cada linha dá um total em % do volume da rocha, em duas colunas:
   * **Atual** — da composição como descrita;
   * **Original** — da composição antes da diagênese: a fração de cada linha de substituição ou de dissolução volta
     ao constituinte que ela substituiu ou dissolveu.
3. Os totais são gravados automaticamente com a descrição: não há botão a apertar.

### Um total personalizado

1. **Totais personalizados…** abre **Totais personalizados do projeto**.
2. **Nova** e dê ao total um **Código** e um nome.
3. Acrescente **Condições**: uma linha é escolhida quando corresponde a todas as colunas de uma condição — tipo,
   grupo, constituinte, localização, hábito, modificador, relação. Clique duas vezes numa célula para escolher
   códigos: marcado significa *incluir*, parcialmente marcado significa *excluir*; uma célula vazia (*qualquer*)
   aceita tudo. **Adicionar condição**, **Remover condição**.
4. **Nesta descrição: … %** mostra o resultado na hora.
5. **OK**. O total aparece, marcado *personalizado*, em todas as descrições do projeto.

## Opções

Os totais embutidos incluem:

| Grupo | Totais |
|---|---|
| Rocha toda | volume, primários, diagenéticos, porosidade, grãos do arcabouço |
| Origem | extrabaciais, intrabaciais, intrabaciais não carbonáticos (Zuffa 1980) |
| Proveniência | Qm, Qp, chert, quartzo, Qt, feldspatos, feldspatos potássicos, plagioclásio, fragmentos de rocha por tipo, L, Lt (Dickinson 1985) |
| Outros | micas, minerais pesados, matriz, matriz deposicional |
| Carbonatos | grãos não esqueletais, bioclastos, constituintes do pré-sal, aloquímicos, lama carbonática, dolomita, carbonatos, evaporitos |
| Diagênese | cimentos (todos, intergranular, silicoso, carbonático, argiloso, de sulfatos), feldspato diagenético, substitutivos, deslocantes |
| Poros | intergranular, intragranular e móldica, de dissolução, de fratura, microporosidade |
| Compactação | IGV, COPL, CEPL, ICOMPACT |

## Como funciona

* Um total soma as porcentagens das linhas escolhidas por qualquer das suas condições.
* IGV = porosidade intergranular + cimento intergranular + matriz deposicional (Paxton et al. 2002).
* COPL = Pi − ((100 − Pi) × IGV) / (100 − IGV) e CEPL = (Pi − COPL) × C / IGV, com Pi = 40 % (Lundegard 1992);
  ICOMPACT = COPL / (COPL + CEPL) (Ehrenberg 1995).
* A lista de todos os totais, com as suas condições e fontes, está em `docs/NOMENCLATURE.md` do código-fonte.

## Por script

```python
d = prj["TS-9"]
t = d.totals()                       # todos os totais em % da rocha
print(t["qt"], t["intergranular_cement"], t["igv"], d.totals(original=True)["feldspar"])
prj.add_total("kaolinite_all", "Caulinita (toda)", rf.Selector(constituents=["kaolinite"]))
rows = prj.table(totals=["volume", "igv", "kaolinite_all"])
prj.to_csv("totais.csv", rows)
```

## Limites e problemas comuns

* Um total personalizado com um código já usado é recusado.
* IGV, COPL e CEPL foram definidos para arenitos; o RockFace os calcula para qualquer rocha, então leia-os com
  cuidado em carbonatos.
* A composição original só é tão boa quanto as relações paragenéticas dadas na composição (substitui, dissolução
  de…).

## Cobertura

P26 (tabela de totais, totais personalizados, gravados automaticamente), P27 (mais de 30 totais automáticos), P28
(editor de totais personalizados).

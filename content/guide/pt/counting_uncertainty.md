# Quão segura é a contagem de pontos

## Para que serve

Uma contagem de 300 pontos não dá a composição, ela a estima: contada de novo, a mesma lâmina daria porcentagens um
pouco diferentes, e uma rocha perto de um limite de classificação poderia cair no campo vizinho. O RockFace mostra
essa **incerteza da contagem** onde os números são usados:

* o **intervalo de 95 %** de cada linha contada da composição;
* a **probabilidade** do campo de cada classificação ternária (Folk, McBride, Dickinson);
* a **região de confiança** do ponto no diagrama ternário;
* durante a contagem, se a classificação já está **estável** ou **quantos pontos a mais** ela precisa.

## Antes de começar

* Uma descrição com **pontos contados** (Petro → Contagem de pontos, ou pontos digitados na aba Composição). Linhas
  com % manual ou quantidade nominal não têm incerteza da contagem e entram como estão.
* Para as probabilidades: um arenito (ou qualquer rocha) que uma classificação ternária situe.

## Passo a passo

1. **Petro → Composição.** A coluna **Intervalo 95 %** dá, para cada linha contada, a faixa de porcentagens da rocha
   que a contagem sustenta; a dica (tooltip) diz como foi calculada.
2. **Petro → Contagem de pontos.** Abaixo dos pontos contados, uma linha como *Folk (1980): Subarcósio 97 % —
   estável* ou *… 81 % — cerca de 240 pontos a mais para 95 %* diz se já dá para parar de contar. *Perto de um
   limite* quer dizer que mais pontos não vão decidir o campo: a rocha está mesmo entre dois campos.
3. **Petro → Classificação.** A coluna **Probabilidade** dá a probabilidade do campo mostrado; selecione uma
   classificação ternária para ler a probabilidade de cada campo, e se ela está estável ou quantos pontos faltam.
4. **Diagrama…** desenha a **região de confiança**: a área sombreada onde o ponto pode estar com 95 % de confiança
   (uma faixa ao longo de um lado quando um polo está vazio). **Região de confiança** a desliga.
5. Os **relatórios** trazem as probabilidades abaixo das classificações e desenham as regiões nos diagramas; a opção
   **Incerteza da contagem das classificações** do diálogo de relatório as deixa de fora.

## Opções

| Item | Valor |
|---|---|
| Confiança dos intervalos e da região | 95 % |
| Uma classificação é *estável* quando | o campo mais provável tem pelo menos 95 % |
| Pontos necessários | contados de novo com as mesmas proporções, até 5.000 pontos a mais |
| Sorteios das probabilidades | 4.000 (a mesma contagem dá sempre os mesmos números) |

Por script, a confiança, o nível de estabilidade e o número de sorteios podem ser trocados.

## Como funciona

* **Intervalos.** Uma linha contada é uma proporção dos pontos contados; o intervalo é o intervalo score de Wilson
  (1927), que fica entre 0 e 100 % e mantém a cobertura de 95 % para constituintes raros, ao contrário do ± 2σ do
  ábaco clássico de Van der Plas & Tobi (1965) (Agresti & Coull 1998; Howarth 1998; Weltje 2002). O intervalo é
  escalado para a parte da rocha que as linhas contadas ocupam.
* **Probabilidades.** As contagens são uma amostra multinomial da rocha (Chayes 1956). Dadas as contagens, as
  proporções verdadeiras seguem uma distribuição de Dirichlet (priori de Jeffreys, contagens + ½; Vermeesch 2005).
  O RockFace sorteia 4.000 composições dela, calcula os totais e o ponto de cada classificação exatamente como para a
  descrição e conta em que campo cada ponto cai.
* **Região.** Os pontos sorteados, em razões logarítmicas aditivas (Aitchison 1982; Weltje 2002), dão uma região
  normal bivariada de 95 %, desenhada de volta no triângulo — uma elipse nas razões logarítmicas, curva perto dos
  vértices. Quando um polo está vazio em todos os sorteios, a região é o intervalo ao longo do lado.
* **Pontos necessários.** As mesmas proporções contadas com mais pontos (de 1,25 a 30 vezes) até o campo mais
  provável chegar a 95 %.

## Por script

```python
d = prj["ILL-TS-001"]
u = d.uncertainty()                          # confidence=0.95, stable=0.95, draws=4000
u["schemes"]["folk1980"]["probabilities"]    # {'subarkose': 0.97, 'arkose': 0.02, …}
u["schemes"]["folk1980"]["needed"]           # 0: já estável; None: perto de um limite
u["lines"][0]                                # {'constituent': 'quartz_mono', 'share': 48.1, 'low': 42.5, 'high': 53.8, …}
rf.wilson_interval(21, 295)                  # (4.7, 10.6) em % dos pontos contados
rf.ternary_figure("folk.png", "folk1980", prj.descriptions(), regions=True)
```

A Mio também responde: *"a classificação da ILL-TS-001 é confiável?"*, *"quantos pontos faltam na ILL-TS-002?"*,
*"how sure is the classification of ILL-TS-002?"*.

## Limites e problemas comuns

* **Só a incerteza da contagem.** O erro de amostragem entre lâminas da mesma rocha (Bayly 1965), os erros de
  identificação do petrógrafo e a incerteza das quantidades manuais e nominais não entram.
* O modelo supõe pontos mais afastados que o maior grão (Van der Plas & Tobi 1965); uma grade mais fina que os grãos
  conta o mesmo grão duas vezes e faz os intervalos parecerem mais estreitos do que são.
* A composição original (antes da diagênese) ainda não tem probabilidades.
* Uma rocha carbonática ganha os intervalos das linhas; as classificações por regras (Dunham, Embry & Klovan…) não
  têm probabilidades.

## Cobertura

O8 (pedido do dono de 17/11/2026: as inovações, a primeira).

Referências: Chayes (1956); Van der Plas & Tobi (1965), https://doi.org/10.2475/ajs.263.1.87; Bayly (1965); Wilson
(1927); Agresti & Coull (1998); Howarth (1998), https://doi.org/10.2475/ajs.298.7.594; Aitchison (1982); Weltje
(2002), https://doi.org/10.1016/S0012-8252(01)00076-9; Vermeesch (2005), https://doi.org/10.1029/2004JB003479;
Vermeesch (2018), https://doi.org/10.1016/j.epsl.2018.08.019.

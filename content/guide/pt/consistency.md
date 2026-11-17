# Consistência entre escalas

## Para que serve

A mesma amostra é medida em várias escalas: a lâmina no microscópio, o plugue no laboratório, o volume de micro-CT,
o perfil do poço na sua profundidade. Cada um vê a rocha de um jeito, e todos deveriam contar uma história coerente
— junto com a sequência paragenética que o petrógrafo escreveu. A aba **Consistência** compara essas medidas e diz,
para cada verificação, se os números concordam, se diferem do jeito que a descrição explica ou se se contradizem — e
o que conferir.

## Antes de começar

As verificações usam o que o projeto já tem; cada uma só roda com os seus dados:

* a **composição** (porosidade, IGV, cimentos, argilas) — Petro → Composição;
* a **porosidade e a permeabilidade do plugue** — Petro → Análises, *Petrofísica convencional*;
* um **volume de micro-CT segmentado** da amostra com a porosidade, ou um mapa de microporosidade — RockFace MC;
* uma **curva de porosidade** (PHIT, PHIE, NPHI, DPHI…) do poço da amostra cobrindo a sua profundidade — RockFace MC
  → perfis;
* a **granulometria e a seleção** — Petro → Microscópica (ou Macroscópica);
* a **sequência paragenética** com os regimes — Petro → Diagênese.

## Passo a passo

1. Abra uma descrição e a aba **Consistência** (a última).
2. Leia a tabela: cada verificação, o resultado e a explicação. Passe o mouse sobre a explicação para ver as
   referências.
   * **Consistente** — os números concordam;
   * **Explicado** — diferem do jeito que a descrição diz que deveriam (o plugue vê a microporosidade das argilas
     descritas, por exemplo);
   * **A conferir** — uma diferença que nada na descrição explica;
   * **Inconsistente** — os dados se contradizem;
   * **Sem dados** — o que falta para rodar a verificação.
3. **Verificar de novo** depois de editar a descrição (a aba acompanha a composição e a descrição microscópica que
   estão na tela).
4. **Perguntar à Mio** envia *"A amostra … é consistente?"* para a Mio; ela também responde *"quais amostras têm
   inconsistências?"* para o projeto inteiro.
5. Os **relatórios** têm a seção *Consistência*, com as verificações que têm dados e as referências.

## As verificações

| Verificação | O que compara | Resultado |
|---|---|---|
| Porosidade: lâmina × plugue | A porosidade da contagem (com a incerteza da contagem) e a do plugue | Lâmina acima do plugue além da incerteza: *inconsistente* (poros criados na preparação, outra lâmina, plugue e lâmina de lugares diferentes). Plugue mais de 5 pontos acima: *explicado* quando há argilas, matriz, micrita ou microporosidade descritas, *a conferir* se não (Halley 1978) |
| Porosidade: micro-CT | A porosidade resolvida de um volume segmentado (ou o total de um mapa de microporosidade) e o plugue — a lâmina quando não há plugue | Mais de 3 pontos acima: *inconsistente* (limiar da segmentação); mais de 5 abaixo: *explicado* (poros menores que o voxel; Andrä et al. 2013) |
| Porosidade: perfil de poço | A curva de porosidade na profundidade da amostra e o plugue (ou a lâmina) | Mais de 5 pontos de diferença: *a conferir* (deslocamento de profundidade, camadas finas, correções do perfil) |
| Volume intergranular (IGV) | O IGV de um arenito | Acima de 45 %: *inconsistente* — mais que a areia recém-depositada (Beard & Weyl 1973; Lundegard 1992). Abaixo de 26 %: *explicado* por 10 % ou mais de grãos dúcteis ou por contatos côncavo-convexos ou suturados, *a conferir* se não (Paxton et al. 2002; Pittman & Larese 1991) |
| Cimento precoce × compactação | Cimento eodiagenético e IGV | 10 % ou mais de cimento precoce com IGV abaixo de 28 %: *inconsistente*; IGV de 35 % ou mais sem cimento precoce nem matriz: *a conferir* |
| Sequência paragenética | Relações e regimes das fases | Relações contraditórias, ou um regime posterior antes de um anterior: *inconsistente* |
| Permeabilidade × textura | A permeabilidade do plugue e a estimativa de Berg (1970) pela porosidade, granulometria mediana e seleção | Dentro de um fator 10: *consistente*; 10 vezes menor: *explicado* por argilas, cimentos ou microporosidade, *a conferir* se não; 10 vezes maior: *explicado* por fraturas, *a conferir* se não |

## Como funciona

* A porosidade da lâmina carrega a incerteza da contagem dos pontos contados (veja *Quão segura é a contagem de
  pontos*): uma diferença dentro dela nunca é chamada de inconsistente.
* Estimativa de Berg (1970): k (mD) = 1000 × 5,1×10⁻⁶ φ^5,1 d² e^(−1,385 p), com φ em %, d a granulometria mediana em
  mm e p = P90 − P10 = 2,563 σ (seleção de Folk & Ward, em unidades φ). Quando a seleção não foi descrita, supõe-se
  uma areia moderadamente selecionada (σ = 0,85), e isso é dito.
* Uma rocha é tratada como carbonática quando os grãos carbonáticos e a lama carbonática superam os grãos
  extrabacinais: as verificações de IGV não se aplicam.
* O valor do perfil é a amostra da curva mais próxima da profundidade corrigida (ou do topo); uma curva em v/v é lida
  em %.

## Por script

```python
rep = prj["ILL-TS-001"].consistency()
rep["status"]                                   # "ok", "explained", "check", "inconsistent" ou "no_data"
[(c["code"], c["status"]) for c in rep["checks"]]
for r in prj.consistency():                     # todas as descrições, primeiro as que pedem atenção
    print(r["name"], r["status"])
rf.berg_permeability(19.4, 0.18, 0.42)          # 138 mD
```

## Limites e problemas comuns

* Os limiares são regras práticas da literatura, não leis: um *a conferir* é uma pergunta ao petrógrafo, não um
  erro.
* A equação de Berg foi deduzida para areias limpas com 30 a 40 % de porosidade; para arenitos cimentados leia-a como
  ordem de grandeza — por isso o fator 10.
* A DRX de rocha total não é comparada com a contagem (porcentagens em peso e em volume, e as fases finas que o
  microscópio não resolve, diferem demais para uma regra simples).
* Os limites do IGV são para arenitos de grãos rígidos; rochas muito grossas, muito mal selecionadas ou ricas em
  matriz começam de uma porosidade deposicional menor.

## Cobertura

O8 (pedido do dono de 17/11/2026: as inovações, a segunda).

Referências: Halley (1978), https://doi.org/10.1306/212F7504-2B24-11D7-8648000102C1865D; Andrä et al. (2013),
https://doi.org/10.1016/j.cageo.2012.09.005; Beard & Weyl (1973); Lundegard (1992),
https://doi.org/10.1306/D42678D4-2B26-11D7-8648000102C1865D; Paxton et al. (2002); Pittman & Larese (1991),
https://doi.org/10.1306/0C9B292F-1710-11D7-8645000102C1865D; Berg (1970); Nelson (1994).

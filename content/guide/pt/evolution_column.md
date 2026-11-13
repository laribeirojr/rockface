# Evolução paragenética e a coluna estratigráfica

## Para que serve

A **evolução paragenética** põe num só quadro as fases diagenéticas de várias amostras — uma formação, um campo, uma
consulta: os eventos em ordem, o seu regime (eo-, meso-, telodiagênese), a fonte da água de cada um, a quantidade média
e o número de amostras, as idades U-Pb e fotos das fases. A **coluna estratigráfica** posiciona as formações com as
suas idades deposicionais e as idades U-Pb das amostras, para mostrar que cada cimento é mais novo que a rocha que o
contém.

## Antes de começar

* Descrições com a sua composição e relações paragenéticas (página [Diagênese: ambientes, sequência paragenética e grafo de conhecimento](diagenesis.md)).
* Para as idades: fases datadas (página [Datação U-Pb no diagrama de Tera-Wasserburg](dating.md)).
* Para a coluna: as formações com as suas idades deposicionais (abaixo).

## Passo a passo

### A evolução

1. No RockFace Explorer, abra a aba **Evolução** e depois **Evolução paragenética**.
2. As descrições são as da consulta da aba Consulta (**Só as descrições da consulta**), ou todas.
3. A tabela lista os **Eventos (fases)** em ordem, com o seu **Regime**, **Fonte da água**, **% média (n)** e **Idade
   U-Pb**. "N amostras, P fases, C relações em contradição entre amostras."
4. Mude o **Regime** ou a **Fonte da água** de uma fase na sua célula (Marinha, Meteórica, Evaporítica, Lago alcalino, Água
   de poro rasa, De bacia (soterramento), Hidrotermal, Não interpretada): a sua escolha fica no projeto.
5. **Fotos das fases** acrescenta fotos de cada fase ao quadro: as fotos dos seus pontos datados, depois as imagens
   Atlas anotadas com o seu constituinte.
6. **Quadro de evolução…** grava o quadro (PNG, SVG, PDF); **Eventos (CSV)…**, a tabela.

### A coluna estratigráfica

1. Abra **Idades na estratigrafia**.
2. Em **Formações, do topo à base (idades deposicionais, Ma)**, **Adicionar formação** e dê o nome da **Formação**, o
   **Topo (Ma)**, a **Base (Ma)** e a **Cor**. **Salvar formações**.
3. A coluna mostra cada formação com o seu intervalo de idade e, ao lado, as idades U-Pb salvas para as suas amostras.
4. **Coluna estratigráfica…** a grava.

## Opções

| Opção | O que muda |
|---|---|
| Só as descrições da consulta | A evolução das amostras encontradas, ou de todas. |
| Regime, Fonte da água | Definidos à mão para uma fase (limpos com um valor vazio). |
| Fotos das fases | Fotos no quadro. |

## Como funciona

Cada fase é um constituinte com o seu hábito e o seu tipo (precipitação ou dissolução), reunido entre as amostras. Os
eventos são ordenados pelo regime, depois pelas relações paragenéticas de todas as amostras juntas, depois pelo seu
lugar na sequência de cada amostra; as relações que se contradizem entre amostras são contadas e ficam de fora. O
regime vem das regras diagenéticas (uma fase sem regime recebe o das fases anteriores), a fonte da água dos ambientes
interpretados, a menos que sejam definidos à mão. As idades são postas na fase que datam (mineral e hábito da idade
salva).

## Por script

```python
evo = prj.evolution(formation="Example Formation", path="evolucao.png")
for ph in evo.phases:
    print(ph.event, ph.label, ph.regime, ph.water, ph.share_mean, ph.ages)
prj.set_phase(evo.phases[-1].key, water="hydrothermal")
prj.stratigraphy = [{"name": "Example Formation", "top": 100.0, "base": 108.0, "colour": "#E9D7A5"}]
prj.strat_column("coluna.pdf")
```

## Limites e problemas comuns

* Uma fase sem relações paragenéticas em nenhuma amostra é posicionada só pelo seu regime e pelo seu lugar na
  sequência de cada amostra.
* A coluna precisa das idades deposicionais das formações (base mais antiga que o topo).

## Cobertura

L8 (sequência paragenética de várias amostras), L12 (idades na estratigrafia; evolução paragenética de várias amostras
com quantificação e fotos).

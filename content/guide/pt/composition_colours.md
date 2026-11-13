# Cor das linhas selecionadas (composição)

## Para que serve

O Counterledge deixa o petrógrafo colorir linhas da tabela de composição para achá-las rápido durante a contagem.
No RockFace, as linhas selecionadas recebem uma cor pelo seu grupo.

## Passo a passo

1. **Petro → Composição**: selecione uma ou mais linhas.
2. **Cor das linhas selecionadas…** e escolha a cor.

## Como funciona

As linhas passam a compartilhar um grupo (o que já compartilham, ou um novo) e a cor do grupo as pinta; desagrupar a
remove. A cor é salva com a composição.

## Por script

```python
d = prj["ILL-TS-001"]; d.composition.groups   # {"g1": {"name": …, "colour": "#123456"}}
```

## Cobertura

Counterledge C2 (Configure Selected Row Color).

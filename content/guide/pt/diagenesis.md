# Diagênese: ambientes, sequência paragenética e grafo de conhecimento

## Para que serve

A aba **Diagênese** interpreta os ambientes diagenéticos pelos quais a rocha passou — marinho, meteórico, árido,
lacustre alcalino, soterramento, fluidos quentes, soerguimento — a partir das feições da sua descrição, cada conclusão
com as regras e fontes que a sustentam. Ela monta também a **sequência paragenética**: as fases diagenéticas na ordem
em que se formaram, com o seu regime (eo-, meso- ou telodiagênese). O petrógrafo confirma ou rejeita cada ambiente e
pode reordenar a sequência à mão.

## Antes de começar

Uma descrição cuja composição tenha constituintes diagenéticos, de preferência com os seus hábitos, localizações e
relações paragenéticas (cobre, substitui, posterior a…) (página [Composição](composition.md)).

## Passo a passo

### Os ambientes

1. Abra a aba **Diagênese**.
2. **Ambientes diagenéticos** lista cada **Ambiente** com o seu **Regime** e o **Resultado**:
   * *Interpretado* — foram achadas uma regra indicativa ou duas regras de apoio diferentes;
   * *Alguma evidência* — uma regra de apoio;
   * vazio — "Nenhuma evidência deste ambiente na descrição."
3. Selecione um ambiente para ver as regras **Encontrado**: a feição da descrição, a regra e a sua fonte.
4. Em **Petrógrafo**, **confirme** ou **rejeite**; a sua decisão prevalece sobre o resultado automático. Escreva uma
   **Nota sobre este ambiente** se precisar.
5. **Interpretação diagenética — notas**: a interpretação geral nas suas palavras.

### A sequência paragenética

1. **Sequência paragenética** mostra as fases em ordem, cada uma com a sua **Etapa**, **Fase** (precipitação ou
   dissolução de um constituinte) e **Regime**, e o gráfico da sequência.
2. A ordem vem das relações paragenéticas da composição; o regime, das regras. As contradições são informadas:
   "Relações contraditórias entre … e …: ficam fora da ordem", "… vem antes de … mas pertence a um regime
   posterior".
3. **Subir** e **Descer** movem uma fase; o regime pode ser mudado na sua célula. **Automático** traz de volta a
   ordem calculada pelo RockFace.
4. **Exportar imagem…** grava o gráfico.
5. **Salvar** (Ctrl+S): a interpretação faz parte da descrição.

### O grafo de conhecimento

1. **Grafo de conhecimento…** (na aba, ou em Ferramentas → Base de conhecimento → **Grafo de conhecimento**).
2. O grafo liga as feições de uma descrição → as regras → os ambientes → os regimes. Linhas contínuas são regras
   indicativas, tracejadas são regras de apoio; as regras encontradas na descrição aberta ficam em azul.
3. Em **Ambiente**, escolha um para ver só a sua parte do grafo, ou **(todos os ambientes)**. **Exportar imagem…**
   o grava.

## Opções

| Campo | O que muda |
|---|---|
| Petrógrafo | Confirmado ou rejeitado: substitui o resultado automático em relatórios, consultas e figuras. |
| Subir, Descer, célula do regime | A sequência definida à mão (guardada com a descrição). |
| Automático | Volta à ordem e aos regimes encontrados pelo RockFace. |

## Como funciona

* As regras são do próprio RockFace, cada uma tirada da literatura publicada: Morad et al. (2000, 2010), Worden &
  Burley (2003), Longman (1980), Flügel (2010), Scholle & Ulmer-Scholle (2003), Radke & Mathis (1980), Tosca & Wright
  (2018), Paxton et al. (2002), Schmidt & McDonald (1979), Taylor (1950), Park & Schot (1968).
* Um ambiente é *interpretado* com uma regra indicativa ou duas regras de apoio diferentes, e tem *alguma evidência*
  com uma regra de apoio. Essa agregação é declarada no programa e em `docs/NOMENCLATURE.md`; a decisão do petrógrafo
  sempre prevalece.
* A ordem das fases é uma ordenação topológica das relações; as relações que se contradizem ficam de fora e são
  informadas.
* O RockFace Explorer desenha a evolução paragenética de várias amostras juntas (página [Evolução paragenética e a coluna estratigráfica](evolution_column.md)).

## Por script

```python
d = prj["TS-9"]
for code, r in d.interpret().items():
    print(code, r["status"], r["regime"], r["rules"])          # p. ex. meso_burial interpreted meso ['albitization']
d.diagenesis.decisions["eo_marine"] = "confirmed"
d.save()
for step in d.paragenesis():
    print(step["step"], step["phase"], step["kind"], step["regime"])
rf.paragenesis_figure("sequencia.png", d)
rf.knowledge_graph("grafo.svg", environment="meso_burial")      # também .png, ou .dot para o grafo inteiro
```

## Limites e problemas comuns

* "Nenhuma fase diagenética na composição." — acrescente primeiro constituintes diagenéticos.
* Sem relações paragenéticas as fases não têm ordem: dê as relações na composição (cobre, substitui, posterior a,
  preenche dissolução de…).
* O arquivo DOT do grafo de conhecimento (para o Graphviz) é gravado só para o grafo inteiro.

## Cobertura

P33 (interpretação dos ambientes diagenéticos), P40 (grafo de conhecimento), L8 (gerador da sequência paragenética).

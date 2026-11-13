# Identificação de uma amostra

## Para que serve

A aba **Identificação** diz do que trata a descrição: o seu nome e usos, o poço ou afloramento, a amostra e as suas
profundidades, a lâmina, o petrógrafo e as observações importantes. Todas as consultas, relatórios, figuras e
arquivos LAS leem estes campos.

## Antes de começar

Uma descrição aberta ou recém-criada (página [Projetos e descrições](projects_descriptions.md)).

## Passo a passo

1. Abra a aba **Identificação** (a primeira).
2. **Descrição**
   * **Nome da descrição** — obrigatório e único no projeto. Depois do primeiro salvamento fica travado (use
     **Salvar como…** para outro nome).
   * **Uso selecionado da descrição** — até três usos (caracterização de reservatório, qualidade de reservatório,
     diagênese, proveniência, ambiente deposicional, calibração petrofísica, geoquímica e datação, ensino, outro),
     sem repetir.
3. **Poço ou afloramento**
   * **Nome** — digite um novo ou escolha um que já está no projeto; escolher um poço existente preenche a sua bacia,
     campo, país, estado e posição.
   * **Tipo** (poço ou afloramento), **Bacia**, **Campo**, **País**, **Estado**, **Latitude (°)**, **Longitude (°)**.
4. **Amostra**
   * **Tipo de amostra** (plugue de testemunho, testemunho inteiro, amostra lateral, amostra de calha, amostra de
     afloramento, outro), **Unidade estratigráfica**, **Zona**.
   * **Profundidade de topo (m)** e **Profundidade de base (m)**; **Profundidade corrigida (m)** (correção
     testemunho–perfil) e **Profundidade ajustada (m)** (a profundidade final usada nos modelos).
   * **Testemunho n.º**, **Caixa n.º**, **Plugue n.º**, **Lâmina n.º** e **Fácies** (o código ou nome da equipe).
5. **Petrógrafo** — **Nome** e **Instituição**. **Primeira edição** e **Última edição** são preenchidas pelo RockFace.
6. **Observações importantes** — um resumo livre do que mais importa na amostra.
7. **Salvar** (Ctrl+S).

## Opções

| Campo | Regra |
|---|---|
| Nome da descrição | Obrigatório; único; travado depois do primeiro salvamento. |
| Uso selecionado | No máximo três, sem repetir. |
| Profundidades | 0 a 9999,99 m; a base não pode ser mais rasa que o topo. |
| Latitude, longitude | −90° a 90°; −180° a 180°. |
| Fácies | Texto livre: o código ou nome que a equipe usa (o painel do Explorer agrupa por ele). |

## Como funciona

Poços, amostras e lâminas são registros compartilhados: duas descrições da mesma lâmina mostram o mesmo poço,
profundidades e números, e mudá-los numa muda para as duas. Os valores guardados são códigos neutros quanto ao idioma
(por exemplo o tipo de amostra), e por isso o projeto se lê igual em inglês, espanhol e português. O levantamento
direcional do poço, quando existe, dá a profundidade vertical verdadeira e a posição de cada amostra (página
[Trajetória do poço](well_trajectory.md)).

## Por script

```python
with rf.open("estudo.rockface") as prj:
    d = prj["TS-9"]
    print(d.identification.well_name, d.identification.top_depth)
    d.update(base_depth=2501.6, facies="F3", uses=["reservoir", "diagenesis"])   # conferido como no formulário e salvo
```

`d.update()` levanta `rf.ScriptError` com as mensagens quando um valor quebra uma regra, e nada é gravado.

## Limites e problemas comuns

* "O nome da descrição é obrigatório." / "Já existe uma descrição chamada … neste projeto."
* "Profundidade de topo (m) deve estar entre 0 e 9999,99 m."
* "A profundidade de base (… m) é menor que a de topo (… m)."
* "No máximo três usos podem ser selecionados." / "Um uso da descrição foi selecionado duas vezes."
* Avisos (não erros): "Nenhum poço ou afloramento informado.", "A lâmina não tem número." A descrição é salva, mas
  as consultas por poço ou por lâmina não a encontrarão.

## Cobertura

P4 (campos da identificação), P5 (usos selecionados), P7 (observações importantes), P8 (posição e profundidades).

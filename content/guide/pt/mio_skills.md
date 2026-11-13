# Skills da Mio

## Para que serve

Uma **skill** é uma pequena receita que a Mio executa sempre que uma pergunta a pede: várias ferramentas dela, uma
após a outra, com os valores tirados da pergunta. "Resumo do poço ILLUSTRATIVE-B" conta as amostras do poço, lista
suas fácies, dá porosidade e permeabilidade e diz quais descrições não têm porosidade — numa só resposta. O RockFace
traz oito skills, ativas desde o início, para usar e copiar; você escreve as suas e as guarda para si ou no projeto,
para toda a equipe.

## Antes de começar

* Um projeto aberto. Escrever uma skill não exige programação: é um texto JSON curto editado na janela **Skills**.

## Passo a passo

### Usar uma skill

1. No painel da Mio digite uma das frases dela ("resumo do poço ILLUSTRATIVE-B", "lacunas", "melhores
   reservatórios", "como faço …") ou o nome após uma barra: `/well-summary ILLUSTRATIVE-B`.
2. Se a skill precisa de um valor que a pergunta não deu (o poço, uma amostra), a Mio pede.

As skills que vêm com o RockFace:

| Skill | Chamada por (exemplos) | O que faz |
|---|---|---|
| `well-summary` | resumo do poço · well summary · resumen del pozo | contagem, fácies, porosidade, permeabilidade, porosidade faltante de um poço |
| `formation-summary` | resumo da formação · formation summary | contagem, poços, fácies, porosidade, cimento de uma formação |
| `reservoir-quality` | melhores reservatórios · reservoir quality | amostras com porosidade ≥ 15 % e permeabilidade ≥ 100 mD, e seus poços |
| `cement-overview` | panorama dos cimentos · cimentação | cimento total e carbonático; amostras com calcita, dolomita, crescimentos de quartzo |
| `dated-samples` | amostras datadas · dated samples | amostras com pontos de datação e seus poços |
| `data-gaps` | lacunas · dados faltantes · controle de qualidade | descrições sem profundidade, porosidade ou permeabilidade |
| `sample-report` | ficha da amostra · sample report | os principais dados de uma descrição e as sugestões dos seus mapas |
| `how-to` | como faço · how do I · cómo hago | as páginas deste guia que explicam uma tarefa |

### Escrever uma skill

1. Painel da Mio → **Skills…**. A lista mostra todas as skills com a origem: *RockFace*, *minha* (sua pasta),
   *projeto*.
2. Selecione uma para vê-la, ou clique em **Nova** para um modelo.
3. Edite o JSON (campos abaixo) e clique em **Salvar para mim** (sua pasta) ou **Salvar no projeto** (todos que
   abrem o projeto). A skill é conferida antes de salvar; os problemas aparecem abaixo do editor.
4. **Ativa** desliga uma skill sem excluí-la. Uma skill salva com o nome de outra a substitui (uma skill do projeto
   chamada `how-to` substitui a do RockFace); **Excluir** traz a outra de volta.

## Opções

```json
{
 "name": "kaolinite-by-well",
 "title": {"en": "Kaolinite by well", "pt": "Caulinita por poço", "es": "Caolinita por pozo"},
 "description": {"en": "…", "pt": "Quantas amostras de um poço têm caulinita, e sua porosidade.", "es": "…"},
 "triggers": ["kaolinite by well", "caulinita por poço", "caolinita por pozo"],
 "inputs": {"well": {"field": "well"}},
 "steps": [
  {"tool": "count", "question": "samples of well {well} with kaolinite"},
  {"tool": "stats", "number": "petrophysics.porosity", "question": "samples of well {well} with kaolinite"}
 ],
 "active": true
}
```

| Campo | O que é |
|---|---|
| `name` | minúsculas, dígitos e hífens; também o `/nome` que chama a skill |
| `title`, `description` | mostrados na lista, em inglês, português e espanhol |
| `triggers` | frases que chamam a skill (acentos e maiúsculas não importam) |
| `inputs` | valores lidos da pergunta: `{"field": "well"}` (qualquer campo da identificação: poço, formação, fácies, campo, bacia, zona…) ou `{"field": "sample"}` (o nome de uma descrição); `{question}` está sempre disponível |
| `steps` | as ferramentas, em ordem: `search`, `count` (`question`), `stats` (`number`, `question`), `values` (`field`, `question`), `missing` (`number`, `question`), `describe` (`sample`), `suggest` (`sample`), `guide` (`question`) |

`number` é `conceito.atributo` como no Explorer: `petrophysics.porosity`, `petrophysics.permeability`,
`petrophysics.grain_density`, `identification.top_depth`, `totals.cement`, `totals.carbonate_cement`…

## Como funciona

Skills são dados, nunca código: uma skill só pode chamar as ferramentas da Mio, e toda ferramenta só lê o projeto.
As skills vêm de três lugares, lidos nesta ordem (uma posterior com o mesmo nome substitui a anterior): a pasta do
RockFace `rockface/mio_skills`, a sua pasta (`~/.rockface/mio/skills`, ou a configuração `mio.skills`, ou
`ROCKFACE_MIO_SKILLS`) e o projeto (guardada no projeto com uma linha de auditoria, então um projeto em servidor
compartilha suas skills com a equipe).

## Por script

```python
for s in prj.mio_skills():
    print(s.name, s.source, s.triggers)
prj.save_mio_skill({"name": "barite-count", "triggers": ["barita por favor"],
                    "steps": [{"tool": "count", "question": "samples with barite"}]})
print(prj.mio(lang="pt").ask("/barite-count").text)
prj.delete_mio_skill("barite-count")
```

## Limites e problemas comuns

* "A skill não pode ser usada: …": a conferência lista o que corrigir (uma ferramenta que não existe, uma entrada
  usada mas não declarada, um `stats` sem número).
* Uma frase que também é uma pergunta comum ("amostras com calcita") faz toda pergunta assim rodar a skill — escolha
  frases que digam o que a skill é.
* Skills que gravam no projeto (aplicar uma sugestão, rodar um script) não são permitidas nesta versão: a Mio propõe,
  o usuário decide.

## Cobertura

O assistente que chama as ferramentas do programa da etapa 0.27 do ROADMAP; o pedido do proprietário de 13/11/2026
(skills criadas pelo usuário, exemplos ativos desde o início).

# Nomenclatura, escalas e referências (a base de conhecimento)

## Para que serve

Todas as listas do RockFace — constituintes, hábitos, localizações, modificadores, relações paragenéticas,
estruturas, contatos, tipos de poro — vêm da sua **base de conhecimento**: 257 termos embutidos em inglês, espanhol e
português, cada um com a sua fonte publicada. O editor da base de conhecimento os mostra e permite que um projeto
acrescente os seus próprios termos, oculte os que não usa e ponha as listas na ordem que preferir. Mostra também as
**escalas** numéricas (granulometria, seleção, arredondamento, tamanho de cristal, tamanho de poro) e as
**referências** citadas.

## Antes de começar

* Um projeto aberto, para mudar algo. Sem projeto, a nomenclatura embutida é mostrada só para leitura.
* Num servidor, mudar a base de conhecimento exige o nível de gerente.

## Passo a passo

### Consultar um termo

1. **Ferramentas → Base de conhecimento → Nomenclatura** (Ctrl+K).
2. Escolha a **Categoria** (constituinte, grupo, hábito, localização, modificador, relação, estrutura, contato…).
3. Digite em **Filtrar (qualquer idioma)…**: "quartzo", "cuarzo" e "quartz" acham o mesmo termo; os acentos são
   ignorados.
4. Selecione um termo para ver o seu código, os rótulos nos três idiomas, o grupo, tipo, família de rocha, a que se
   aplica, e as suas **Fontes**.

### Acrescentar um termo do projeto

1. Escolha a categoria e clique em **Adicionar termo…**.
2. Preencha o **Código** (minúsculas, letras, dígitos e `_`; nunca muda depois), os rótulos em **Inglês**
   (obrigatório), **Espanhol** e **Português** (um aviso quando faltam) e, conforme a categoria, **Grupo** e **Família
   de rocha** (constituintes), **Tipo** (grupos), **Aplica-se a** (localizações e modificadores) e **Relação inversa**
   (relações).
3. Em **Fontes**, dê a referência completa da fonte (autor, ano, título, publicação). Todo termo embutido traz a sua
   fonte da literatura; um termo do projeto sem fonte é salvo com um aviso.
4. **Aplicar** e depois **Salvar no projeto**.

### Ocultar, ordenar, desfazer

* **Ocultar** tira um termo embutido das listas deste projeto (as descrições que o usam o mantêm). Marque **Mostrar
  termos ocultos** para vê-los, e **Mostrar** para trazer um de volta.
* **Subir** e **Descer** mudam a ordem em que os termos aparecem nas listas dos formulários.
* **Remover** exclui um termo do projeto (os termos embutidos só podem ser ocultados).
* **Desfazer** cancela a última mudança; **Restaurar padrão** traz de volta a ordem embutida e todos os termos
  ocultos (os termos do próprio projeto ficam).
* **Salvar no projeto** grava as mudanças, com uma linha na auditoria; **Fechar** pergunta antes se algo não foi
  salvo.

### Escalas

1. **Ferramentas → Base de conhecimento → Escalas**.
2. Escolha a **Escala**: granulometria (Udden–Wentworth, com o φ de Krumbein), seleção (σI de Folk & Ward),
   arredondamento (Powers), tamanho de cristal (Folk 1962) ou tamanho de poro. A tabela dá cada classe com **De**,
   **Até (exclusive)** e φ.
3. **Verificar um valor com uma classe**: digite um **Valor**, escolha uma **Classe**; o RockFace responde "Coerente"
   ou "Incoerente: … é …, não …". Os formulários da descrição usam a mesma verificação (página
   [Descrição macroscópica e microscópica](macro_micro_description.md)).

### Referências

**Ferramentas → Base de conhecimento → Referências** lista cada referência com a sua **Chave**, a **Referência**
completa e **Citada por** (quantos termos, regras, totais e classificações a citam).

## Opções

| Campo | O que é |
|---|---|
| Código | O valor guardado no projeto; nunca traduzido, nunca mudado. |
| Grupo, Tipo | Onde o termo entra nas listas da composição (por exemplo, carbonato diagenético). |
| Família de rocha | Siliciclástica, carbonática ou ambas: as listas de uma descrição mostram a família que se aplica. |
| Aplica-se a | Para localizações e modificadores: os tipos de constituinte que podem descrever. |
| Relação inversa | Para relações paragenéticas: a relação lida no outro sentido (por exemplo *substitui* ↔ *substituído por*). |

## Como funciona

A nomenclatura embutida é do próprio RockFace, construída a partir da literatura publicada; nada dela vem da
ontologia de um programa comercial. O projeto guarda só as suas diferenças — os seus termos, os termos ocultos e a
ordem —, e por isso um RockFace mais novo, com mais termos embutidos, ainda o abre. A lista completa, com as fontes,
está em `docs/NOMENCLATURE.md` do código-fonte.

## Por script

```python
with rf.open("estudo.rockface") as prj:
    for t in prj.search("caulinita"):                 # qualquer idioma, acentos ignorados
        print(t.category, t.code, t.labels["pt"], t.citations())
    print(prj.term("constituent", "kaolinite").labels)
from rockface.core import scales
print(scales.classify("grain_size", 0.3))            # 'medium_sand'
```

## Limites e problemas comuns

* "Abra um projeto para adicionar, ocultar ou reordenar termos; a nomenclatura embutida é mostrada."
* Um código já usado, ou com maiúsculas ou espaços, é recusado; também um constituinte sem o seu grupo e família de
  rocha.
* Ocultar um termo não muda as descrições que já o usam.

## Cobertura

P39 (ferramentas da base de conhecimento: editores de atributos com e sem intervalos de coerência, ordem dos itens,
adicionar, atualizar, remover, desfazer).

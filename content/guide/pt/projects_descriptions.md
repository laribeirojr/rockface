# Projetos e descrições

## Para que serve

Um **projeto** guarda uma coleção: os seus poços e afloramentos, amostras, lâminas, descrições, imagens, análises,
volumes e perfis. Uma **descrição** é o registro do petrógrafo sobre uma lâmina. Esta página trata de criar e abrir
projetos, e de criar, carregar, salvar, copiar, excluir e usar descrições como modelos.

## Antes de começar

O RockFace Petro aberto (página [Primeiros passos](getting_started.md)).

## Passo a passo

### Um projeto

1. **Início → Projeto → Novo projeto** (Ctrl+Shift+N): escolha uma pasta e um nome. O arquivo termina em `.rockface`.
2. **Abrir projeto…** (Ctrl+O) abre um projeto existente; a lista **Recentes** da página inicial guarda os últimos.
3. **Salvar projeto como…** grava uma cópia do projeto inteiro com outro nome e continua na cópia.
4. **Fechar projeto** volta à página inicial.

Um projeto num servidor da equipe é aberto com **Conectar ao servidor** (página [Trabalhar em equipe num servidor](server.md)).

### Uma nova descrição

1. **Início → Descrição → Nova descrição** (Ctrl+N).
2. Digite o **Nome da nova descrição** e escolha a sua **Lâmina delgada**:
   * uma lâmina nova, ou
   * uma já existente, quando vários petrógrafos (ou vários estudos) descrevem a mesma lâmina. A identificação começa
     então com o que já se sabe dessa lâmina: poço, profundidades, amostra, números.
3. A aba **Identificação** se abre. Preencha-a (página [Identificação de uma amostra](identification.md)) e as outras abas que precisar.
4. **Salvar** (Ctrl+S). Todas as abas são conferidas juntas: qualquer erro impede o salvamento inteiro, e a primeira
   aba com erro é mostrada, com o campo marcado.

No painel **Projeto**, um clique duplo numa lâmina também começa uma nova descrição dela.

### Carregar, salvar e copiar

* **Carregar descrição…** (Ctrl+L) lista as descrições com o seu poço, profundidade e lâmina; digite em **Filtrar…**
  para encurtar a lista. Um clique duplo no painel **Projeto** faz o mesmo.
* **Salvar** (Ctrl+S) grava a descrição aberta. Se você carregar outra ou fechar o projeto com mudanças não salvas,
  o RockFace pergunta antes.
* **Salvar como…** (Ctrl+Shift+S) grava uma cópia com outro nome (**Nome da cópia**). O nome de uma descrição salva
  não pode ser mudado: use Salvar como e exclua a antiga.
* **Excluir** remove a descrição aberta, com as suas partes e a contagem de pontos, depois de uma confirmação. Não se
  pode desfazer. Quando era a última descrição de uma lâmina, a lâmina sai também, a menos que tenha imagens do Atlas
  ou análises pontuais, ou que a sua amostra tenha análises ou solicitações: essas nunca são jogadas fora. O poço
  sempre fica.
* **Início → Formulário → Limpar** esvazia a aba mostrada, para recomeçá-la.

### Modelos

Um modelo é uma descrição guardada como ponto de partida: uma lista habitual de constituintes, o petrógrafo e a
instituição, um conjunto padrão de usos.

1. Abra uma descrição que seja um bom começo e use **Salvar como…**.
2. Marque **Marcar a cópia como modelo**.
3. Os modelos aparecem com o rótulo *modelo* no painel e ficam fora da contagem de descrições e das consultas do
   Explorer; uma exportação só os inclui quando pedido.
4. Para usar um: carregue-o, **Salvar como…** com o nome da nova amostra (sem a marca) e mude o que for diferente.

## Opções

| Campo | O que muda |
|---|---|
| Lâmina delgada (Nova descrição) | Lâmina nova, ou uma lâmina já no projeto: várias descrições de uma lâmina compartilham as suas imagens, o sistema de coordenadas da contagem e as análises. |
| Marcar a cópia como modelo | A cópia é um modelo: fica à parte da coleção. |

## Como funciona

O modelo de dados segue a rocha: bacia → campo → poço (ou afloramento) → testemunho → amostra → lâmina → descrição,
com as imagens, análises, volumes e perfis ligados à amostra ou à lâmina. Toda mudança fica escrita na tabela de
auditoria do projeto (quem, quando, o quê). Uma descrição é salva como uma transação: a identificação e todas as suas
partes, ou nada.

## Por script

```python
import rockface.api as rf
with rf.create("estudo.rockface") as prj:                  # um projeto novo, vazio
    d = prj.new("TS-9", well_name="ILLUSTRATIVE W-1", top_depth=2501.3, thin_section_no="9")
    prj.copy("TS-9", "TS-9 modelo", template=True)         # um modelo
    print([x.name for x in prj], len(prj.descriptions(templates=True)))
with rf.open("estudo.rockface") as prj:
    prj.delete("TS-9")
```

## Limites e problemas comuns

* "Já existe uma descrição chamada … neste projeto": os nomes são únicos num projeto.
* "O nome de uma descrição salva não pode ser alterado; use Salvar como."
* "Não salvo: …" na barra de status diz o campo a corrigir; a aba com o erro é mostrada.
* Num servidor, as descrições escritas por outra pessoa abrem só para leitura para um petrógrafo (página [Trabalhar em equipe num servidor](server.md)).

## Cobertura

P1 (janela principal), P2 (Nova, Carregar, Salvar, Salvar como, modelos, Excluir), P6 (lâmina escolhida para uma
descrição), P9 (Carregar descrição).

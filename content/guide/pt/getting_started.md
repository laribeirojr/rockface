# Primeiros passos

## Para que serve

O RockFace Suite descreve, fotografa, consulta e mede rochas sedimentares, da lâmina delgada ao banco de dados. São
cinco programas que abrem o mesmo projeto e a mesma lâmina: o que um grava, os outros leem na hora.

| Programa | Para | Abre com |
|---|---|---|
| **RockFace Petro** | a descrição de uma lâmina: identificação, composição, contagem de pontos, classificações, diagênese, relatórios | `rockface-petro` |
| **RockFace Atlas** | imagens de lâminas inteiras e fotos de detalhe no seu lugar na lâmina, anotações, mapas mineralógicos, análises pontuais | Início → **Atlas** (Ctrl+Shift+A) ou `rockface-atlas` |
| **RockFace Explorer** | consultas sobre uma coleção, o painel, grupos, figuras, apresentações, LAS, datação, evolução paragenética | Início → **Explorer** (Ctrl+Shift+E) ou `rockface-explorer` |
| **RockFace Lab** | análise de imagens de uma lâmina: recorte, filtros, registro, segmentação, objetos, medidas | Início → **Lab** (Ctrl+Shift+L) ou `rockface-lab` |
| **RockFace MC** | volumes de micro-CT, testemunhos inteiros e perfis de imagem de um poço | Início → **MC** (Ctrl+Shift+M) ou `rockface-mc` |

## Antes de começar

* O RockFace instalado no seu computador com o instalador que a equipe do RockFace lhe enviou (os downloads públicos começam na versão 1.0). O RockFace
  IA e o modelo de linguagem local são instalados à parte (páginas [RockFace IA: instalação, dispositivo e o hub de modelos](ai_setup_hub.md) e [Mio: perguntas em linguagem natural e o modelo de linguagem local](mio.md)).
* Nada mais: o primeiro projeto pode ser o exemplo ILUSTRATIVO.

## Passo a passo

### A página inicial

1. Abra o **RockFace Petro**. A página inicial mostra **Novo projeto**, **Abrir projeto…**, **Conectar ao servidor** e
   **Abrir o exemplo ilustrativo**, os projetos **Recentes** e os cinco programas de **A suíte RockFace**.
2. Escolha **Abrir o exemplo ilustrativo** para conhecer o programa. Ele grava um pequeno projeto com amostras
   inventadas (todos os nomes marcados ILLUSTRATIVE) e o abre.
3. Ou arraste um arquivo `.rockface` para a janela, para abri-lo.

### A janela

* A **faixa de opções** no alto tem quatro abas:
  * **Início** — os grupos **Projeto**, **Servidor**, **Descrição**, **Imagens** (Atlas, Lab, MC), **Coleção**
    (Explorer), **Relatórios e intercâmbio** e **Formulário**;
  * **Exibir** — **Tema escuro** e o **Idioma**;
  * **Ferramentas** — a **Base de conhecimento** (Nomenclatura, Escalas, Referências, Grafo de conhecimento),
    **Python** (Scripts) e **Mio**;
  * **Ajuda** — **Conteúdo da ajuda** (F1), **Sobre o RockFace**, **Licença**, **Suporte…**, **Plug-ins e
    atualizações…**, o grafo de conhecimento e os dois projetos ILUSTRATIVOS.
* O painel **Projeto**, à esquerda, lista os poços, as suas lâminas e as descrições de cada lâmina.
* As **abas da descrição**, no centro: Identificação, Macroscópica, Microscópica, Composição, Contagem de pontos,
  Sistema poroso, Classificação, Diagênese, Análises e Solicitações.
* A **barra de status**, embaixo, dá o resultado de cada ação; à direita, o número de descrições e o nome do projeto.

### Idioma e tema

1. **Exibir → Idioma**: English, Español ou Português. Todas as janelas mudam na hora, e a escolha fica guardada para
   a próxima vez.
2. **Exibir → Tema escuro** alterna entre o tema claro e o escuro.

O projeto não depende do idioma: um projeto escrito em português abre, e gera relatórios, em inglês ou espanhol. Só
os rótulos mudam; os valores guardados são os mesmos códigos.

### Ajuda dentro do programa

* **Ajuda → Conteúdo da ajuda** (F1) abre este guia no idioma da interface, com **Conteúdo**, **Índice** e
  **Buscar**.
* A **Mio**, a assistente do RockFace, responde perguntas do tipo "como faço…" com a página deste guia que explica
  (página [Mio: perguntas em linguagem natural e o modelo de linguagem local](mio.md)).
* **Ajuda → Suporte…** reúne as versões do RockFace e das suas bibliotecas para enviar com uma pergunta (sem nomes de
  arquivos e sem conteúdo do projeto).

### A coleção ILUSTRATIVA

**Ajuda → Abrir a coleção ILUSTRATIVA** grava um projeto de 48 descrições inventadas de quatro poços, com imagens,
análises, pontos U-Pb e uma tabela estratigráfica. Serve para experimentar o RockFace Explorer.

## Opções

| Onde | O que muda |
|---|---|
| Exibir → Idioma | O idioma da interface (inglês, espanhol, português) de todos os programas. |
| Exibir → Tema escuro | Janelas claras ou escuras. Diagramas e figuras são sempre desenhados em cores de papel. |
| Ajuda → Plug-ins e atualizações… | Os plug-ins instalados e a verificação de um RockFace mais novo (página [Ajuda, suporte, plug-ins e atualizações](help_plugins.md)). |

## Como funciona

Um projeto é um arquivo `.rockface` (um banco SQLite) ou um banco num servidor PostgreSQL compartilhado por uma equipe
(página [Trabalhar em equipe num servidor](server.md)). Cada imagem, ponto contado e análise pontual é guardado no sistema de coordenadas da sua lâmina
(milímetros), nunca só em pixels da imagem, e por isso os cinco programas concordam sobre onde as coisas estão.
Arquivos gravados por uma versão mais antiga são atualizados ao abrir; um arquivo gravado por uma versão mais nova é
recusado com uma mensagem.

## Por script

```python
import rockface.api as rf
with rf.example("demo.rockface") as prj:           # o projeto de exemplo ILUSTRATIVO
    print(len(prj), [d.name for d in prj])
```

Num terminal:

```
rockface example demo.rockface        # grava o projeto de exemplo ILUSTRATIVO
rockface collection coll.rockface     # grava a coleção ILUSTRATIVA (48 descrições)
rockface petro demo.rockface          # abre-o no RockFace Petro (também atlas, explorer, lab, mc)
```

## Limites e problemas comuns

* "Este projeto foi gravado por um RockFace mais novo": atualize o RockFace para abri-lo.
* "… não é um projeto RockFace": o arquivo não é um banco do RockFace (ou está danificado).
* As preferências (idioma, tema, projetos recentes) são do seu usuário neste computador, não do projeto.

## Cobertura

P1 (janela principal), P3 (barra de status), P10 (interface em inglês, português e espanhol), P40 (conteúdo da
ajuda), O1 (scripts).

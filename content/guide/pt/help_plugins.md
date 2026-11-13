# Ajuda, suporte, plug-ins e atualizações

## Para que serve

**Conteúdo da ajuda** (F1) abre este guia dentro do programa, com sumário, índice e busca. **Suporte** prepara o que
enviar ao pedir ajuda. **Plug-ins e atualizações** instala extensões escritas em Python e avisa quando existe um
RockFace mais novo.

## Antes de começar

Nada, para a ajuda. Para plug-ins: um `.zip` de plug-in (uma pasta com `plugin.json` e o código) ou o endereço de um
servidor de plug-ins.

## Passo a passo

1. **Ajuda → Conteúdo da ajuda** (F1). *Conteúdo*: páginas e seções; *Índice*: todos os títulos, com filtro;
   *Buscar*: palavras e Enter — as melhores seções primeiro.
2. **Ajuda → Suporte…**: as versões do RockFace, do Python, das bibliotecas e dos plug-ins, para copiar ou salvar;
   escreva para o endereço de suporte que a sua equipe definiu (preferência `support/contact`).
3. **Ajuda → Plug-ins e atualizações…**: *Instalar de um arquivo…* mostra o nome, o autor e o SHA-256 do arquivo
   antes de instalar; *Instalar de um repositório Git…* clona o repositório (acrescente `@ramo` ou `@etiqueta` ao
   endereço para uma versão) e mostra o commit antes de instalar; marque *Ativo* para ligar (no próximo início); *Remover*. *Servidor*: vazio para o catálogo do
   RockFace ou o endereço de outro `index.json`; *Listar os plug-ins do servidor* e clique duas vezes para instalar;
   *Procurar uma versão mais nova do RockFace*.

## Opções

| Campo do `plugin.json` | Significado |
|---|---|
| name, version, description, author, licence | mostrados na lista |
| requires | a versão mais antiga do RockFace com que funciona |
| module | o arquivo Python com `register(app)` |

## Como funciona

* O guia é o mesmo Markdown do site, indexado quando o programa é montado; a busca ordena as seções por BM25 sobre
  as palavras, como a Mio.
* Os plug-ins ficam em `~/.rockface/plugins`; um plug-in começa desativado e só é carregado depois que o usuário o
  ativa; um arquivo com caminhos para fora da pasta é recusado; um plug-in que falha no início é avisado, sem
  derrubar o programa.
* O índice do servidor lista o RockFace mais recente (versão, instalador, SHA-256, notas) e os plug-ins; um download
  só é guardado se o SHA-256 conferir. O RockFace nunca instala uma atualização sozinho.

## Por script

```python
rf.plugins.install_zip("ferramenta.zip"); rf.plugins.enable("ferramenta")
rf.plugins.install_git("https://example.org/team/tool.git", "v1.0")
rf.plugins.check_update("https://example.org/rockface/index.json")
```

## Limites e problemas comuns

* Um plug-in roda com as suas permissões: instale só o que é de confiança.
* O catálogo padrão será publicado junto com os instaladores (a partir da 1.0); até lá, use um servidor da equipe.

## Cobertura

P40 (conteúdo da ajuda, suporte), P41 (gerenciador de plug-ins e atualizador); Counterledge C6.

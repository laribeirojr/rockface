# O RockFace como servidor MCP para outros assistentes de IA

## Para que serve

Além de chamar serviços externos, o RockFace pode ser chamado por eles. O comando `rockface mcp serve` abre um
projeto como **servidor MCP** (Model Context Protocol): um assistente de IA que fala MCP — o Claude Desktop, um
editor de código, um agente corporativo — passa a consultar as amostras, ler tabelas, achar páginas do guia e escrever
scripts para o RockFace, conversando em linguagem natural com o usuário. É o caminho para tarefas maiores que as
receitas da Mio: o assistente lê a referência da interface de programação e escreve o script, que você executa no
RockFace.

## Antes de começar

* O RockFace instalado no computador e um projeto.
* Um assistente que aceite servidores MCP. Você é responsável pelo que o assistente envia para fora: se ele roda na
  nuvem, as respostas do RockFace chegam ao serviço dele. Para um projeto confidencial use um assistente local, ou não
  use este recurso.

## Passo a passo

### Ligar o RockFace ao assistente

1. Gere a configuração: `rockface mcp config projeto.rockface`. Sai um trecho JSON `mcpServers` com o comando que
   inicia o servidor.
2. Cole esse trecho no arquivo de configuração MCP do assistente (no Claude Desktop, o arquivo de configuração das
   ferramentas de desenvolvedor) e reinicie o assistente.
3. Pergunte ao assistente, por exemplo:
   * "No RockFace, quantas amostras têm calcita e quais são os poços?"
   * "Mostre a tabela de petrofísica das amostras com porosidade acima de 15 %."
   * "Como faço a contagem de pontos com platina motorizada no RockFace?"
   * "Escreva um script RockFace que, para cada poço, exporte o LAS e uma tabela de classificações de Folk."

### Deixar o assistente executar scripts

Com `rockface mcp config projeto.rockface --allow-scripts` o servidor oferece também `run_script`: o assistente
roda scripts no projeto e vê a saída. Use só num projeto de trabalho, com cópia de segurança, e com um assistente em
que confie.

### Servir por HTTP

`rockface mcp serve projeto.rockface --http 8765` serve o mesmo conteúdo por HTTP (Streamable HTTP) em
`127.0.0.1:8765`, só neste computador.

## Opções

| Ferramenta do servidor | O que dá ao assistente |
|---|---|
| `ask` | a resposta da Mio a uma pergunta (contagens, listas, estatísticas, valores, lacunas, uma descrição) |
| `search` | as descrições de uma pergunta e as condições lidas |
| `describe` | uma descrição em palavras |
| `table` | um conceito em tabela (identificação, composição, petrofísica, totais, classificações…), opcionalmente só das descrições de uma pergunta |
| `guide` | as páginas deste guia que respondem a uma pergunta |
| `write_script` | um script escrito pelas receitas da Mio (devolvido, não executado) |
| `api` | a referência da interface de programação (`rf`) |
| `run_script` | só com `--allow-scripts`: executa um script no projeto |

Recursos: `rockface://api` (a referência) e `rockface://guide/<página>` (as páginas do guia). Opções do comando:
`--lang pt|en|es` (idioma das respostas), `--allow-scripts`, `--http PORTA`.

## Como funciona

O servidor usa o SDK oficial do MCP em Python (licença MIT). Cada chamada do assistente gera uma linha na auditoria
do projeto (`mcp`), com a ferramenta e o texto pedido. As ferramentas, exceto `run_script`, só leem o projeto. As
respostas vêm do banco de dados e das receitas testadas; o assistente pode reformulá-las, mas os números são os do
RockFace.

## Por script

```python
cfg = rf.mcp_config("projeto.rockface")          # o trecho mcpServers
print(cfg)
print(rf.api_reference()[:2000])                 # o que a ferramenta api devolve
```

## Limites e problemas comuns

* O assistente não vê o RockFace: confira o caminho do projeto no trecho `mcpServers` e reinicie o assistente.
* Respostas em inglês: inicie com `--lang pt`.
* `run_script` não aparece: falta `--allow-scripts`.
* O projeto está aberto no RockFace ao mesmo tempo: as leituras funcionam; gravações de `run_script` e do programa
  podem se cruzar — feche um deles para gravar.

## Cobertura

Etapa 0.30 do ROADMAP (as ferramentas da Mio oferecidas também como servidor MCP).

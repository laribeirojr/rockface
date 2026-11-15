# Conversar com a Mio

## Para que serve

A Mio é uma conversa, como com um assistente de chat: você escreve como escreveria a um colega — *como exporto os
poços para LAS?*, *e a trajetória também?*, *o que é calcita poiquilotópica?*, *quantas amostras deste projeto têm
pirita?* — e ela responde em poucas frases, no seu idioma, e acompanha o fio da conversa. Não é preciso aprender
comandos nem palavras-chave.

Ela responde com o que o RockFace diz sobre si mesmo — o guia do usuário, os manuais e o site — e com o projeto aberto
na janela. Cada resposta indica as páginas de onde saiu, como links que abrem o guia na seção certa. Os números do seu
projeto são calculados pelas ferramentas do RockFace, como antes; um número da resposta que não está no que a Mio leu
aparece para ser conferido.

O modelo de linguagem roda só no seu computador. Ele é baixado uma vez; depois disso a Mio funciona sem internet e
nada do que você pergunta sai do computador.

## Antes de começar

* O RockFace 1.0.0rc3 ou mais recente, instalado pelo instalador (as duas edições trazem o llama.cpp, o motor que roda
  o modelo). A partir do código Python: `pip install "rockface-suite[llm]"`.
* Para o modelo recomendado, uns 4 GB de memória livre e 2,5 GB de disco; a internet uma vez, para baixá-lo. Não é
  preciso placa de vídeo.
* Um projeto aberto, para as perguntas sobre o projeto; as perguntas sobre o programa não precisam de projeto.

## Passo a passo

### Baixar o modelo (a primeira vez)

1. Abra o painel da Mio: o botão **Mio** da barra de ferramentas (no Petro, **Ferramentas → Mio**) ou **Ctrl+Alt+M**.
2. Quando ainda não há modelo, o painel oferece o recomendado para este computador — por exemplo *Qwen3 4B Instruct
   2507 (2,5 GB, roda no processador)*. Clique em **Baixar Qwen3 4B Instruct 2507**. Uma janela mostra o progresso do
   download; **Cancelar** interrompe.
3. **Outros modelos…** abre a lista dos modelos que cabem neste computador, um arquivo GGUF que você já tenha ou um
   servidor local (Ollama, LM Studio). **Agora não** esconde a oferta até o programa ser aberto de novo; a Mio então
   responde com as suas regras e os trechos do guia.
4. Quando o download termina, a Mio avisa que o modelo está pronto. A primeira resposta o carrega (alguns segundos); as
   seguintes começam logo.

### Conversar

1. Escreva na caixa de baixo e pressione **Enter** ou **Perguntar**.
2. A resposta aparece palavra por palavra. **Parar** interrompe.
3. Continue a conversa: *e com porosidade acima de 10?*, *explique o segundo passo*, *e em espanhol?*. Uma continuação
   curta é completada com as perguntas anteriores antes de a Mio procurar a resposta (numa pergunta sobre o projeto, a
   pergunta completa é a que as ferramentas respondem).
4. **Nova conversa** recomeça: a Mio esquece a conversa (o modelo continua carregado).

A figura mostra uma resposta escrita pelo Qwen3 4B Instruct 2507 num processador, registrada na avaliação de
15/11/2026 (`tools/mio_eval`).

### Fontes e números conferidos

* Abaixo de cada resposta, **Fontes** lista os trechos que a resposta cita ([1], [2]…). Um trecho do guia abre
  **Ajuda → Conteúdo da ajuda** (F1) na sua seção; um manual abre o PDF no site.
* Numa pergunta sobre o projeto, a resposta é escrita a partir do resultado da ferramenta (contagem, média, valores,
  resumo de uma amostra, um termo da nomenclatura, as idades U-Pb). **Abrir no Explorer** mostra uma busca como
  consulta do Explorer.
* *Confira estes números…* abaixo de uma resposta lista os números da resposta que não estão nos trechos nem nos
  resultados do projeto que a Mio recebeu.
* Os scripts (*escreva um script que…*), as chamadas a conectores (*ache Folk 1980 no Crossref*) e as skills chamadas
  pelo nome (*/well-summary A*) funcionam como antes.

## Opções

| Campo | O que muda |
|---|---|
| Usar o modelo de linguagem | Desligado: a Mio responde com as suas regras, e uma pergunta sobre o programa recebe os melhores trechos do guia |
| Modelo de linguagem… | O modelo: um da lista (o recomendado marcado), um arquivo GGUF ou um servidor local; processador ou placa de vídeo |
| `llm.context` (configurações) | Quantos tokens o modelo lê de uma vez (8192 por padrão): conversas longas guardam mais do seu começo |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DIR` | O modelo sem a interface (scripts, o terminal) |

Os modelos (licenças permissivas, quantização Q4_K_M; o recomendado depende da memória, das threads e da placa de vídeo
encontradas):

| Modelo | Arquivo | Licença | Para |
|---|---|---|---|
| Qwen3 4B Instruct 2507 | 2,5 GB | Apache-2.0 | a conversa (recomendado com 8 threads ou mais) |
| Qwen3 1.7B | 1,3 GB | Apache-2.0 | notebooks com menos de 8 threads (mais rápido, respostas mais simples) |
| Qwen2.5 0.5B Instruct | 0,4 GB | Apache-2.0 | computadores com pouca memória (respostas curtas) |
| Qwen2.5 7B Instruct · Qwen3 8B | 4,7–5,0 GB | Apache-2.0 | uma placa de vídeo |

## Como funciona

* **O que o RockFace diz.** O guia (português, inglês e espanhol), os sete manuais (em português, por enquanto) e os
  textos do site são cortados em uns 2 000 trechos que acompanham o programa. Para cada mensagem, os trechos que melhor
  a respondem são encontrados por estatística de palavras (BM25, sem acentos nem plurais; siglas como LAS mantidas),
  primeiro no idioma da mensagem. Quatro deles vão com a mensagem, numerados.
* **O que o projeto diz.** As perguntas sobre o projeto são respondidas pelas ferramentas da Mio (busca, contagem,
  estatística, valores, resumo, lacunas, nomenclatura, idades), as mesmas das versões anteriores; o resultado vai com
  a mensagem.
* **A resposta.** O modelo recebe quem é a Mio e a instrução de tirar os fatos sobre o programa só dos trechos, e os
  números do projeto só dos resultados, citando os trechos que usa. A conversa vai com cada mensagem; quando não cabe
  mais, as voltas mais antigas são encurtadas primeiro.
* **Conferido.** Cada número da resposta é procurado no que o modelo recebeu; os outros são listados para conferir.
  Uma pergunta que as ferramentas do projeto respondem vai ao modelo só com o resultado delas, e uma resposta cujos
  números não batem com esse resultado é trocada pela frase da própria ferramenta (com um aviso).
* **Medido.** Um conjunto de avaliação de 150 perguntas escritas como os usuários perguntam (70 em português, 40 em
  inglês, 40 em espanhol, uma ou mais sobre cada página do guia), mais perguntas sobre o projeto, conversa e
  continuações (`tools/mio_eval`): os trechos de uma página esperada estão entre os quatro dados ao modelo em 9 de cada
  10 perguntas. As respostas do modelo real são medidas pelo fluxo "Mio evaluation" do repositório de downloads: com o
  Qwen3 4B Instruct 2507 num processador, todas as respostas vieram no idioma da pergunta, 136 das 150 respostas sobre
  o programa citaram um trecho da página que responde e as 10 perguntas sobre o projeto deram os números das
  ferramentas (15/11/2026).
* **Privacidade.** O modelo roda no RockFace (llama.cpp) ou num servidor neste computador; um servidor em outro
  computador é recusado, a menos que você permita explicitamente.

## Por script

```python
import rockface.api as rf

c = rf.chat(lang="pt", model=True)                  # o modelo das configurações; model=None: regras e trechos
r = c.ask("Como exporto os poços para LAS?", on_token=print)
print(r.text, r.cited, [s["title"] for s in r.sources])
r = c.ask("E a trajetória também?")                 # a conversa continua
prj = rf.open("projeto.rockface")
print(prj.chat(model=True).ask("Quantas amostras têm pirita?").text)
print(rf.docs_search("porosidade de micro-CT", "pt", n=3))
```

No terminal: `rockface llm chat` (uma conversa; `--project arquivo.rockface` para as perguntas do projeto, `/new`
recomeça) ou `rockface llm chat --no-model --lang pt como instalo um plug-in?` para uma resposta.

## Limites e problemas comuns

* "Esta instalação não consegue rodar um modelo de linguagem sozinha": uma instalação anterior à 1.0.0rc3 — instale a
  atual ou escolha um servidor local em **Modelo de linguagem…**.
* Respostas lentas: no processador, as primeiras palavras levam de alguns segundos a uns trinta segundos, conforme o
  computador e o tamanho dos trechos; escolha o **Qwen3 1.7B** em **Modelo de linguagem…** para respostas mais rápidas,
  ou uma placa de vídeo.
* O download falha atrás de um proxy: o download usa as configurações de proxy do sistema; baixe o arquivo GGUF pelo
  navegador e escolha-o em **Modelo de linguagem… → Um arquivo GGUF neste computador**.
* Uma resposta sem fontes: o guia não tem nada sobre isso, ou a pergunta é geral (geologia, conversa). A Mio diz quando
  o guia não responde; confira o que ela diz com o guia.
* Um modelo local é menor que os assistentes da internet: ele pode entender mal uma pergunta. As fontes e os números
  conferidos estão lá para verificar a resposta.
* A Mio não altera o projeto: as ferramentas dela só leem; as sugestões só são gravadas quando você as aceita.

## Cobertura

Pedido do dono de 15/11/2026: a Mio como uma conversa em linguagem natural, como os assistentes baseados em modelos de
linguagem, respondendo com os guias do usuário, os manuais e o site; o modelo só local, baixado no primeiro uso
(ROADMAP 1.0.0rc3).

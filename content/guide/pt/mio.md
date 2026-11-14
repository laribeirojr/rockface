# Mio: perguntas em linguagem natural e o modelo de linguagem local

## Para que serve

A **Mio** é a assistente do RockFace. Você pergunta sobre as descrições do projeto com suas próprias palavras —
"quais amostras têm barita?", "quantas amostras do poço B têm porosidade acima de 20 %?", "permeabilidade média das
amostras com caulinita", "o que falta antes do estudo?", "como segmento uma lâmina com IA?" — e ela responde a partir
do banco de dados: as descrições que atendem, quantas, mínimo, média e máximo de um número, os valores de um campo,
os principais dados de uma amostra, as descrições sem um valor, a página deste guia que explica uma tarefa. Toda
resposta mostra as condições que ela leu, para você ver exatamente o que foi perguntado ao banco.

No Explorer a mesma leitura funciona como **busca em linguagem natural**: digite a pergunta na caixa de busca da
barra de ferramentas e a consulta aparece na lista de critérios, pronta para refinar, salvar ou exportar.

A Mio funciona sem modelo de linguagem (as regras dela entendem as palavras da nomenclatura do RockFace em português,
inglês e espanhol, números — também por extenso — e comparações). Um **modelo de linguagem local** — um modelo aberto pequeno que roda no seu
computador, no processador ou na placa de vídeo — permite entender perguntas mais livres: outras grafias ("baritina",
"caolim"), sinônimos ("romboedros de dolomita"), palavras fora da nomenclatura.

## Antes de começar

* Um projeto aberto com descrições.
* Para o modelo de linguagem: o RockFace com o extra `llm` (`pip install "rockface-suite[llm]"`, que instala o
  llama-cpp-python), ou um servidor local já em execução (Ollama, LM Studio ou llama-server). Não é preciso placa de
  vídeo.

## Passo a passo

### Perguntar à Mio

1. Clique em **Mio** na barra de ferramentas (no Petro: **Ferramentas → Mio**) ou pressione **Ctrl+Alt+M**. O painel
   da Mio abre à direita.
2. Digite a pergunta e pressione **Enter** (ou **Perguntar**). O `@mio` no início é opcional no painel.
3. Leia a resposta e a linha **Condições lidas**. **Palavras não usadas** lista as palavras que ela não transformou em
   condição — reformule se alguma delas importava.
4. Quando a resposta é uma busca, **Abrir no Explorer** mostra-a como consulta do Explorer.

Em qualquer caixa de busca que fala com a Mio (a do Explorer), um texto que começa com **@mio** vai para o painel.

### Perguntas que a Mio entende sem condições (0.31)

* **O tamanho do projeto** — *quantas descrições há?* → "O projeto tem 48 descrições."
* **Uma estatística por grupo** — *porosidade média por fácies*, *permeabilidade média por poço*, *compare a
  porosidade entre os campos*: uma linha por fácies (poço, formação, campo, zona, bacia, tipo de amostra, tipo de
  rocha) com a média, o número de descrições e o intervalo, e depois o total.
* **O que é um termo** — *o que é caulinita?*, *defina dolomita*: o termo da nomenclatura, o seu código, os nomes nas
  outras línguas, o grupo, as fontes da literatura e quantas descrições do projeto o têm.
* **O que falta** — *amostras sem porosidade*, *faltam permeabilidades?*, *amostras do poço X sem porosidade*: as
  descrições sem o número, para completar.
* **As idades** — *qual a idade do cimento de calcita?*, *quais idades U-Pb temos?*: as idades U-Pb salvas no projeto
  (aba **Datação U-Pb** do Explorer), com o erro a 95 %, o MSWD e o número de pontos.

### Busca em linguagem natural no Explorer

1. **Explorer** → digite na caixa *Buscar em linguagem natural…* (por exemplo *amostras com barita e porosidade acima
   de 20 %*) e pressione **Enter**.
2. Os critérios aparecem na lista e as descrições encontradas abaixo deles. Uma pergunta que não é uma consulta única
   ("calcita ou dolomita") seleciona as descrições na lista.

### Escolher o modelo de linguagem

1. No painel da Mio, clique em **Modelo de linguagem…**.
2. A janela mostra este computador (memória, threads, placas de vídeo, se o llama.cpp pode usar a placa) e os modelos
   que cabem nele, com tamanho, licença, onde rodaria e o **recomendado** marcado. Você escolhe:
   * **O modelo selecionado na lista** — baixado uma vez (pergunta antes, com o tamanho e a licença) e guardado em
     `~/.rockface/llm`;
   * **Um arquivo GGUF neste computador** — qualquer modelo no formato GGUF que você já tenha;
   * **Um servidor local** — o endereço do Ollama (`http://localhost:11434`), do LM Studio ou do llama-server, e o
     nome do modelo no servidor.
3. **Rodar em**: processador ou placa de vídeo. **OK** guarda a escolha; o modelo carrega na primeira pergunta.
4. **Usar o modelo de linguagem** (painel) liga e desliga o modelo; **Respostas fluentes** deixa o modelo reescrever
   a resposta (mantida só quando os números são exatamente os do banco).

Na linha de comando: `rockface llm setup` (a mesma escolha, com o recomendado marcado), `rockface llm use
<arquivo.gguf | http://localhost:11434>`, `rockface llm info` e `rockface llm ask <projeto> "<pergunta>"`.

## Opções

| Campo | O que muda |
|---|---|
| Usar o modelo de linguagem | Desligado: as regras respondem sozinhas. Ligado: o modelo lê as perguntas em que as regras deixam palavras |
| Respostas fluentes | O modelo reescreve a resposta; uma reescrita com qualquer número mudado é descartada |
| Rodar em | Processador ou placa de vídeo (a placa exige o llama.cpp compilado com CUDA, Metal ou Vulkan) |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DEVICE` | O modelo sem a interface (scripts, trabalhos) |
| `ROCKFACE_LLM_DIR` | Onde ficam os modelos baixados |

Os modelos oferecidos (todos com licenças permissivas, quantização Q4_K_M):

| Modelo | Arquivo | Licença | Para |
|---|---|---|---|
| Qwen2.5 0.5B Instruct | 0,40 GB | Apache-2.0 | qualquer computador |
| Qwen3 1.7B | 1,28 GB | Apache-2.0 | notebooks (recomendado com menos de 8 threads) |
| Qwen3 4B · Phi-4 mini | 2,5 GB | Apache-2.0 · MIT | 8 threads ou mais, 8 GB de memória |
| Qwen2.5 7B Instruct · Qwen3 8B | 4,7–5,0 GB | Apache-2.0 | uma placa de vídeo |

## Como funciona

* **Quem responde é o banco, nunca o modelo.** A pergunta é lida em critérios do Explorer (os mesmos que você monta à
  mão) e as descrições são encontradas pelo Explorer nos registros. Ao modelo só se pede que transforme as palavras que
  as regras não entenderam em frases do vocabulário do RockFace, com números; as frases dele são conferidas com o
  vocabulário (uma frase que não está nele é descartada ou trocada pela mais próxima) e lidas de novo pelas regras,
  então toda condição é uma que o usuário vê. A resposta restrita a um esquema JSON (gramática do llama.cpp) impede o
  modelo de escrever outra coisa.
* **As regras.** O vocabulário é a base de conhecimento do projeto (constituintes, grupos, hábitos, localizações,
  modificadores em três línguas), os valores da identificação (poços, formações, fácies…), as análises (porosidade,
  permeabilidade, profundidade, totais) e as análises pontuais; as palavras são comparadas sem acentos e sem plural,
  com tolerância de uma letra nas palavras longas; os números se ligam à palavra numérica mais próxima, os hábitos ao
  constituinte mais próximo.
* **As ferramentas.** `search`, `count`, `stats`, `values`, `describe`, `missing`, `suggest`, `guide`, `define`, `ages` — todas só leem.
  As **skills** da Mio as encadeiam (página *Skills da Mio*).
* **Privacidade.** O modelo roda no computador; um endereço de servidor em outro computador é recusado a menos que
  você permita explicitamente, porque as perguntas e os registros mostrados ao modelo sairiam do computador.
* **Aceite num conjunto de teste.** Um projeto ILUSTRATIVO de 48 descrições inventadas de conteúdo conhecido e 41
  perguntas em português, inglês e espanhol: 41 certas pelas regras. Quinze paráfrases mais difíceis: 8 certas só
  pelas regras, 13 com o Qwen2.5 0.5B num processador sem placa de vídeo (2 threads; 3–14 s, mediana de 5 s, nas
  perguntas que chamam o modelo) — `docs/LLM.md`.

## Por script

```python
a = prj.ask("amostras com barita e porosidade acima de 20 %")      # só as regras
print(a.count, a.names, a.explanation, a.unknown)
q = a.query()                                                      # a consulta do Explorer, quando é uma
mio = prj.mio(model=True, lang="pt")                               # com o modelo de linguagem configurado
r = mio.ask("@mio quantas amostras do poço ILLUSTRATIVE-B têm caulinita?")
print(r.tool, r.text, r.data)
from rockface.api import llm
m = llm.LlamaModel("Qwen2.5-0.5B-Instruct-Q4_K_M.gguf", device="cpu")   # ou llm.ServerModel("http://localhost:11434", "qwen2.5:0.5b")
print(prj.ask("plugues com baritina", model=m).names)
```

## Limites e problemas comuns

* "Sem modelo de linguagem": escolha um em **Modelo de linguagem…** ou com `rockface llm setup`; a Mio continua
  respondendo com as regras.
* Uma palavra ignorada: aparece em **Palavras não usadas**; use o termo da nomenclatura ou ligue o modelo.
* A primeira pergunta com modelo leva alguns segundos a mais (o modelo é carregado uma vez por sessão).
* Num projeto em servidor o painel responde na linha de execução da janela (a janela espera enquanto o modelo lê).
* A Mio não altera o projeto: ferramentas e skills só leem; sugestões só são gravadas quando você as aceita.

## Cobertura

L1 (busca em linguagem natural no banco de dados), o assistente que chama as ferramentas do programa e a escolha do
processador ou da placa de vídeo da etapa 0.27 do ROADMAP.

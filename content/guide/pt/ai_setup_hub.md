# RockFace IA: instalação, dispositivo e o hub de modelos

## Para que serve

O RockFace IA acrescenta redes neurais ao Lab e ao MC: modelos que segmentam imagens, lâminas inteiras, volumes de
micro-CT e perfis de imagem, que podem ser treinados e ajustados com as suas próprias anotações, e um modelo gerativo
de imagens de rocha. É uma **opção**: o RockFace sem IA tem todas as outras funções, e nada mais muda quando ela é
acrescentada. Esta página mostra como instalá-la para o computador que você tem, como escolher onde os modelos rodam
(o processador ou uma placa de vídeo) e como os modelos são guardados, compartilhados e comparados no **hub de
modelos**.

## Antes de começar

* RockFace instalado (0.26 ou posterior).
* Para uma placa de vídeo: o driver da própria placa (NVIDIA, AMD ou Intel). O resto vem com os pacotes.

## Passo a passo

### Instalação: o computador é identificado, você escolhe

1. Num terminal, rode `rockface ai setup`. O RockFace lista o que encontrou — sistema, processador, núcleos,
   instruções vetoriais, memória, placas de vídeo e os pacotes de IA já instalados — e as opções para este computador:

   | Opção | Quando |
   |---|---|
   | RockFace sem IA | Nada mais a instalar |
   | IA no processador | Qualquer computador; aplicar um modelo leva de segundos a minutos, treinar de minutos a horas |
   | IA na placa de vídeo NVIDIA (CUDA) | Uma placa NVIDIA: a mais rápida para aplicar e para treinar |
   | IA na placa de vídeo (DirectML) | Windows com qualquer placa DirectX 12 (NVIDIA, AMD, Intel): os modelos são aplicados na placa, o treino roda no processador |
   | IA no Apple silicon (Core ML e MPS) | Um Mac com processador M |

   A opção recomendada vem marcada; **a decisão é sua**. Digite o número dela (ou Enter para a recomendada).
2. O RockFace mostra o comando de instalação (`python -m pip install …`) e pergunta antes de rodá-lo. Com
   `--option cuda --yes` ele escolhe e instala sem perguntar; com `--dry-run` só mostra o comando.
3. O mesmo diálogo está no programa: **Lab → IA** ou **MC → IA**, botão **Hardware e dispositivo…**. Ele mostra o
   hardware, as opções com a recomendada em negrito e o comando que instala a selecionada (com o botão **Copiar**).
   **OK** guarda a sua escolha.

`rockface ai info` mostra o hardware e o dispositivo em uso; `rockface ai models [projeto]` lista os modelos.

### O hub de modelos

A tabela **Modelos** da aba IA lista todos os modelos que o RockFace conhece para aquela aba, de três lugares:

* **RockFace** — os modelos que vêm com o programa (veja *Como funciona*);
* **Pasta do hub** — uma pasta compartilhada pela equipe (um drive de rede, uma pasta sincronizada), escolhida na
  primeira vez em que se clica **Publicar no hub**, ou dada pela variável `ROCKFACE_AI_HUB`;
* **Projeto** — os modelos treinados no projeto ou importados para ele.

Selecione uma linha e use:

* **Ficha…** — o que o modelo é: tarefa, entradas, classes, os dados com que foi treinado e as suas licenças, as
  métricas em dados reservados, o modelo pai (quando foi ajustado) e a sua linhagem, e o SHA-256 da rede;
* **Importar… / Exportar…** — um modelo como um arquivo `.rfai`, para enviar a um colega ou guardar;
* **Publicar no hub** — o modelo gravado na pasta do hub como `<nome>/<versão>.rfai`, com um `index.json` do hub; uma
  versão nunca é sobrescrita;
* **Excluir** — um modelo do projeto (com uma linha na auditoria);
* **Comparar** — as fichas das linhas selecionadas lado a lado (métricas, dados, pai).

## Opções

| Campo | O que muda |
|---|---|
| Opção (setup) | Quais pacotes são instalados e qual dispositivo roda os modelos |
| `ROCKFACE_AI_DEVICE` | O dispositivo sem a interface (`cpu`, `cuda`, `directml`, `coreml`) — para scripts e trabalhos |
| `ROCKFACE_AI_HUB` | A pasta do hub sem a interface |

## Como funciona

* **Duas camadas, instaladas à parte.** Aplicar um modelo usa o ONNX Runtime (licença MIT; extra `ai`), cujos
  provedores de execução rodam a mesma rede no processador, em CUDA, em DirectML ou em Core ML; o processador é sempre
  a alternativa. Treinar usa o PyTorch (licença BSD; extra `ai-train`) no processador, em CUDA ou no MPS da Apple.
* **Um modelo é dado, nunca código.** Um arquivo `.rfai` é um zip com `model.onnx` (a rede, formato ONNX) e
  `card.json` (a sua ficha). A ficha guarda o SHA-256 da rede, conferido a cada leitura: um arquivo alterado é
  recusado. Modelos nunca são objetos Python serializados (pickle).
* **Versões e linhagem.** Cada modelo tem nome e versão; ajustar um modelo faz a versão seguinte, com o modelo de
  origem como pai; o mesmo nome e versão não podem ser guardados duas vezes.
* **Os modelos que vêm com o programa** foram treinados só com dados cuja licença permite — os dados sintéticos do
  RockFace (verdade exata) e dados abertos sob CC BY 4.0 ou ODC-BY — e cada ficha declara os dados e as métricas
  medidas em dados que o modelo não viu. Dados sob licenças não comerciais ou de compartilhamento pela mesma licença
  são usados só em testes internos, nunca para treinar um modelo distribuído.

## Por script

```python
info = prj.ai_hardware()              # hardware, opções (a recomendada marcada), dispositivo, pacotes instalados
for m in prj.ai_models():             # todos os modelos: origem, nome, versão, tarefa, licença, métricas
    print(m["name"], m["version"], m["metrics"])
m = prj.ai_model("rockface-thinsection-pores")      # a versão mais nova, onde estiver
prj.ai_export(m, "pores.rfai"); rid = prj.ai_import("pores.rfai")
prj.ai_publish(rid, "//servidor/rockface-hub"); print(prj.ai_lineage(rid))
```

## Limites e problemas comuns

* "O RockFace IA não está instalado": rode `rockface ai setup` (ou `pip install -e ".[ai]"` a partir do código).
* "O treinamento precisa do extra ai-train": aplicar modelos funciona; treinar precisa do PyTorch
  (`pip install -e ".[ai-train]"`).
* No Linux, o pacote PyTorch do PyPI traz as bibliotecas CUDA (cerca de 3 GB). Para um computador só com processador,
  instale-o do índice CPU do PyTorch (`pip install torch --index-url https://download.pytorch.org/whl/cpu`).
* Uma placa que não aparece: atualize o driver; no Windows a opção DirectML funciona com qualquer placa DirectX 12.

## Cobertura

L13 (hub de modelos), GT18 / GV19 (os modelos pré-treinados e a escolha do modelo para o hardware encontrado) e a
instalação da IA da etapa 0.26 do ROADMAP.

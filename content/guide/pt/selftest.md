# Autoteste de uma instalação

## Para que serve

O autoteste verifica, em cerca de um minuto, que o RockFace funciona neste computador: o que depende do computador e
não do programa — as bibliotecas, os relatórios em todos os formatos, os arquivos, as figuras, o processamento de
imagens e volumes, os modelos de IA, a Mio e as cinco janelas na tela de verdade. Execute-o depois de instalar e
sempre que algo se comportar de modo estranho; o relatório dele é o que a equipe do RockFace pede quando você relata
um problema.

## Antes de começar

* Nada a preparar. O autoteste faz os seus próprios dados ILUSTRATIVOS numa pasta temporária e nunca abre, muda ou
  salva os seus projetos nem as suas preferências.

## Passo a passo

1. No RockFace Petro: **Ajuda → Executar o autoteste…**.
2. A janela lista cada verificação quando ela termina. Os cinco programas abrem e fecham sozinhos: não clique neles.
3. No fim, **Abrir o relatório** mostra o `report.html` no navegador, com as imagens que ele fez; **Abrir a pasta**
   mostra a pasta com `report.html`, `report.json` e `selftest.zip`.
4. Se uma verificação falhou, envie o `selftest.zip` com o seu relato (veja [Enviar a sua opinião](feedback.md)).

## Opções

| Onde | O que faz |
|---|---|
| `rockface selftest` | As mesmas verificações num terminal, sem as janelas |
| `--gui` | Também abre e fotografa as cinco janelas (Ajuda → Executar o autoteste… faz isso) |
| `--quick` | Só o relatório HTML entre os formatos de relatório |
| `-o PASTA` | A pasta do relatório (padrão: uma pasta temporária nova) |
| `--open` | Abre o `report.html` no fim |

## Como funciona

| Parte | O que é verificado |
|---|---|
| Instalação | Versão, sistema, edição (com ou sem IA), os arquivos de licença |
| Numérica | numpy, SciPy, scikit-image e scikit-learn, com um limiar de resposta conhecida |
| Projetos | O projeto de exemplo ILUSTRATIVO gravado, fechado e aberto de novo; os totais e a classificação de Folk (1980) |
| Relatórios | O relatório de uma descrição em HTML, Word, Excel e PDF |
| Intercâmbio | As descrições exportadas para um arquivo `.rfx` e importadas num projeto novo |
| Figuras | Um diagrama ternário |
| Imagens | Uma lâmina sintética com resina azul de porosidade conhecida: filtro e segmentação; a porosidade encontrada deve ficar a menos de 3 pontos da desenhada |
| Volumes | Um volume de microtomografia sintético de porosidade conhecida: importação e segmentação de Otsu, a menos de 2 pontos |
| IA | O modelo de lâminas que vem com o programa aplicado à lâmina sintética (edição AI; "não se aplica" na outra), o dispositivo e se o treinamento está disponível |
| Mio | Uma pergunta em linguagem comum lida pelas regras |
| Servidor | O driver PostgreSQL do modo servidor |
| Interface | As cinco janelas, o tamanho e a escala da tela |

Cada verificação é independente: uma falha nunca interrompe as outras. Uma verificação que não se aplica à
instalação (os modelos de IA na edição sem IA) é marcada "não se aplica", e não como falha.

## Por script

```python
import rockface.api as rf

res = rf.selftest(gui=False, quick=True)
print(res["summary"], res["folder"])     # {'passed': 13, 'skipped': 0, 'failed': 0} and the folder of report.html
```

## Limites e problemas comuns

* **A verificação das janelas num computador sem tela.** Execute `rockface selftest` sem `--gui`, ou defina
  `QT_QPA_PLATFORM=offscreen`.
* **Na primeira vez demora mais.** O sistema operacional e o antivírus verificam os arquivos do programa na primeira
  execução.

## Cobertura

1.0 (autoteste da instalação; ROADMAP).

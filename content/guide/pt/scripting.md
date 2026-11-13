# Scripts em Python

## Para que serve

Todos os programas do RockFace podem ser conduzidos por scripts em Python por meio de uma API pública,
`rockface.api`: para preencher muitas descrições de uma vez, gerar as tabelas e figuras de um estudo, conferir uma
coleção inteira ou automatizar qualquer tarefa do Atlas, Explorer, Lab e MC. Os scripts ficam guardados no projeto,
podem virar botões da faixa de opções e rodam também sem a interface, num terminal ou num notebook Jupyter.

## Antes de começar

* Um projeto aberto, para guardar scripts nele ("Abra um projeto para guardar scripts nele.").
* Python básico. O botão **API…** e o `docs/SCRIPTING.md` do código-fonte listam todas as chamadas.

## Passo a passo

### A janela de scripts

1. **Ferramentas → Python → Scripts** (Ctrl+Shift+P). A janela **Scripts Python** se abre.
2. **Scripts do projeto** à esquerda: **Novo**, **Excluir**, **Importar .py…**, **Exportar .py…**.
3. Dê ao script um **Nome**. Marque **Botão** para listá-lo sob a seta do botão **Scripts** da faixa de opções.
4. Escreva o script no editor (números de linha, realce de Python). Num script:
   * `rf` — a API; `project` — o projeto aberto; `current` — a descrição aberta na interface;
   * `ui.message(texto)` escreve na barra de status; `ui.open(nome)` abre uma descrição depois que o script termina.
5. **Executar** (F5 ou Ctrl+Shift+J) roda o script inteiro; **Executar seleção** (Ctrl+J) roda as linhas
   selecionadas ou a linha atual.
6. **Saída** mostra o que o script imprime e os seus erros, com a linha do erro marcada no editor ("O script parou
   com um erro na linha …").
7. O **console** sob a saída avalia uma linha no mesmo espaço de nomes da última execução — Enter executa.
8. **Salvar no projeto** (Ctrl+S).

Se a descrição aberta tiver mudanças não salvas, o RockFace pergunta se deve salvá-la antes da execução, e a recarrega
depois.

### Um primeiro script

```python
for d in project:
    t = d.totals()
    print(d.name, round(t["porosity"], 1), d.classify("folk1980", label=True))
rows = project.table(totals=["volume", "qt", "feldspar", "igv"], classifications=["folk1980"])
project.to_csv("resumo.csv", rows)
ui.message(f"{len(rows)} descrições gravadas")
```

### Sem a interface

```
rockface script meu_script.py --project estudo.rockface -- arg1 arg2
```

No Jupyter ou em qualquer programa Python:

```python
import rockface.api as rf
with rf.open("estudo.rockface") as prj:
    print(len(prj))
```

`rockface notebook estudo.rockface` grava um notebook que abre o projeto (página [MC → Mais: copos, mapa de distâncias, vigia de pasta, reconstrução, transferência de escala e escoamento bifásico](mc_more_tools.md)).

### Os scripts de exemplo

O projeto de exemplo ILUSTRATIVO traz os scripts de exemplo: uma tabela-resumo, uma figura de proveniência, um total
personalizado, uma conferência de todas as descrições, o resumo da diagênese, relatórios em lote, a visão geral do
Atlas, figuras anotadas, mapas mineralógicos, análises pontuais, consultas e figuras do Explorer, datação e evolução,
e os exemplos do Lab e do MC.

## Opções

| Opção | O que faz |
|---|---|
| Botão | Lista o script sob o botão Scripts da faixa de opções (aba Ferramentas). |
| Executar seleção | Roda só as linhas selecionadas, ou a linha atual. |

## Como funciona

* **As mesmas verificações.** Um script não consegue gravar o que os formulários recusariam: `d.save()` valida
  exatamente como os formulários e levanta `rf.ScriptError` com as mensagens, sem gravar nada.
* **Auditoria.** O que um script grava é registrado com o nome do usuário seguido de ` [script]`.
* **Scripts escritos por outros.** Um script guardado num projeto e escrito por outra pessoa só roda depois de uma
  confirmação ("Um script pode ler e alterar o projeto e os arquivos deste computador. Executá-lo?").
* **Estabilidade.** `rf.API_VERSION` segue o versionamento semântico: dentro da 1.x os nomes só são acrescentados.
* **Licença.** Os scripts que usam a API são obra do próprio usuário: escrevê-los, executá-los e compartilhá-los é
  permitido.

## Por script

Esta página é sobre scripts; a seção "Por script" de cada outra página deste guia mostra as chamadas daquela função.

## Limites e problemas comuns

* "O script parou com um erro na linha …": o traceback na saída mostra só as linhas do próprio script.
* Um script roda com os seus direitos no computador: execute só scripts em que confia.
* Um script longo bloqueia a janela enquanto roda; para cálculos longos do MC use trabalhos (página [Trabalhos: computação em lote e remota](jobs.md)).

## Cobertura

O1 (scripts em Python em todos os aplicativos do RockFace).

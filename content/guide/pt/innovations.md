# As seis inovações

## Para que serve

Além das funções dos programas de referência, o RockFace traz seis inovações de método, uma por versão da 1.0.0rc4 à
1.0.0rc9, da mais simples à mais ousada. Esta página diz o que cada uma faz, onde está nos programas e como foi
conferida; cada uma tem a sua página.

| # | Inovação | Versão · onde | O que dá ao petrógrafo |
|---|---|---|---|
| 1 | [Quão segura é a contagem de pontos](counting_uncertainty.md) | 1.0.0rc4 · Petro | O intervalo de 95 % de cada constituinte contado, a probabilidade de cada campo das classificações, a região de confiança no diagrama ternário e quantos pontos ainda faltam |
| 2 | [Consistência entre escalas](consistency.md) | 1.0.0rc5 · Petro, MC, Lab | Sete verificações entre lâmina, plugue, micro-CT, perfil e sequência paragenética, cada contradição explicada com a sua fonte |
| 3 | [Ditado no microscópio](dictation.md) | 1.0.0rc6 · Petro, Mio | Ditar a descrição e contar por voz sem sair da ocular; reconhecimento no próprio computador |
| 4 | [Contagem de pontos assistida por IA](assisted_counting.md) | 1.0.0rc7 · Petro | Um modelo que aprende com os pontos contados e propõe os próximos, os mais incertos primeiro, com uma concordância honesta |
| 5 | [A Mio olha a imagem](mio_vision.md) | 1.0.0rc8 · Mio, Atlas | Um modelo de visão na placa de vídeo do laboratório propõe a textura e o sistema poroso a partir de uma fotomicrografia, cada proposta com quantas respostas concordam |
| 6 | [Aprendizado federado entre laboratórios](federated_learning.md) | 1.0.0rc9 · Petro | Laboratórios treinam juntos um modelo da contagem; só os números do modelo saem de cada um |

## Passo a passo

1. **Quão segura é a contagem**: Composição → a coluna *Intervalo de 95 %*; Classificação → *Probabilidade*; o
   diagrama ternário → *Região de confiança*; a aba Contagem de pontos diz quando a classificação está estável.
2. **Consistência**: a aba *Consistência* de uma descrição, ou a Mio: *"a ILL-TS-001 está consistente?"*.
3. **Ditado**: Início → **Ditar**; na aba Contagem de pontos, o botão do microfone.
4. **Contagem assistida**: aba Contagem de pontos → **Propor o constituinte (IA)**; Enter aceita.
5. **A Mio olha**: Início → **Mio olha** (um modelo de visão no computador, escolhido em *Modelos de visão…*).
6. **Aprendizado federado**: Ferramentas → **Aprendizado federado**; na aba Contagem de pontos, **Modelo
   compartilhado**.

## Como funciona

As seis seguem os mesmos princípios:

* **Local.** Tudo roda no computador do usuário — as estatísticas, o reconhecimento de fala, o modelo de visão, o
  modelo da contagem; numa federação só saem os números do modelo, num arquivo que o laboratório lê antes.
* **O petrógrafo decide.** O programa propõe e diz quão seguro está; nada é gravado até o petrógrafo aceitar, e os
  pontos às cegas medem a concordância sem o viés de ver a proposta antes.
* **Medido.** Cada inovação tem critério de aceitação e testes automáticos: os intervalos cobrem 95 % por simulação;
  todos os exemplos do guia do ditado são entendidos nos três idiomas; 91 % dos pontos restantes certos depois de 75
  contados pelos mais incertos, contra 81 % na ordem da grade; um modelo federado acerta 83 % num laboratório que não
  participou, contra 79 % de cada laboratório sozinho (dados ILLUSTRATIVE).
* **Com fontes.** Cada versão começou por um levantamento da literatura e das patentes; as referências estão em cada
  página, as notas de patentes na auditoria de licenças. A busca de lâminas parecidas numa biblioteca (inovação 5)
  ficou de fora por decisão do proprietário, até uma consulta de patentes.

## Por script

```python
d = prj["ILL-TS-002"]
d.uncertainty()                 # 1 · intervalos e probabilidades
d.consistency()                 # 2 · as verificações entre escalas
d.dictate("moderadamente selecionado, grãos subarredondados", "pt")   # 3 · propostas a partir de texto
d.assist(top=5)                 # 4 · propostas da IA da contagem
d.look(samples=3)               # 5 · o que o modelo de visão propõe
prj.federated_update("fed-r1.rffed", "lab.rfupd", site="Lab A")   # 6 · a atualização deste laboratório
```

## Limites e problemas comuns

* As propostas de 3 a 6 são propostas: cada página diz como foram medidas e onde podem falhar.
* O modelo de visão (5) foi testado com respostas roteirizadas; o acerto em lâminas reais ainda será medido.
* O aprendizado federado (6) protege os dados, não todo vestígio deles no modelo: a página dele diz o que o corte e o
  ruído fazem e não fazem.

## Cobertura

O8 (pedido do proprietário de 2026-11-17: "Gostei de todas elas. Podemos implementar da mais simples para a mais
ousada?").

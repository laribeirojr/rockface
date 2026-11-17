# Aprendizado federado entre laboratórios

## Para que serve

Vários laboratórios treinam **juntos um modelo da contagem de pontos**, e cada um guarda suas imagens, pontos e
descrições. Só os números do modelo saem de um laboratório, num arquivo que ele pode ler antes de enviar. O modelo
compartilhado então ajuda as contagens de todos: com as **propostas da IA** da contagem de pontos (1.0.0rc7), ele
propõe o constituinte sob um ponto **desde o primeiro ponto**, antes que uma contagem nova tenha os 15 pontos de que o
modelo dela precisa.

## Antes de começar

* Contagens com a imagem (aba Contagem de pontos → a imagem da lâmina), pontos contados e linhas cujo constituinte
  está na base de conhecimento do RockFace. A imagem com nicóis cruzados só é necessária se a federação pedir.
* Pelo menos 50 pontos contados nas contagens enviadas (com menos pontos é mais fácil recuperá-los de uma atualização).
* Um laboratório **coordena**: cria a federação e combina as atualizações. Qualquer laboratório pode fazer isso.
* Um meio de trocar arquivos pequenos (cerca de 55 kB cada): e-mail, pasta compartilhada, disco — o que cada
  instituição permitir. O RockFace não envia nada sozinho.

## Passo a passo

**O coordenador — criar a federação.** Ferramentas → **Aprendizado federado** → *Coordenar*. Dê um nome, o número de
rodadas (20), as passadas locais por rodada (2), a atualização máxima (5) e, se quiser, ruído (veja abaixo). **Criar a
federação…** grava `<nome>-r1.rffed`. Envie-o aos laboratórios.

**Cada laboratório — participar.** *Participar* → **Abrir uma federação…** → o `.rffed` recebido. Digite o nome que
os outros verão (p. ex. *Lab A*), marque as contagens a usar e clique em **Preparar minha atualização**. O RockFace
mostra **o que sai deste computador — o arquivo inteiro**: a federação, a rodada, o nome do laboratório, o número de
pontos, a mudança dos pesos do modelo (uns dez mil números), o tamanho dela e como o modelo compartilhado se saiu em
20 % dos seus próprios pontos reservados, antes e depois das suas passadas. Abaixo, **o que fica aqui**: seus pontos
por constituinte. **Salvar a atualização…** e envie o `.rfupd` ao coordenador.

**O coordenador — a próxima rodada.** *Coordenar* → **Abrir uma federação…** (o `.rffed` atual) → **Adicionar as
atualizações dos laboratórios…** → **Combinar na próxima rodada…** grava `<nome>-r2.rffed`. O histórico mostra cada
rodada: os laboratórios com seus pontos e quantos dos pontos reservados deles o modelo compartilhado acertou antes e
depois. Envie o novo arquivo aos laboratórios e repita.

**Todos — usar na contagem.** *Usar na contagem* → **Escolher o modelo compartilhado…** (o `.rffed` mais recente). Na
aba Contagem de pontos marque **Propor o constituinte (IA)** e **Modelo compartilhado**: as propostas vêm desde o primeiro ponto,
marcadas *(modelo compartilhado)*; à medida que você conta, o seu próprio modelo aprende e os dois se misturam — o
modelo compartilhado pesa como 30 dos seus pontos, e cada vez menos (*esta contagem e o modelo compartilhado*). Nada é
contado por você: Enter aceita uma proposta, como na 1.0.0rc7, e os pontos às cegas continuam medindo a concordância
com honestidade.

**Mio**: *"como está a federação?"* (*"status of the federated model?"*, *"¿cómo va la federación?"*) mostra o modelo
compartilhado em uso, as rodadas, os laboratórios da última rodada e os acertos nos pontos reservados deles.

## Como funciona

* **O modelo.** Uma rede de uma camada oculta sobre as mesmas 45 características do assistente da contagem (cor,
  dispersão, saturação, matiz, percentis de brilho, bordas e resina azul em janelas de 3 × 3 pixels, 30 µm e 90 µm em
  volta do ponto; 90 com a imagem com nicóis cruzados). As classes são **todos os constituintes da base de
  conhecimento embutida** (106): uma lista fixa, então a lista não diz nada sobre as rochas de ninguém.
* **Cada imagem padronizada por ela mesma.** Antes de o modelo ver um ponto, cada característica é padronizada pela
  média e dispersão daquela característica em todos os pontos da grade da mesma imagem, contados ou não. Isso tira o
  corante, a lâmpada e a câmera de cada laboratório e não precisa de estatística de ninguém — a ideia de manter a
  normalização local (FedBN, Li et al. 2021).
* **Média federada.** A cada rodada cada laboratório parte dos pesos compartilhados, faz algumas passadas sobre os
  próprios pontos e envia a mudança; o coordenador soma a média das mudanças, cada uma pesada pelo seu número de pontos
  (FedAvg, McMahan et al. 2017; o termo proximal do FedProx está disponível por script, Li et al. 2020). Rodadas por
  arquivos foram como duas petroleiras e uma universidade fizeram um teste federado com rochas digitais: os pesos
  foram por transferência de arquivos, e os modelos federados superaram o modelo próprio de cada participante (Chang
  et al. 2024).
* **Verificações.** Uma atualização de outra federação, de outra rodada, feita a partir de outra versão do modelo, de
  um laboratório já presente na rodada, com um campo que não deveria estar lá ou com números não finitos é recusada.
  Todo arquivo leva uma impressão digital; um arquivo alterado é recusado.
* **O que protege e o que não protege.** Imagens, pontos, coordenadas, nomes e os constituintes contados nunca saem.
  Mas os números de um modelo ainda podem dizer algo sobre os dados de que ele aprendeu: gradientes podem ser
  invertidos (Zhu et al. 2019) e a participação de um dado adivinhada (Shokri et al. 2017). Uma atualização de centenas
  de pontos depois de várias passadas é muito mais difícil de inverter que um gradiente; a **atualização máxima** corta
  as grandes, e o **ruído** torna qualquer uma ainda mais difícil — com um preço: com dois laboratórios, ruído 0,01
  custou cerca de 1 ponto de acerto, 0,02 seis, 0,05 quinze (o ensaio abaixo). Isto **não é uma garantia formal de
  privacidade diferencial** por ponto (isso exige corte por ponto e uma contabilidade de privacidade, Abadi et al.
  2016), e o coordenador vê a atualização de cada laboratório (a agregação segura, Bonawitz et al. 2017, não foi
  implementada). Escolha um coordenador em quem todos os laboratórios confiem.

**O ensaio (ILLUSTRATIVE).** Dois laboratórios inventados, cada um com três lâminas contadas de cerca de 260 pontos,
seu próprio tom de cor e a maior parte de um constituinte sem contar (A quase não contou feldspato, B quase não contou
cimento); 20 rodadas de 2 passadas; acertos em lâminas nunca vistas (média de três repetições,
`tools/bench_federated.py`):

| Modelo | Lab A | Lab B | Lab C (não participou) |
|---|---|---|---|
| Federado | 80 % | 83 % | 83 % |
| Todos os pontos juntos (só possível com dados inventados) | 81 % | 84 % | 86 % |
| Só o Lab A | 76 % | 74 % | 79 % |
| Só o Lab B | 76 % | 78 % | 79 % |

Uma contagem nova no Lab C com o modelo compartilhado: 83 % das propostas certas desde o primeiro ponto; sem ele,
nenhuma proposta antes de 15 pontos, 42 % aos 15, 71 % aos 30, 79 % aos 60 (e 83 % aos 60 com os dois).

## Por script

```python
rf.federation_create("arenitos-r1.rffed", "Arenitos", rounds=20)               # o coordenador
r = prj.federated_update("arenitos-r1.rffed", "lab-a.rfupd", site="Lab A")       # cada laboratório
r["fields"]                                   # todos os campos do arquivo que sairia
r["by_class"]                                 # o que fica: pontos por constituinte
rf.federation_aggregate("arenitos-r1.rffed", ["lab-a.rfupd", "lab-b.rfupd"], "arenitos-r2.rffed")
rf.federation("arenitos-r2.rffed")["history"]
prj["ILL-TS-002"].assist(top=5, shared="arenitos-r2.rffed")    # propostas com o modelo compartilhado
```

O módulo `rockface.core.federated` tem as partes: `create`, `site_data`, `site_update`, `inspect`, `check_update`,
`aggregate`, `simulate`, `centralized`, `local_only`.

## Limites e problemas comuns

* O modelo é tão bom quanto as contagens por trás dele: um constituinte que ninguém conta nunca é proposto, e um
  contado com nomes diferentes em dois laboratórios o confunde. As classes são os constituintes da base de
  conhecimento.
* Rochas muito diferentes (uma federação de carbonatos e uma contagem de arenito) dão propostas fracas; a coluna
  *Acertos antes* do histórico mostra como o modelo compartilhado se sai nos pontos de cada laboratório antes de
  aprender com eles.
* Uma contagem sem imagem, ou sem a imagem com nicóis cruzados quando a federação pede, fica de fora.
* "Só N pontos podem ensinar o modelo": marque mais contagens ou conte mais pontos.
* As propostas do modelo compartilhado são propostas: o petrógrafo conta, e Enter só aceita o que ele vê.
* *Patentes.* O Google tem patentes de aprendizado federado (p. ex. US 10,402,469 B2, US 11,120,102 B2,
  US 10,657,461 B2). O RockFace faz a média de atualizações trocadas como arquivos e não usa atualizações comprimidas
  ou esboçadas nem otimizador adaptativo no servidor; é uma nota de projeto, não um parecer jurídico
  (`docs/LICENSE_AUDIT.md`).

## Cobertura

O8 (pedido do proprietário de 2026-11-17: as inovações, a sexta).

Referências: McMahan et al. (2017), Communication-efficient learning of deep networks from decentralized data,
AISTATS, arXiv:1602.05629; Li et al. (2020), Federated optimization in heterogeneous networks (FedProx), MLSys,
arXiv:1812.06127; Li et al. (2021), FedBN, ICLR, arXiv:2102.07623; McMahan et al. (2018), Learning differentially
private recurrent language models, ICLR, arXiv:1710.06963; Abadi et al. (2016), Deep learning with differential
privacy, CCS, https://doi.org/10.1145/2976749.2978318; Zhu, Liu & Han (2019), Deep leakage from gradients, NeurIPS,
arXiv:1906.08935; Shokri et al. (2017), Membership inference attacks, IEEE S&P,
https://doi.org/10.1109/SP.2017.41; Bonawitz et al. (2017), Practical secure aggregation, CCS,
https://doi.org/10.1145/3133956.3133982; Kairouz et al. (2021), Advances and open problems in federated learning,
https://doi.org/10.1561/2200000083; Chang et al. (2024), Federated learning test for collaborative machine
learning, SCA2024-1036; RahimiZadeh et al. (2025), FTA-FTL: federated transfer learning for lithology microscopic
images, arXiv:2501.03349.

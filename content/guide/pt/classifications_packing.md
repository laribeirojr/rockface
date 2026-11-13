# McBride, Bramkamp & Powers e as classes de empacotamento

## Para que serve

Três classificações que os programas de referência oferecem e que o RockFace agora tem, cada uma com a sua fonte
publicada: **McBride (1963)** para arenitos, **Bramkamp & Powers (1958)** para carbonatos — com o símbolo de rocha-
reservatório (por exemplo *21BD*) — e as **classes de empacotamento** frouxo, normal e fechado da proximidade de
empacotamento de Kahn (1956).

## Antes de começar

* Uma descrição com a composição (Petro → Composição).
* Para Bramkamp & Powers: os dados carbonáticos que a composição não dá (abaixo).
* Para a classe de empacotamento: os contatos dos grãos contados numa travessia, ou os tipos de contato em %.

## Passo a passo

1. **Petro → aba Classificação.** McBride aparece ao lado de Folk (1980), com o campo atual e o original;
   **Diagrama…** desenha o triângulo.
2. Numa rocha carbonática, preencha os **dados carbonáticos** no canto inferior direito:
   * *Textura original (Bramkamp & Powers)*: não alterada visivelmente, moderadamente alterada, fortemente alterada
     (ainda reconhecível) ou obliterada;
   * *Porosidade visual*: A porosa ou pouco cimentada, B compacta, C densa;
   * *Alterada por*: pela dolomita (padrão), anidrita (A), sílica (S) ou mudanças pouco compreendidas (X);
   * *Fácies*, *Grupo* e *Dolomita %* vêm da composição e podem ser trocados;
   * *Tipo especial de rocha*: 14AX/14BX, 31BX ou 51BX quando os vazios substituem grãos.
3. A linha *Carbonatos — Bramkamp & Powers (1958)* mostra o nome, a fácies e o símbolo; **Possibilidades…** lista as
   28 classes com os critérios.
4. **Petro → aba Microscópica → Contatos e empacotamento.** Digite os contatos grão–grão e o total de uma travessia,
   ou os tipos de contato com as %: a proximidade e a classe aparecem na hora. **Ajuda de empacotamento…** mostra três
   empacotamentos ILUSTRATIVOS, um por classe, cada um com a sua proximidade contada.

## Opções

| Campo | Valores |
|---|---|
| Polos de McBride | Q = quartzo, quartzito e chert; F = feldspatos; R = outros fragmentos de rocha (incluídos os plutônicos e os carbonáticos) |
| Grupo de Bramkamp & Powers | 1 calcário fino, 2 calcário calcarenítico, 3 calcarenito, 5 carbonato clástico grosso; 4 dolomito cristalino (obliterado) |
| Símbolo | grupo · grau (1 moderado, 2 forte, 3 reliquiar) · porosidade (A, B, C) · alteração (R, D, A, S, X) |
| Classes de empacotamento | frouxo P < 40 %, normal 40–55 % (os dois limites incluídos), fechado P > 55 % |

## Como funciona

* **McBride (1963)** usa os limites de Folk (1954): quartzarenito acima de 95 % de Q; as linhas F = 25 % e R = 25 %
  saem dos pontos de 75 % dos lados, e F = 10 %, R = 10 % dos pontos de 10 % da base; subarcósio lítico onde F e R
  estão ambos entre 10 e 25 %; F:R = 1:1 divide o resto (McBride 1963, fig. 1 e p. 666–667).
* **Bramkamp & Powers (1958)**: grupo 1 quando os fragmentos carbonáticos clásticos do tamanho areia ou maiores são
  menos de 10 %; grupo 2 acima disso com pelo menos 10 % da matriz fina original; grupos 3 e 5 com menos de 10 % de
  matriz, separados pelos fragmentos maiores que areia. As colunas de alteração da Tabela 2: < 10 % de dolomita
  recristalizado, > 10 % de dolomita porfiroblástica (moderado), 10–75 % dolomítico e > 75 % reliquiar (forte);
  obliterado é o grupo 4. A fácies: impura com argila e silte, arenosa com grãos detríticos (a partir de 1 % dos
  sólidos). As porcentagens são dos sólidos.
* **Empacotamento**: proximidade de Kahn P = contatos grão–grão ÷ todos os contatos dos grãos cruzados × 100
  (Kahn 1956); sem contagem, a mesma razão pelos tipos de contato (todos menos "flutuante"). Os limites das classes
  são os de Bocardi (2005, p. 31) e Menezes Filho (2015, p. 40). As figuras da ajuda são calculadas pelo RockFace:
  um empacotamento de grãos redondos cujos raios crescem até a proximidade, contada em travessias horizontais como
  Kahn descreve, cair na classe.

## Por script

```python
d = prj["ILL-TS-001"]
d.classify("mcbride1963", label=True)
c = prj["ILL-CB-001"]
c.carbonate.bp_texture, c.carbonate.bp_porosity = "moderate", "B"
c.save()
c.classify("bramkamp_powers1958", label=True), c.symbol()   # (…, '21BD')
d.packing()                                           # {'proximity': 62.0, 'density': …, 'class': 'tight'}
rf.packing_class(47)                                  # 'normal'
```

## Limites e problemas comuns

* McBride não diz onde ficam os fragmentos plutônicos grossos: o RockFace os conta como fragmentos de rocha (Folk
  1980 os conta como feldspato) e avisa ao lado do diagrama.
* A porosidade visual A/B/C de Bramkamp & Powers não tem números no artigo: escolha pelos critérios deles (a dica do
  campo os resume). Enquanto não for escolhida, o símbolo mostra "?".
* Bramkamp & Powers vale quando os carbonatos são mais da metade dos sólidos.

## Cobertura

P14 (classes de empacotamento e ajuda visual), P29 e M3 (McBride), P32 (Bramkamp & Powers).

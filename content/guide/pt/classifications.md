# Classificações e diagramas ternários

## Para que serve

A aba **Classificação** dá nome à rocha: arenitos por Folk (1980) e McBride (1963), proveniência por Dickinson (QtFL
e QmFLt), textura pelas classes cascalho–areia–lama de Folk, carbonatos por Dunham, Embry & Klovan, Wright, Grabau e
Bramkamp & Powers. Cada classificação é calculada a partir da composição, sobre a composição atual e a original, e as
ternárias são desenhadas numa janela de diagrama. Um projeto pode acrescentar as suas próprias classificações
ternárias.

## Antes de começar

* Uma descrição com a sua composição (e, para a textura, as % de cascalho, areia e lama da aba Microscópica).
* Para carbonatos: os dados de rochas carbonáticas que a composição não dá (abaixo).

## Passo a passo

### Ler as classificações

1. Abra a aba **Classificação**. **Classificações** lista cada classificação com o seu resultado **Atual** e
   **Original**.
2. "sem dados" quer dizer que a composição não tem o que a classificação precisa; "fora dos campos", que o ponto cai
   fora de todos os campos; "Perto do limite com: …", que ele fica dentro da tolerância de outro campo.
3. **Observações** — uma nota sobre a classificação.

### O diagrama ternário

1. Selecione uma classificação ternária e clique em **Diagrama…**.
2. A janela **Diagrama ternário** mostra os campos, o ponto da descrição e, com **Ponto original**, o ponto da
   composição original.
3. **Valores (% dos três polos)** dá cada **Polo** e o **Resultado**; **Sob o cursor** nomeia o campo sob o mouse.
4. **Ajustar**, **Aproximar**, **Afastar**; **Tamanho do ponto**; **Cores** (campos coloridos ou não); **Nomes** (nomes
   dos campos ligados ou desligados).
5. **Exportar imagem…** grava o diagrama em PNG ou SVG.

### Rochas carbonáticas

1. Quando os carbonatos passam de metade dos sólidos, preencha **Rochas carbonáticas: o que a composição não
   indica**:
   * **Suporte da trama** (como na aba Microscópica, ou definido aqui); **Ligada organicamente na deposição** (não;
     sim, modo desconhecido; organismos anteparos; organismos incrustantes que ligam; arcabouço rígido);
   * **Grãos maiores que 2 mm (% dos grãos)** e o seu suporte;
   * **Contatos microestilolíticos**, **O cimento é o componente principal**, **A diagênese obliterou a trama**;
   * **Tamanho de cristal (µm)** e a granulometria dominante (mm);
   * os dados de Bramkamp & Powers (página [McBride, Bramkamp & Powers e as classes de empacotamento](classifications_packing.md)).
2. **Possibilidades…** lista todas as classes da classificação selecionada com os seus critérios, marcando a
   encontrada. **Falta: …** nomeia os dados que ainda faltam.

### Uma classificação do projeto

1. **Gerenciar classificações…** (na aba ou na janela do diagrama) abre **Classificações ternárias do projeto**.
2. **Nova**; dê o **Código** e o nome.
3. **Polos**: três polos, cada um com um **Símbolo** e os **Totais somados** (códigos de totais separados por
   vírgulas).
4. **Campos**: **Adicionar campo**, o seu nome e os seus **Vértices** — três porcentagens por vértice na ordem dos
   polos, vértices separados por ponto e vírgula (por exemplo `100 0 0; 50 50 0; 50 0 50`).
5. **Aplicar**. A classificação aparece em todas as descrições do projeto, nos grupos do Explorer e nas figuras.

## Opções

| Classificação | Dados |
|---|---|
| Folk (1980), McBride (1963) — QFR | quartzo, feldspatos e fragmentos de rocha da composição |
| Dickinson QtFL, QmFLt | supõe a contagem Gazzi–Dickinson; fragmentos plutônicos não são plotados |
| Folk (1954) cascalho–areia–lama | % de cascalho, areia e lama da aba Microscópica |
| Dunham (1962), Embry & Klovan (1971) | suporte, grãos, lama, ligação orgânica, grãos > 2 mm |
| Wright (1992) | também cimento, microestilolitos, obliteração, tamanho de cristal |
| Grabau (1904) | granulometria dominante dos grãos carbonáticos |
| Bramkamp & Powers (1958) | grupo, textura, porosidade, alteração, dolomita |

## Como funciona

* Um ponto ternário são os totais dos três polos normalizados para 100; o campo é encontrado pelo ponto-em-polígono
  sobre os limites publicados (Folk 1980; McBride 1963; Dickinson et al. 1983 e Dickinson 1985).
* Os subcampos do orógeno reciclado do QmFLt vêm de uma única digitalização da figura publicada e estão marcados
  "Limites a conferir com a figura original."
* As classes de carbonatos seguem os critérios dos seus artigos, mostrados em **Possibilidades…**. Elas se aplicam
  quando os carbonatos passam de 50 % dos sólidos ("Os carbonatos são … % dos sólidos; as classificações de
  carbonatos se aplicam acima de 50 %").

## Por script

```python
d = prj["TS-9"]
print(d.classify("folk1980", label=True), d.point("folk1980"))
print(d.classify("dunham1962"), d.classify("folk1980", original=True))
d.carbonate.support = "grain_supported"               # dados de carbonatos, depois salvar
d.save()
rf.ternary_figure("qtfl.svg", "dickinson_qtfl", [d], original=False)   # várias descrições podem ser dadas
```

## Limites e problemas comuns

* "sem dados": faltam à composição os polos (nenhum feldspato e nenhum fragmento ainda é um ponto; nenhum grão do
  arcabouço não é).
* Campos personalizados com vértices que não somam 100: "Vértices não entendidos".
* Uma classificação do projeto com um código já usado é recusada.

## Cobertura

P29 (classificações siliciclásticas, atual e original), P30 (proveniência de Dickinson), P31 (janela do diagrama
ternário), P32 (classificações de carbonatos e a tabela de possibilidades), M3 (classificações recalculadas com os
dados mais recentes).

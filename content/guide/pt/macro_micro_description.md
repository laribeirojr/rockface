# Descrição macroscópica e microscópica

## Para que serve

A aba **Macroscópica** registra o que se vê na amostra de mão ou no testemunho: estruturas, textura, cor e trama. A
aba **Microscópica** registra o que se vê na lâmina: estruturas, o intervalo granulométrico e as suas modas,
seleção, forma dos grãos, trama, os contatos intergranulares e o empacotamento. O RockFace confere cada valor com a
sua escala, e assim o texto e os números de uma descrição nunca discordam.

## Antes de começar

Uma descrição aberta (página [Projetos e descrições](projects_descriptions.md)). As listas vêm da base de conhecimento (página
[Nomenclatura, escalas e referências (a base de conhecimento)](nomenclature_knowledge_base.md)).

## Passo a passo

### Macroscópica

1. Abra a aba **Macroscópica**.
2. **Estruturas** — até três (**Estrutura 1–3**), cada uma com a sua **Extensão (%)** na amostra.
3. **Textura** — **Granulometria modal** (Udden–Wentworth), **Tamanho de cristal** (Folk 1962, para rochas
   cristalinas), **Seleção**, **Arredondamento** (Powers) e **Esfericidade**.
4. **Cor** — o **Código Munsell** (por exemplo `5YR 6/4` ou `N7`) e o **Nome da cor**.
5. **Trama** — **Orientação** e **Suporte**.
6. **Notas** e depois **Salvar** (Ctrl+S).

### Microscópica

1. Abra a aba **Microscópica**.
2. **Estruturas** — até três, com a sua extensão.
3. **Granulometria**
   * **Intervalo granulométrico**: a classe **Mais fino** e a **Mais grosso**.
   * **Modas**: a **Moda principal** e até mais três (**Segunda**, **Terceira**, **Quarta moda**), cada uma como
     classe ou como tamanho em **mm**. Quando um tamanho é digitado, a sua classe é preenchida.
   * **Cascalho (%)**, **Areia (%)** e **Lama (%)**, com o total mostrado ao lado.
4. **Seleção e forma dos grãos** — **Seleção** como classe ou como **σI (φ)** (Folk & Ward 1957); **Arredondamento**,
   o **Intervalo de arredondamento** e os **Modificadores de arredondamento**; **Esfericidade**; **Tamanho de
   cristal**; **Orientação** e **Suporte**.
5. **Contatos e empacotamento**
   * **Contatos, do mais abundante (%)** — até cinco tipos de contato (pontual, longo, côncavo-convexo, suturado,
     flutuante) com a sua porcentagem.
   * Para o empacotamento de Kahn (1956): conte, ao longo de uma travessia, **Todos os contatos da travessia** dos
     grãos atravessados e quantos são **Contatos grão–grão**; o RockFace mostra a **Proximidade de empacotamento
     (Kahn)** e a sua classe (frouxo, normal, fechado). Meça os **Interceptos de grãos (mm)** e o **Comprimento da
     travessia (mm)** para a **Densidade de empacotamento (Kahn)**.
   * **Ajuda de empacotamento…** abre a ajuda visual das classes de empacotamento (página
     [McBride, Bramkamp & Powers e as classes de empacotamento](classifications_packing.md)).
6. **Notas** e depois **Salvar**.

## Opções

| Campo | Regra |
|---|---|
| Estruturas | No máximo três, sem repetir; uma extensão precisa de uma estrutura; 0–100 %. |
| Modas | No máximo quatro; a moda principal primeiro; cada uma dentro do intervalo granulométrico. |
| Intervalo granulométrico | O extremo mais fino primeiro. |
| σI (φ), tamanhos modais | Um número prevalece sobre a classe: quando discordam, a classe é atualizada, com uma mensagem. |
| Cascalho + areia + lama | Deve somar 100 % (salvo mesmo assim, com um aviso). |
| Contatos | No máximo cinco, sem repetir, somando no máximo 100 %. |
| Contatos grão–grão | Não mais que todos os contatos. |

## Como funciona

* A granulometria segue a escala de Udden–Wentworth (Wentworth 1922) com o φ de Krumbein (1934); a seleção, o desvio
  padrão gráfico inclusivo de Folk & Ward (1957); o arredondamento, as classes de Powers (1953); o tamanho de
  cristal, Folk (1962).
* "O número prevalece": um valor em milímetros ou em φ é a medida, e a classe é derivada dele.
* Proximidade de empacotamento P = contatos grão–grão ÷ todos os contatos × 100; densidade de empacotamento =
  intercepto total dos grãos ÷ comprimento da travessia × 100 (Kahn 1956). Classes: frouxo abaixo de 40, normal de
  40 a 55, fechado acima de 55.

## Por script

```python
d = prj["TS-9"]
d.micro.sorting_phi = 0.62               # σI de Folk & Ward; a classe acompanha ao salvar
d.micro.grain_contacts, d.micro.total_contacts = 38, 80
print(d.micro.packing_proximity, d.micro.packing_class)       # 47.5 normal
d.macro.colour_code = "5Y 7/2"
d.save()                                 # conferido exatamente como nos formulários
```

## Limites e problemas comuns

* "“…” não está em notação Munsell (por exemplo 5YR 6/4 ou N7)."
* "Intervalo granulométrico: o primeiro extremo é maior que o segundo."
* "Foram dadas modas secundárias sem a moda principal." / "… está fora do intervalo indicado."
* "Granulometria modal: 0,3 corresponde a areia média; o número prevalece e a classe foi atualizada." — uma mensagem,
  não um erro.

## Cobertura

P11 (descrição macroscópica), P12 (estruturas e granulometria microscópicas), P13 (seleção e forma), P14 (contatos e
empacotamento).

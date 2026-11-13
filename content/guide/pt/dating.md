# Datação U-Pb no diagrama de Tera-Wasserburg

## Para que serve

Os pontos U-Pb de um mineral diagenético (um cimento de calcita, uma dolomita) medidos em várias amostras são datados
juntos: o RockFace Explorer os plota no **diagrama de Tera-Wasserburg**, ajusta a reta da regressão de York e dá a
idade no seu intercepto inferior com a concórdia, com a sua incerteza, o MSWD e a probabilidade do ajuste. A idade fica
no projeto com a fase que ela data, e é posicionada na evolução paragenética e na coluna estratigráfica.

## Antes de começar

* Análises pontuais U-Pb nas lâminas (página [Análises pontuais: geoquímica, datação e inclusões fluidas](spot_analyses.md)): tipo *datação* (ou sistema "U-Pb") com ²³⁸U/²⁰⁶Pb e
  ²⁰⁷Pb/²⁰⁶Pb, as suas incertezas e a correlação dos erros (rho).
* Uma consulta no Explorer que encontre as amostras a datar juntas (por exemplo, uma formação).

## Passo a passo

1. No RockFace Explorer, abra a aba **Datação U-Pb**.
2. **Descrições com pontos U-Pb (da consulta)** lista as amostras encontradas que têm pontos U-Pb.
3. **Mineral datado**: o constituinte (ou grupo) cujos pontos são usados, ou **Todos os minerais**.
4. **Regressão**:
   * **Livre (York)** — a reta pelos pontos;
   * **Ancorada no Pb comum de Stacey & Kramers (1975)** — o ²⁰⁷Pb/²⁰⁶Pb inicial do modelo na idade encontrada;
   * **Ancorada num ²⁰⁷Pb/²⁰⁶Pb inicial dado** — digite o **²⁰⁷Pb/²⁰⁶Pb inicial** e o **Erro da âncora**.
5. A tabela lista todos os pontos; desmarque **Ponto (usado)** para tirar um ponto da regressão (ele fica no diagrama,
   marcado).
6. O diagrama mostra os pontos com as suas elipses de erro, a concórdia com as suas idades, a reta da regressão e o
   resultado: "Idade = … ± … Ma (2σ)", "± … Ma (conf. 95 %)", o MSWD, n e o ²⁰⁷Pb/²⁰⁶Pb inicial.
7. **Exportar diagrama…** o grava (PNG, SVG, PDF).
8. **Salvar idade…**: dê um nome; ela fica com a fase que data (mineral e hábito). **Idades do projeto (clique duplo
   abre)** lista as idades salvas; **Excluir idade**.

## Opções

| Opção | O que muda |
|---|---|
| Mineral datado | Quais pontos são usados. |
| Regressão | Livre, ancorada no chumbo comum de Stacey & Kramers, ou ancorada num valor dado com o seu erro. |
| Ponto (usado) | Tira um ponto anômalo do ajuste. |

## Como funciona

* Regressão de York com erros correlacionados nas duas coordenadas (York et al. 2004); a idade é o intercepto
  inferior da reta com a concórdia de Tera-Wasserburg (constantes de decaimento de Jaffey et al. 1971, ²³⁸U/²³⁵U de
  Hiess et al. 2012). O ajuste ancorado força a reta pelo ²⁰⁷Pb/²⁰⁶Pb inicial (Stacey & Kramers 1975, ou o valor
  dado).
* A incerteza é dada em 2σ (analítica) e como intervalo de 95 %: t(n−2) × σ × √MSWD quando MSWD > 1, senão 1,96σ
  (Ludwig 2003); os erros das constantes de decaimento não entram. MSWD = χ²/(n − 2) (Wendt & Carl 1991), com a
  probabilidade do ajuste.
* Conferido com valores publicados: os dados de Pearson com os pesos de York dão a inclinação, o intercepto e os erros
  publicados; em 800 conjuntos sintéticos o intervalo de 95 % contém a idade verdadeira em 97,2 % (livre) e 97,5 %
  (ancorada) das vezes.

## Por script

```python
d = prj.date(formation="Example Formation", constituent="calcite_dia", anchor="stacey_kramers", figure="tw.pdf")
print(f"{d.age:.1f} ± {d.age_2s:.1f} Ma (2σ), MSWD {d.mswd:.2f}, n = {d.n}")
prj.save_age("Calcita do arenito", ("identification", "formation", "Example Formation"),
             constituent="calcite_dia", habit="poikilotopic", anchor="stacey_kramers")
print(prj.ages())
```

## Limites e problemas comuns

* "Sem idade: …" — poucos pontos, ou "A reta não corta a concórdia."
* "Nenhuma idade a salvar: date pontos primeiro."
* Pontos sem rho são tomados como não correlacionados (rho = 0).

## Cobertura

L12 (datação U-Pb, Tera-Wasserburg; idades na estratigrafia).

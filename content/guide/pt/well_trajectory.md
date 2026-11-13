# Trajetória do poço

## Para que serve

Num poço desviado, a amostra está numa profundidade medida (MD) que não é a sua profundidade vertical (TVD), nem fica
logo abaixo da cabeça do poço. **Trajetória do poço** lê o levantamento direcional e dá a cada amostra a TVD, a
profundidade abaixo do nível do mar, os afastamentos norte e leste, e a latitude e longitude.

## Antes de começar

* O poço no projeto (Identificação), com latitude e longitude da cabeça para a posição geográfica.
* Um arquivo de levantamento: profundidade medida, inclinação e azimute (CSV, texto ou LAS).

## Passo a passo

1. **Petro → Início → Trajetória do poço…**
2. Escolha o poço; digite a elevação do datum de profundidade acima do nível do mar e a referência do norte.
3. **Ler um levantamento…** e escolha o arquivo. As estações aparecem com TVD, norte, leste e severidade do dogleg.
4. **Amostras**: cada amostra do poço na trajetória. **Planta e seção**: a vista em planta e a seção vertical, com as
   amostras em vermelho.

## Opções

| Campo | Significado |
|---|---|
| Datum de profundidade | elevação do datum (mesa rotativa, kelly bushing) acima do nível do mar: TVDSS = TVD − datum |
| Referência do norte | verdadeiro, de quadrícula ou magnético, como o levantamento dá os azimutes (registrado, não convertido) |
| Colunas | MD / Depth / Prof., Inc / Incl / Devi, Azi / Azim / Hazi, em qualquer ordem; vírgula, ponto e vírgula, tabulação ou espaços |

## Como funciona

Mínima curvatura (Bourgoyne et al. 1986; Sawaryn & Thorogood 2005): entre duas estações o poço segue o arco de um
círculo; ΔN, ΔE e ΔTVD são as meias somas dos cossenos diretores vezes ΔMD, vezes o fator RF = (2/β)·tan(β/2), β o
dogleg. Uma amostra entre estações fica no mesmo arco. Latitude e longitude saem da cabeça pelos raios de curvatura
do WGS 84 (plano tangente local).

## Por script

```python
st = prj.survey("ILL-WELL-1", "levantamento.csv", datum_elevation_m=25.0)
st[-1].tvd, st[-1].north, st[-1].east
rf.trajectory.sample_position(prj.raw, sample_id)     # {'tvd': …, 'tvdss': …, 'latitude': …, …}
```

## Limites e problemas comuns

* Acima da primeira estação o poço é tomado como vertical; abaixo da última, mantém a última direção (marcado como
  *extrapolado*).
* Azimutes magnéticos não são corrigidos pela declinação: converta antes ou escolha a referência certa.

## Cobertura

P8 (localização da amostra: posição geográfica, profundidade e trajetória do poço).

# Sistema poroso

## Para que serve

A aba **Sistema poroso** registra a porosidade visual da lâmina e os tipos de poro que a compõem, cada um com a sua
fração, tamanho e modificador. Os tipos de poro são os de Choquette & Pray (1970) para carbonatos e os das
classificações de poros de arenitos, vindos da base de conhecimento.

## Antes de começar

Uma descrição aberta. A porosidade da resina azul medida numa imagem (RockFace Lab) ou os pontos contados (aba
Contagem de pontos) podem servir de porosidade visual.

## Passo a passo

1. Abra a aba **Sistema poroso**.
2. **Porosidade** — digite a **Porosidade visual (%)**. A soma dos tipos é mostrada ao lado.
3. **Tipos de poro** — até oito linhas. Para cada uma:
   * **Tipo** — os poros seletivos de trama de Choquette & Pray (interpartícula, intrapartícula, intercristalino,
     móldico, fenestral, de abrigo, de arcabouço de crescimento), os não seletivos de trama (fratura, canal, vugue,
     caverna) e os que podem ser uma coisa ou outra (brecha, perfuração, escavação, contração), e os poros de
     arenitos (intergranular primário e secundário, dissolução intragranular, agigantado, microporosidade);
   * **%** — a sua fração do volume da rocha;
   * **mm** — um tamanho típico, ou a classe de **Tamanho de poro** (a classe acompanha um tamanho digitado);
   * **Modificador** — um modificador da base de conhecimento que se aplica a poros.
4. **Notas** e depois **Salvar** (Ctrl+S).

## Opções

| Campo | Regra |
|---|---|
| Porosidade visual | 0–100 %. |
| Tipos de poro | No máximo oito, sem repetir; cada um 0–100 %. |
| Soma dos tipos | Comparada com a porosidade visual: mais ou menos que ela gera um aviso. |

## Como funciona

Os tipos de poro e os seus modificadores são termos do RockFace vindos da literatura publicada (Choquette & Pray 1970
para carbonatos; os tipos de poro de arenitos segundo Schmidt & McDonald 1979 e Pettijohn et al. 1987). As classes
de tamanho de poro são os microporos (< 1/16 mm), mesoporos pequenos e grandes (até 4 mm) e megaporos pequenos e
grandes (até 256 mm) de Choquette & Pray. Os tipos de poro contados como pontos na composição (tipo *poro*) são um
registro à parte: o Sistema poroso é a síntese do petrógrafo.

## Por script

```python
from rockface.core import texture as tx
d = prj["TS-9"]
d.pores.total_porosity = 18.0
d.pores.pores = [tx.Pore("interparticle", 12.0, size_mm=0.15), tx.Pore("moldic", 6.0)]
d.save()
```

## Limites e problemas comuns

* "Os tipos de poro somam … %, mais que a porosidade visual (… %)." — um aviso: confira as frações.
* "… deve estar entre 0 e 100 %."
* Um código de tipo de poro ou de modificador desconhecido (de um script ou de um arquivo antigo) é recusado com
  "Valor desconhecido …".

## Cobertura

P17 (descrição do sistema poroso).

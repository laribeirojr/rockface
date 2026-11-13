# RockFace Lab: registro e a calculadora de imagens

## Para que serve

O **Registro** alinha uma imagem de uma lâmina sobre outra — a imagem de nicóis cruzados sobre a de luz polarizada
plana, uma imagem de catodoluminescência, um segundo escaneamento — por pares de pontos e/ou automaticamente, e a grava
na malha de pixels da imagem fixa, para que as duas possam ser usadas juntas pixel a pixel. A **Calculadora** combina as
imagens de uma lâmina com uma fórmula, pixel a pixel: uma máscara dos pixels escuros do XP, a diferença de duas luzes,
um limiar do matiz.

## Antes de começar

Duas imagens da mesma lâmina no RockFace Lab (página [RockFace Lab: recorte, filtros e a máscara da amostra](lab_preparation.md)).

## Passo a passo

### Registro

1. Abra a aba **Registro**.
2. **Imagem fixa** (normalmente a PP) e **Imagem móvel** (XP, CL…).
3. **Transformação**: **translação**, **similaridade (giro, escala, translação)**, **afim** ou **spline de placa
   fina**.
4. Ou:
   * **Pares de pontos…** — clique um ponto na imagem fixa (esquerda) e depois o mesmo ponto na móvel (direita); o
     ajuste é feito a cada par, com o **Resíduo** de cada um e "RMS … px, deixando um de fora … px"; **Remover par**,
     **Remover todos**; ou
   * **Automático** — a correlação dos contornos dos grãos (ECC), partindo do referencial das lâminas ou dos pares.
     **Busca (automática)**: a partir do referencial, **translação**, **qualquer giro** ou **giro e escala**.
5. O resultado: "…: giro …°, escala …, translação … px", a correlação dos contornos, os erros dos pares.
6. Confira: **Móvel sobre fixa** mistura as duas; **Piscar** alterna entre elas.
7. **Salvar o registro** o guarda na imagem móvel; **Gravar na malha da imagem fixa** grava a imagem móvel reamostrada
   pixel a pixel sobre a fixa ("Imagem adicionada na malha fixa: …").

### Calculadora

1. Abra a aba **Calculadora**. As imagens da lâmina são listadas; clique duas vezes num nome para inseri-lo.
2. Escreva a **Fórmula**, com `{nome da imagem}` e um canal: `.r .g .b`, `.l` (luminância), `.h .s .v`. Exemplos:
   * `{XP}.l < 40` — os pixels escuros do XP (uma máscara);
   * `({PP}.v − {XP}.v)/2 + 128` — uma imagem em cinza;
   * `where({PP}.h > 190, 255, 0)`.
   Números, `+ − * / **`, comparações, `& | ~`, e `abs sqrt log log10 exp min max where clip round`.
3. **Imagem de referência** — a malha do resultado (as outras imagens são tomadas sobre ela por meio dos seus
   registros).
4. **Resultado**: **pela fórmula** (uma comparação dá uma máscara, um número dá uma imagem em cinza), **máscara** ou
   **imagem em cinza**. **Esticar os valores** com o **Valor em preto** e o **Valor em branco**.
5. **Nome do resultado** e depois **Calcular**. "Usa: …" lista as imagens usadas. "Resultado adicionado: …".

## Opções

| Opção | O que muda |
|---|---|
| Transformação | Translação, similaridade, afim (≥ 3 pares) ou spline de placa fina (não linear, muitos pares). |
| Busca (automática) | Até onde a busca automática vai: nenhuma, translação, qualquer giro, giro e escala. |
| Resultado | Máscara (um mapa de 0/1) ou imagem em cinza. |

## Como funciona

* Os ajustes de pares de pontos são de mínimos quadrados; o erro deixando um de fora prevê cada par pelos outros. O
  registro automático maximiza o coeficiente de correlação melhorado (ECC) dos contornos dos grãos, depois de uma busca
  de translação, giro e escala.
* Conferências: XP sobre PP recuperado dentro de 0,017 px para qualquer giro e ±8 % de escala; um escaneamento
  deslocado 6 px corrigido para 0,15 px; uma spline de placa fina a 0,06 px numa deformação não linear; em pares reais
  de lâminas, o deslocamento comum foi achado em 52 e 59 de 60 recortes.
* A calculadora trabalha bloco a bloco sobre a malha da imagem de referência.

## Por script

```python
pp_c, xp_c = prj.image("ILLUSTRATIVE mosaic PP (crop)"), prj.image("ILLUSTRATIVE mosaic XP (crop)")
t = xp_c.register_on(pp_c, search="rotation")            # automático, a partir do referencial das lâminas
print(t.rotation_deg, t.scale, t.ecc)
xp_on_pp = xp_c.resample_on(pp_c)                        # na malha da imagem PP
escuro = prj.calculate("{%s}.l < 60" % xp_on_pp.name, pp_c, name="escuro no XP")
print(escuro.areas_mm2())
```

## Limites e problemas comuns

* "Escolha duas imagens diferentes da lâmina."
* "N pares: são necessários pelo menos …." — 1 para uma translação, 2 para uma similaridade, 3 para uma transformação
  afim, 4 para uma spline de placa fina.
* O registro automático precisa de imagens com grãos em comum; em luzes muito diferentes (CL sobre PP), dê antes
  alguns pares de pontos.

## Cobertura

GT5 (registro PP ↔ XP com pares de pontos, registro automático), GT19 (Volume Calculator das "More tools").

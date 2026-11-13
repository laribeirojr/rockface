# RockFace Lab: recorte, filtros e a máscara da amostra

## Para que serve

O RockFace Lab prepara as imagens de uma lâmina para a análise. **Recortar** corta todas as imagens da lâmina no mesmo
retângulo, mantendo o seu lugar na lâmina. **Filtros** melhoram uma imagem — brilho e contraste, saturação, gama,
níveis, equalização do histograma, correção de sombreamento, suavização, nitidez — com pré-visualização. A **Máscara**
encontra a área útil da lâmina (a rocha, sem o vidro e as bordas) e a separa em fragmentos.

## Antes de começar

* Uma lâmina com imagens no RockFace Atlas (página [RockFace Atlas: lâminas inteiras, fotos de detalhe e a biblioteca de imagens](atlas_viewer.md)).
* Abra o Lab: **Início → Imagens → Lab** (Ctrl+Shift+L) no RockFace Petro, ou `rockface lab projeto.rockface`.

## Passo a passo

### A janela

* **Lâmina:** no alto escolhe a lâmina; **Imagens da lâmina** lista as suas imagens (as originais e as feitas pelo Lab,
  com o que as fez).
* O visualizador mostra a imagem selecionada: **Ajustar**, **1:1**, **Aproximar**, **Afastar**.
* As abas à direita: **Recortar**, **Filtros**, **Máscara**, **Registro**, **Calculadora**, **Segmentação**, **Edição e
  objetos**, **Medidas**, **Fluxos**, **IA**.

Cada ferramenta grava uma **nova imagem** da lâmina; a original nunca é alterada.

### Recortar

1. Abra **Recortar**. Dê o retângulo no sistema da lâmina: **Esquerda (mm)**, **Topo (mm)**, **Direita (mm)**, **Base
   (mm)**, ou:
   * **Desenhar na imagem** — arraste um retângulo;
   * **Imagem inteira**; **Caixa da máscara**;
   * um retângulo das **Regiões salvas** ou das **Últimas usadas**.
2. **Nome da região** e **Salvar região** o guardam para as próximas lâminas; **Excluir região**.
3. Em **Imagens a recortar**, marque as imagens (PP, XP, um mapa…). Cada uma é recortada na parte que cobre.
4. **Recortar as imagens marcadas**. "N imagem(ns) recortada(s) adicionada(s) à lâmina."

### Filtros

1. Abra **Filtros** e escolha a imagem.
2. **Adicionar** um filtro à lista:
   * **Brilho e contraste**, **Saturação**, **Gama**;
   * **Níveis automáticos** (**Percentil inferior** e **Percentil superior**, canais juntos ou cada um);
   * **Equalização do histograma**;
   * **Correção de sombreamento** (iluminação desigual: **Referência** resina, claro, tudo, máscara ou plana; **Grau
     da superfície**; **Ganho máximo**);
   * **Suavização gaussiana** (**Sigma (px)**), **Filtro de mediana** (**Tamanho (px)**), **Máscara de nitidez**
     (**Sigma**, **Intensidade**);
   * **Pintar fora da amostra** (com uma máscara em **Imagem** e o seu **Preenchimento**).
3. Os filtros rodam em ordem: **Subir**, **Descer**, **Remover**, **Desfazer**, **Refazer**. O visualizador mostra o
   resultado na hora; **Mostrar o original** compara.
4. **Nome da nova imagem** e depois **Gravar como nova imagem**. "Imagem filtrada adicionada: …".

### Máscara da amostra

1. Abra **Máscara**. A máscara é encontrada **pela cor (resina azul)** ou **por amostras desenhadas**: **Desenhar
   amostra de rocha** e **Desenhar amostra de resina** na imagem.
2. **Separar em fragmentos** pela resina entre eles: **Resina mais larga que**, **Manter os maiores** (N fragmentos,
   ou todos), **Suavização**, **Área mínima**.
3. **Encontrar a amostra**. "Amostra: …% da imagem, N fragmento(s)". "Não há vidro nem borda: a imagem inteira é a
   amostra." quando a imagem é toda rocha.
4. **Nome da máscara** e depois **Guardar a máscara**. A máscara é usada pelo Recorte (**Caixa da máscara**), por
   **Pintar fora da amostra**, pela segmentação e pelas medidas.

## Opções

| Opção | O que muda |
|---|---|
| Correção de sombreamento — Referência | O que deve ficar uniforme: a resina, as áreas claras, toda a imagem, uma máscara, ou uma imagem de campo plano. |
| Níveis automáticos — Canais | Esticar os três canais juntos (mantém as cores) ou cada um à parte. |
| Resina mais larga que | A menor faixa de resina que separa dois fragmentos (fração do lado menor). |

## Como funciona

* Brilho, contraste e saturação dão exatamente o que o ImageEnhance do Pillow dá, e a equalização do histograma da
  luminância exatamente o que o OpenCV dá (conferido em 26 imagens, 20 delas recortes de lâminas reais).
* Os filtros são aplicados bloco a bloco: uma lâmina inteira de qualquer tamanho é filtrada com pouca memória, e o
  resultado é o mesmo de filtrar a imagem inteira de uma vez.
* A correção de sombreamento ajusta uma superfície polinomial à referência (a resina, por padrão) e a divide: uma
  desigualdade de 0,086–0,130 voltou a 0,021 em lâminas de teste.
* A máscara encontra o vidro e as bordas pela cor e textura; em lâminas PP e XP coincidiu com a máscara verdadeira com
  IoU de 0,97–0,9996.

## Por script

```python
pp, xp = prj.image("ILLUSTRATIVE mosaic PP"), prj.image("ILLUSTRATIVE mosaic XP")
pp_c, xp_c = prj.crop([pp, xp], roi=(2.0, 2.0, 8.0, 6.0))          # mm do sistema da lâmina
melhor = pp_c.filter(["shading", ("brightness_contrast", {"contrast": 20}), ("unsharp", {"sigma": 1.5})])
mask = pp.sample_mask(split=True, n_largest=2)
print(mask.areas_mm2())
prj.save_roi("Centro", (2.0, 2.0, 8.0, 6.0))
```

## Limites e problemas comuns

* "Indique um retângulo para recortar." / "Marque pelo menos uma imagem."
* "A lâmina ainda não tem máscara (aba Máscara)."
* Numa lâmina sem resina azul, encontre a máscara **por amostras desenhadas**.

## Cobertura

GT3 (recorte), GT4 (filtros de realce), GT6 (área útil da amostra: fragmentos, manter os N maiores).

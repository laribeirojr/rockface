# Poços para LAS

## Para que serve

As descrições de um poço gravadas como um arquivo **LAS 2.0** — um por poço —, para que programas de modelagem de
reservatório como o Petrel, o Techlog ou o Geolog leiam a petrografia como curvas contra a profundidade: porosidade e
permeabilidade, totais, classificações, fácies… Os atributos de texto viram curvas discretas com as suas tabelas de
códigos.

## Antes de começar

* Descrições com um poço e uma profundidade.
* Opcional: uma consulta no Explorer, para gravar só as descrições encontradas.

## Passo a passo

1. No RockFace Explorer, **Exportar → Poços para LAS (Petrel)…**. O diálogo **Poços para LAS 2.0** se abre.
2. **Profundidade das amostras**: medida (topo), corrigida ou ajustada.
3. **Empresa** — escrita no cabeçalho.
4. **Só as N descrições encontradas pela consulta**, ou todas as descrições.
5. **Curvas (um valor por profundidade de amostra)**: marque os atributos a gravar (porosidade, permeabilidade,
   densidade de grão, totais, classificações, fácies, zona…). Cada um tem o seu mnemônico e unidade.
6. **Primeiro arquivo** mostra o começo do primeiro arquivo, para conferir.
7. **Gravar…** e escolha a pasta. "N arquivos LAS gravados em …".

## Opções

| Opção | O que muda |
|---|---|
| Profundidade das amostras | Qual profundidade da identificação é a curva DEPT. |
| Curvas | Curvas numéricas, ou curvas discretas para atributos de texto (códigos inteiros com a sua tabela). |

## Como funciona

* Um arquivo LAS 2.0 por poço, com passo de profundidade irregular (`STEP 0`) e `NULL -999.25`.
* Os atributos de texto (fácies, uma classificação) viram curvas discretas de códigos inteiros; a tabela de códigos
  vai nas seções Parameter e Other.
* Duas amostras na mesma profundidade são reunidas.
* Os arquivos foram conferidos com dois leitores independentes (lasio e o LASReader de W. Weckesser): todo valor é
  igual ao registro, os itens obrigatórios do cabeçalho estão presentes e o lasio não dá nenhum aviso.

## Por script

```python
prj.export_las("las", ("identification", "formation", "Example Carbonate Unit"),
               curves=["petrophysics.porosity", "petrophysics.permeability", rf.Curve("totals.qt", "QT", "%"),
                       "identification.facies"],
               depth="corrected_depth", company="ILLUSTRATIVE")
las = rf.las.read("las/ILLUSTRATIVE-A1.las")             # lê de volta um arquivo LAS 2.0
```

## Limites e problemas comuns

* "Nenhuma amostra com esta profundidade." — a profundidade escolhida está vazia nessas amostras (por exemplo, sem
  profundidade ajustada).
* As amostras sem poço ficam de fora.
* Para perfis de imagem e curvas do RockFace MC, veja [RockFace MC: perfis de imagem](mc_image_logs.md) (LAS, CSV, DLIS, NetCDF) e a exportação WITSML
  (página [Exportar poços para WITSML e amostras para o OSDU](exports.md)).

## Cobertura

P38 (exportação para LAS para programas de modelagem de reservatório), L4 (exportador de LAS para o Petrel).

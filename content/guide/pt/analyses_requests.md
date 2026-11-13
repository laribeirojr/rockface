# Análises e solicitações de análise

## Para que serve

A aba **Análises** guarda os resultados de laboratório da amostra — petrofísica, DRX, MEV, isótopos, química,
bioestratigrafia — com as suas imagens. A aba **Solicitações** pede ao laboratório novas análises e acompanha-as até
ficarem prontas. As duas pertencem à **amostra**: todas as descrições das lâminas da amostra as mostram.

## Antes de começar

Uma descrição **salva**: análises e solicitações pertencem à sua amostra ("Salve primeiro a descrição: análises e
solicitações pertencem à sua amostra.").

## Passo a passo

### Acrescentar uma análise

1. Abra a aba **Análises**. O seu título nomeia a amostra.
2. **Adicionar análise…**
3. Escolha a **Análise**: petrofísica convencional, petrofísica especial, DRX (rocha total ou fração argila), MEV
   (elétrons secundários ou retroespalhados), isótopos estáveis (C, O), isótopos de estrôncio, química ou
   bioestratigrafia.
4. Preencha o **Laboratório**, a **Data (aaaa-mm-dd)** e os resultados. Os campos seguem o tipo:
   * petrofísica convencional — **Porosidade** (%), **Permeabilidade** (mD), **Densidade de grão** (g/cm³);
   * isótopos estáveis — **δ13C** e **δ18O** (‰ VPDB); estrôncio — **87Sr/86Sr**;
   * DRX — uma tabela de **Mineral** e **%** (**Adicionar linha**, **Remover linha**);
   * química — uma tabela de **Elemento ou composto**, **Valor** e **Unidade**;
   * petrofísica especial — o **Método**; bioestratigrafia — **Biozona**, **Idade** e **Fósseis**;
   * **Notas** para o resto.
5. Em **Imagens e arquivos**, **Adicionar imagem…** (imagens de MEV, difratogramas, cromatogramas); **Exportar…**
   grava uma de volta num arquivo.
6. **OK**. A lista mostra o tipo, o laboratório, a data, um resumo dos resultados e o número de imagens. **Editar…**
   e **Excluir** agem sobre a análise selecionada.

### Solicitar uma análise

1. Abra a aba **Solicitações** e depois **Nova solicitação…**
2. Escolha a **Análise**. A **Dica** diz o que um bom objetivo informa para aquele tipo.
3. Escreva o **Objetivo** (obrigatório): que pergunta a análise deve responder.
4. **Situação**: Solicitada, Em andamento, Concluída ou Cancelada. Mude-a conforme o trabalho avança.
5. **Notas** e imagens (por exemplo, uma foto da área a amostrar), e depois **OK**.

A lista mostra o tipo, o objetivo, a situação, quando foi solicitada e por quem.

## Opções

| Campo | Regra |
|---|---|
| Data | aaaa-mm-dd, aaaa-mm ou aaaa. |
| Porosidade, permeabilidade, densidade de grão | 0–100 %, 0–100 000 mD, 1,5–5,0 g/cm³. |
| δ13C, δ18O | −50 a 50 ‰ VPDB; 87Sr/86Sr 0,69–0,80. |
| Linhas de DRX | Cada mineral com nome; as porcentagens devem somar 100 (salvo mesmo assim, com um aviso). |

## Como funciona

As análises e solicitações são guardadas com a amostra; assim, a porosidade de um plugue é digitada uma vez e
aparece em todas as descrições daquele plugue. Elas entram nos relatórios, nos arquivos de intercâmbio, nas consultas
do Explorer (petrofísica, isótopos, DRX) e no seu painel (porosidade × permeabilidade, densidade de grão). As imagens
ficam dentro do projeto. As análises de rotina de testemunho de um laudo de laboratório em PDF podem ser lidas para as
amostras de um poço pela profundidade (Início → **Importar laudo de laboratório (PDF)…**, página [Arquivos dos programas de referência](file_formats.md)).

## Por script

```python
d = prj["TS-9"]
d.add_analysis("conventional_petrophysics", laboratory="ILLUSTRATIVE lab", date="2026-03-02",
               values={"porosity": 18.2, "permeability": 245.0, "grain_density": 2.65})
d.add_analysis("xrd_whole_rock", rows=[{"mineral": "Quartzo", "percent": 71}, {"mineral": "Calcita", "percent": 29}],
               pictures=["drx.png"])
d.add_request("stable_isotopes", "δ13C e δ18O do cimento de calcita, para datar a água que o formou")
for a in d.analyses():
    print(a["kind"], a["values"], a["rows"])
print([r["status"] for r in d.requests()])
```

## Limites e problemas comuns

* "Escolha o tipo de análise." / "Indique o objetivo da solicitação."
* "… deve estar entre … e …": um valor fora do intervalo plausível do seu tipo.
* "A análise ainda não tem resultados." — um aviso: a análise é salva vazia.
* Imagens maiores que o limite de anexos do projeto são recusadas.

## Cobertura

P15 (análises adicionais), P16 (solicitações de análise com imagens).

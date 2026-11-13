# Exportar e importar descrições

## Para que serve

Um **arquivo de intercâmbio do RockFace** (`.rfx`, XML) leva descrições de um projeto a outro: para mandar um estudo
a um colega, reunir o trabalho de vários petrógrafos ou guardar um arquivo num formato aberto. Ele guarda tudo de uma
descrição — identificação, partes, composição, contagem de pontos, classificação, diagênese — e as análises,
solicitações e imagens da sua amostra; opcionalmente as imagens Atlas da sua lâmina.

## Antes de começar

* Um projeto com descrições salvas (para exportar), ou um arquivo de intercâmbio (para importar).
* Num servidor, importar exige o nível de petrógrafo ou acima.

## Passo a passo

### Exportar

1. **Início → Relatórios e intercâmbio → Exportar…** (Ctrl+E).
2. Marque as **Descrições** a exportar.
3. Escolha:
   * **Incluir as imagens** — as imagens de análises, solicitações e pontos contados;
   * **Incluir as imagens Atlas das lâminas** — todos os blocos das suas pirâmides vão para o arquivo (imagens de
     lâminas inteiras de vários gigabytes são melhor levadas com **Salvar projeto como…**);
   * **Um arquivo por descrição, numa pasta**.
4. **Exportar…** e escolha o arquivo (ou a pasta). "N descrições exportadas para …".

### Importar

1. **Início → Relatórios e intercâmbio → Importar…** (Ctrl+I).
2. **Arquivos…** ou **Pasta…** (todos os `.rfx` e `.xml` dela).
3. A lista mostra cada **Descrição**, o seu **Arquivo** e se está **Neste projeto** (*nova* ou *nome já usado*).
   Marque as que vai importar.
4. **Nomes já presentes no projeto**:
   * **Importar com outro nome: (2), (3)…**
   * **Ignorá-las**
   * **Substituir as descrições do projeto** (pede confirmação).
5. **Importar**. O resultado diz o que foi importado, renomeado ou não importado, e por quê.

## Opções

| Opção | O que muda |
|---|---|
| Incluir as imagens | Os anexos vão para o arquivo (em base64). |
| Incluir as imagens Atlas | As imagens das lâminas, com as suas anotações, mapas e pontos. |
| Um arquivo por descrição | Uma pasta de arquivos em vez de um arquivo só. |
| Nomes já presentes no projeto | Renomear, ignorar ou substituir. |

## Como funciona

O arquivo é conferido antes de qualquer importação (versão do formato, códigos conhecidos por este RockFace, totais
do projeto). Poços, amostras e lâminas são reconhecidos por nome e números, e assim duas descrições da mesma lâmina
continuam juntas; os identificadores são remapeados para o novo projeto; os resumos (totais, classificações) são
recalculados. Os arquivos gravados por qualquer RockFace anterior são lidos. Os totais personalizados do projeto que
exportou vão junto no arquivo.

O XML de outros programas é lido por um mapeamento (Início → **Importar XML com um mapeamento…**, página
[Catálogo de amostras, tabela para o Touchstone e XML por mapeamento](catalogue_exchange.md)).

## Por script

```python
with rf.open("estudo.rockface") as prj:
    prj.export("para-o-lab.rfx", names=["TS-9", "TS-10"], images=True)
    prj.export_folder("arquivo", names=None)               # um arquivo por descrição
with rf.create("copia.rockface") as outro:
    for r in outro.import_file("para-o-lab.rfx", policy="skip"):
        print(r["name"], r["action"], r["as"], r["messages"])
print(rf.read_exchange("para-o-lab.rfx").names())          # lê sem importar
```

## Limites e problemas comuns

* "Nenhuma descrição nos arquivos escolhidos."
* "…: não importada — …": o motivo (código desconhecido, arquivo gravado por um RockFace mais novo…).
* Substituir não pode ser desfeito.

## Cobertura

P2 (Exportar, Importar), P36 (gerador de XML em lote), P37 (importador de XML: arquivos ou pastas, conflitos de
nomes).

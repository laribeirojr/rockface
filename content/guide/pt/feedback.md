# Enviar a sua opinião

## Para que serve

O RockFace é testado por colegas e alunos antes de chegar a todos os usuários. **Enviar opinião…** abre o formulário
de opinião do RockFace no seu navegador, onde você diz o que funciona, o que não funciona e o que falta — sobre o
programa em geral ou sobre uma função deste guia. As respostas vão para a equipe do RockFace.

## Antes de começar

* Um navegador e uma conexão de rede.
* O formulário é um Microsoft Forms da equipe do RockFace (Universidade de Brasília). Enquanto o seu endereço não for
  definido, o botão avisa (abaixo).

## Passo a passo

1. No RockFace Petro: **Ajuda → Enviar opinião…**. No RockFace Atlas, Explorer, Lab e MC: o botão **Enviar opinião…**
   da barra de ferramentas.
2. O navegador abre o formulário. Diga sobre qual programa e qual função você escreve — a seção **Cobertura** no fim de
   cada página deste guia dá os itens da função (por exemplo *GT11*), que ajudam a equipe a encontrá-la.
3. Descreva o que você fez, o que esperava e o que aconteceu. Anexe uma captura de tela se ajudar; nunca anexe dados
   confidenciais.
4. Envie o formulário.

Quando o formulário ainda não está definido, o RockFace mostra "O formulário de opinião ainda não foi definido." —
escreva então para o endereço de suporte da sua equipe (**Ajuda → Suporte…** prepara as versões a enviar).

## Opções

| Onde | O que muda |
|---|---|
| Preferência `feedback/url` | O endereço do formulário (definido pela equipe quando o formulário muda). |
| Variável de ambiente `ROCKFACE_FEEDBACK_URL` | O mesmo, para um computador ou uma sessão; prevalece sobre a preferência. |

## Como funciona

O RockFace só abre o endereço do formulário no navegador: nada é enviado pelo programa, e nenhum arquivo, projeto ou
dado pessoal sai do computador. O texto de **Ajuda → Suporte…** (só as versões) pode ser colado no formulário.

## Por script

```python
print(rf.feedback_url())          # o endereço do formulário, ou "" quando ainda não está definido
rf.send_feedback("lab")           # abre o formulário no navegador; devolve o endereço, ou "" se não definido
```

Num terminal: `rockface feedback` mostra o endereço do formulário (ou que ele ainda não foi definido) e o abre.

## Limites e problemas comuns

* "O formulário de opinião ainda não foi definido." — a equipe ainda não deu o seu endereço: use **Ajuda →
  Suporte…**.
* Nada abre: nenhum navegador está definido como padrão do sistema; copie o endereço mostrado por `rockface feedback`.

## Cobertura

O2 (o formulário de opinião dos testadores nos programas, depois da 1.0 e do site).

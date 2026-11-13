# Trabalhar em equipe num servidor

## Para que serve

Uma equipe de petrógrafos descreve ao mesmo tempo a mesma coleção de amostras. Em vez de cada um manter um
arquivo de projeto, todos se conectam a um único **banco de dados no servidor**. Cada um vê o que os outros salvam,
e ninguém sobrescreve o trabalho de ninguém. O RockFace Petro, o Atlas, o Explorer, o Lab e o MC funcionam no
servidor do mesmo modo que num arquivo.

## Antes de começar

* O administrador da equipe preparou o servidor (veja "Preparar um servidor", abaixo) e lhe deu:
  * o endereço e a porta do servidor;
  * o nome do banco de dados;
  * o seu usuário e a sua senha.
* O seu computador alcança o servidor pela rede. Numa rede de laboratório isso costuma funcionar. Entre redes
  diferentes, pergunte ao administrador sobre SSL.

## Passo a passo

### Conectar

1. Abra o RockFace Petro. Na página inicial, ou em **Início → Servidor**, escolha **Conectar ao servidor**.
2. Preencha **Servidor**, **Porta** (normalmente 5432), **Banco de dados**, **Usuário** e **Senha**.
   * Dê um nome à conexão em **Conexão** (por exemplo "Laboratório").
   * Deixe marcado **Lembrar esta conexão**, para na próxima vez digitar só a senha. O RockFace nunca guarda a
     senha.
3. Opcional: clique em **Testar**. Aparecem o seu usuário e o seu **nível**.
4. Clique em **OK**. O título da janela mostra `banco@servidor — usuário (nível)`.

### O seu nível

O nível define o que você pode fazer. Quem o define é o administrador.

| Nível | Você pode |
|---|---|
| leitor | ler tudo, fazer consultas, figuras e relatórios |
| petrógrafo | também criar descrições e alterar **as suas**; adicionar imagens, análises, volumes, perfis |
| gestor | também alterar as descrições **de qualquer um** e a base de conhecimento, e remover bloqueios |
| administrador | também gerenciar usuários, níveis e senhas, e fazer cópias de segurança |

### Editar em equipe

* **Abrir uma descrição.** Quando você abre uma descrição para editar, o RockFace a **bloqueia** para você.
* **Outra pessoa está editando.** Se outra pessoa abrir a mesma descrição, verá uma mensagem como "ILL-02 está
  sendo editada por alice (LAB-PC3) desde 10:42: aberta somente para leitura". O botão Salvar dela fica desligado.
* **Descrição de outro autor.** Para um petrógrafo, ela abre somente para leitura, com uma mensagem dizendo quem a
  escreveu.
* **Quando o bloqueio sai.** Ele é liberado quando você abre outra descrição ou fecha o programa.
  * Um computador desligado, ou que perde a rede, deixa de renovar o bloqueio. Depois de 10 minutos o bloqueio fica
    livre de novo.
  * Um gestor pode remover um bloqueio na hora (Início → Servidor → Usuários, bloqueios e auditoria →
    **Bloqueios**).
* **Alterada no meio do caminho.** Se uma descrição que você tem aberta foi alterada por outra pessoa nesse meio
  tempo (por exemplo, um gestor que assumiu um bloqueio), o seu salvamento é recusado: "Este registro foi alterado
  em outra estação desde que você o abriu". Abra a descrição de novo, veja as alterações e refaça as suas. O
  RockFace nunca escreve por cima do trabalho de outra pessoa sem avisar.
* **O que os outros fazem.** A cada 15 segundos a barra de status mostra a última alteração feita por outra pessoa
  (por exemplo "bob: create description:ILL-B2"), e a árvore à esquerda é atualizada.

### O seu perfil e a sua senha

**Início → Servidor → Usuários, bloqueios e auditoria → Meu perfil**: o seu nome, instituição e e-mail, e **Mudar
minha senha** (pelo menos 8 caracteres).

### A auditoria

**Usuários, bloqueios e auditoria → Auditoria** lista todas as alterações: quando (UTC), quem, o quê, em qual
registro.

* Filtre por usuário, ação ou parte do nome do registro e clique em **Exportar CSV**.
* Ninguém pode alterar ou apagar a auditoria, nem um gestor.

### Publicar um arquivo de projeto no servidor

Para levar um projeto de um arquivo para o servidor, com as descrições, imagens, análises, volumes e perfis:

1. Abra o arquivo no RockFace Petro.
2. Escolha **Início → Servidor → Publicar no servidor**.
3. Clique em **Servidor e banco de dados (como administrador)…** e informe a conexão de um administrador a um banco
   **novo e vazio**. Ele é criado e preparado se ainda não existir.
4. Na tabela, informe para cada autor encontrado no arquivo o **usuário que ele tem no servidor**, para que
   continue editando as suas descrições.
5. Clique em **OK**. O RockFace abre a cópia do servidor.

### Cópia de segurança

* **Salvar projeto como…** de um projeto no servidor grava um arquivo de projeto (`.rockface`) completo, com tudo.
* O administrador pode fazer o mesmo pela linha de comando (`rockface server backup`).

## Preparar um servidor (administrador)

1. No computador servidor, com o Docker instalado, copie `docker/.env.example` para `docker/.env` e escolha uma
   senha longa em `ROCKFACE_ADMIN_PASSWORD`.
2. Inicie o banco de dados: `docker compose up -d db` (na pasta `docker`).
3. Prepare-o para o RockFace:

   ```
   docker compose --profile admin build
   docker compose run --rm admin init "postgresql+psycopg://rockface_admin@db:5432/rockface"
   ```

4. Adicione os usuários:

   ```
   ROCKFACE_NEW_PASSWORD=… docker compose run --rm admin add-user "postgresql+psycopg://rockface_admin@db:5432/rockface" alice --role petrographer --name "Alice …"
   ```

   Também é possível adicionar usuários pelo programa: **Usuários, bloqueios e auditoria → Usuários → Adicionar
   usuário**.
5. Faça cópias de segurança regularmente:

   ```
   docker compose run --rm admin backup "postgresql+psycopg://rockface_admin@db:5432/rockface" /backups/rockface-AAAA-MM-DD.rockface
   ```

**Sem Docker:** use qualquer PostgreSQL 13 ou mais novo e um computador com o RockFace instalado
(`pip install ".[server]"`). Os comandos são os mesmos, sem `docker compose run --rm admin`: por exemplo
`rockface server init postgresql+psycopg://admin@servidor:5432/rockface`.

## Opções

* **Criptografia (SSL)**: "conforme o servidor" (padrão), *prefer*, *require* ou *verify-full* (confere o
  certificado do servidor).
* **Senha vazia**: o RockFace usa o seu arquivo `pgpass` (`%APPDATA%\postgresql\pgpass.conf` no Windows,
  `~/.pgpass` nos outros sistemas).

## Como funciona

* **O servidor.** É um banco de dados PostgreSQL. O seu usuário é um usuário do banco. O seu nível é o grupo a que
  ele pertence: `rf_<banco>_viewer`, `…_petrographer`, `…_manager` ou `…_admin`.
* **Permissões.** O programa as confere antes de salvar, e o banco de dados as confere de novo, com os seus
  próprios privilégios e políticas de segurança por linha. Uma descrição só pode ser alterada pelo autor ou por um
  gestor, qualquer que seja o programa que escreva no banco.
* **Bloqueios.** Ficam no banco de dados (tabela `edit_lock`).
* **Versões.** Cada descrição tem um número de versão. O salvamento leva a versão que foi lida e é recusado se o
  banco tiver uma mais nova.
* **Mais.** Veja `docs/SERVER.md` para os detalhes e o teste de aceitação.

## Por script

```python
import rockface.api as rf
with rf.connect("postgresql+psycopg://alice@servidor:5432/rockface") as prj:
    print(prj.user, prj.role)
    for entry in prj.audit(limit=10):
        print(entry["when"], entry["user"], entry["action"], entry["target"])
    prj.backup("copia.rockface")
```

## Limites e problemas comuns

* **"Não foi possível conectar ao servidor"**: confira o endereço, a porta, o nome do banco, o usuário e a senha, e
  se o servidor aceita o seu computador (o `pg_hba.conf` dele).
* **"Você só pode ler este banco de dados"**: o seu nível é leitor; fale com o administrador.
* **"… foi escrita por …: só o autor ou um gestor pode alterá-la"**: é a descrição de um colega. Peça a um gestor,
  ou use **Salvar como…** (no grupo Descrição) para fazer a sua própria cópia.
* Imagens, volumes e perfis são registros compartilhados: quando duas pessoas alteram o mesmo, vale o último
  salvamento.

## Cobertura

P42 (versão servidor), R4 (armazenamento central), L13 (contêineres).

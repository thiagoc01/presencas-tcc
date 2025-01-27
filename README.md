# Aplicação para cadastro de obras e artistas | Projeto Presenças | TCC 2024/2025

Esse repositório contém o código para a aplicação externa que cadastra artistas e obras em um repositório CKAN com os metadados do Projeto Presenças.

## Como funciona?

A aplicação é simples. Ao subir, ela fica disponível na porta 80 por padrão com um container de NGINX atuando como proxy para uma aplicação Flask gerada por um Gunicorn. A stack contém um banco de dados para guardar a tabela de usuários e de solicitações e também um fail2ban. Caso você execute em Docker Swarm ou um cluster diferente, utilize o fail2ban com o proxy reverso e disponibilize o arquivo presencas.log em outro caminho que o fail2ban acesse. Veja as instruções para Docker Swarm.

Após iniciar a stack, acesse qualquer endereço da sua máquina/do seu cluster na porta específica para visualizar a tela de login. O menu é auto explicativo. Veja como configurar a aplicação abaixo.

## Dependências

- Docker
- Docker compose V2
- Python 3

## Como executar?

As instruções sempre serão consideradas para a produção e utilizando o Docker. Caso você queira utilizar o modo desenvolvedor, altere a variável FLASK_DEBUG para True no arquivo .env e DATABASE_URL para uma instância de SQLite. Execute python3 manage.py run.
Caso você queira rodar o modo produção sem Docker, rode o comando do Gunicorn conforme o Dockerfile.

Estando no diretório deste repositório, siga as instruções.

### Configurações para Docker Standalone

1 - Criar o arquivo presencas.log no diretório fail2ban e alterar o ownership do arquivo para o ID utilizado no container.

```sh
$ touch fail2ban/presencas.log
$ sudo chown 2024:2024 fail2ban/presencas.log
```
2 - Execute
```bash
$ mv .env.template .env
```
3 - Execute
```bash
$ mkdir psql/ && mkdir psql/data
```
4 - Execute
```bash
$ sudo docker build -t presencas .
```
5 - Execute
```bash
$ sudo docker network create presencas-tcc
```

**:warning: Se você desejar utilizar um banco externo, comente ou apague as linhas do serviço "db" e vá para o passo 9, caso contrário:**

6 - Altere a senha do PSQL no compose para uma mais forte.
Execute:
```bash
$ sudo docker compose up -d db
```
E depois monitore com
```bash
$ sudo docker compose ps
```
para verificar o status do container.

7 -  Execute
```bash
$ sudo docker compose exec db bash
```
8 - Execute
```bash
$ psql -h 127.0.0.1 --username postgres
```

9 - Crie um usuário para a aplicação. Recomenda-se rodar os seguintes comandos:

```sql
CREATE USER presencas WITH PASSWORD '<escolha uma senha>';
CREATE DATABASE presencas OWNER presencas;
```

10 - Saia do cliente do PSQL e do container com CTRL + D duas vezes.

11 - Obtenha uma SECRET_KEY executando
```bash
$ python3 -c 'import secrets; print(secrets.token_hex())'
```
12 - Editar o arquivo .env com essa SECRET_KEY gerada, altere a DATABASE_URL para o banco de dados a ser usado, altere a URL do CKAN forme configuração e também o TOKEN_REQUISICOES para o API token de um sysadmin do CKAN. Lembre-se, se utilizar o serviço de banco da stack, coloque o nome do container como host.

13 - Execute
```bash
$ sudo docker compose up -d
```
e verifique com o `docker compose ps` os status dos containers.

14 - Acesse 127.0.0.1:80 e verifique se a tela de login da aplicação aparece.

15 - Se tudo ocorrer bem, entre no container do Gunicorn com 
```bash
$ sudo docker compose exec guinicorn ash
```

16 - Inicialize o banco de dados com
```bash
$ flask db init && flask db migrate && flask db upgrade
```

17 - Execute
```bash
$ python3 manage.py criar_super_administrador
```

18 - Escolha um nome de usuário e uma senha e confirme-a. O superadministrador será criado e pode ser usado para a aplicação. Ao fim, saia do container.

### Configurações para Docker Swarm

No caso de um Swarm, é preciso realizar algumas mudanças como caminhos, estrutura da stack e exposição de portas.

Supondo que haja um proxy reverso geral, o serviço do fail2ban deve estar próximo dele para que as regras de firewall sejam aplicadas na mesma máquina. O arquivo de log do presenças, que é lido pelo fail2ban, deve estar visível ao fail2ban. A rede presencas-tcc deve ser do tipo **overlay**. Os nomes de container devem ser removidos e, por fim, os volumes devem ser alterados para um diretório visível a todos os hosts, como, por exemplo, um NFS. Portanto:

1 - Para todo caminho relativo, isto é, ./caminho/para, basta substituir o ponto por uma outra raiz, por exemplo:

```bash
/swarm-arquivos/presencas/psql
/swarm-arquivos/presencas/.env
```
2 - O volume 'compartilhamento' deve ser alterado para um local-persist ou para um bind também em `/swarm-arquivos/presencas/. Por exemplo:

```bash
/swarm-arquivos/presencas/arquivos-container
```

3 - As regras `ports` devem ser removidas, já que o proxy reverso do cluster irá administrar o acesso. No caso do banco, a porta pode ser exposta caso desejado.

4 - Caso a stack seja disparada via Portainer ou `stack deploy` e se nomeada como presencas, os nomes de hosts dos containers seguirão o mesmo. Caso contrário, atente-se ao nome de host no serviço do banco e no redirecionamento do `nginx.conf`.

## Como configurar?

O arquivo config.py possui classes com variáveis de configuração do Flask. Todas as linhas com `env.get` podem ter as variáveis configuradas no .env. As variáveis são:

| Variável | Descrição |
|-----------|---|
| SECRET_KEY    | Chave secreta utilizada pelo Flask (mandatório) |
| FLASK_DEBUG         |  Ativa ou desativa o modo Debug (True ou False)  |
| DATABASE_URL          | URL em formato de SQLAlchemy para o banco de dados (mandatório) |
| FLASK_APP | Não modificar |
| FLASK_RUN_PORT | Porta exposta para o modo Debug |
| TOKEN_REQUISICOES | Token utilizado para a API do CKAN, obtida via configuração de usuário no CKAN (mandatório) |
| CKAN_URL | Endereço da API do CKAN |
| SESSION_PERMANENT | Torna a sessão do usuário permanente |
| PERMANENT_SESSION_LIFETIME | Configura o tempo da sessão do usuário antes de expirar |
| ORGANIZACAO | Nome da organização no CKAN para uso na API |
| GRUPO | Nome do grupo no CKAN para uso na API |
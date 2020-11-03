# **Gerenciador de Matrículas**

## **Visão Geral**

Aplicação Flask que permite que gerentes se registrem e gerenciem o cadastro de alunos, cursos e suas respectivas
matrículas.

## **Como utilizar**

### Utilização via Docker

- Com Docker instalado, execute o comando `docker run -d -p 5000:5000 vitoto16/gerenciador_matriculas` para
utilizar a versão mais recente.

### Através deste repositório

- Clone o repositório em seu git local ou faça o download.
- No diretório raiz do projeto, crie um ambiente virtual e execute o comando `pip install -r requirements.txt`.
- Ainda no diretório raiz, acesse o Python Shell digitando `python` no seu terminal.
- Em seguida, gere uma chave de segurança executando o comando `import secrets` e em seguida `secrets.token_hex(16)`.
- Copie o valor gerado. Fora do Python Shell, associe o valor a uma variável de ambiente:
 
    - Em Windows: execute `set SECRET_KEY=<valor_gerado>`
    - Em Linux e MacOs: execute `export SECRET_KEY=<valor_gerado>`

- Então, atribua a uma variável de ambiente a URI que se pretende utilizar para o banco de dados. Esta operação pode ser
feita utilizando o método anterior. Exemplo: `export/set SQLALCHEMY_DATABASE_URI=sqlite:///site.db`.
- De volta no Python Shell, execute os seguintes comandos:

    - `from gerenciador_matriculas import create_app, db`
    - `app = create_app()`
    - `app.app_context().push()`
    - `db.create_all()`
- Assim criamos as tabelas no banco de dados a partir das classes modeladas no arquivo models.py.

#### A aplicação está pronta para uso!

Para iniciar o servidor de desenvolvimento, fora da Python Shell execute o comando `python run.py`.

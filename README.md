# Sistema de Gestão Universitária

Este é um sistema de gestão universitária desenvolvido com Flask e SQLite3.

## Descrição

O sistema permite que os usuários se autentiquem e acessem diferentes funcionalidades dependendo de seu papel (aluno, professor ou diretor). 

Os arquivos principais da aplicação são:

- `app.py`: Este é o arquivo principal que contém a aplicação Flask. Ele define as rotas e as lógicas para cada uma delas.

- `db.py`: Este arquivo contém funções para a criação do banco de dados e para adicionar usuários.

- `templates/index.html`: Este é o arquivo de modelo para a página inicial da aplicação.

- `templates/dashboard.html`: Este é o arquivo de modelo para a página Aluno da aplicação.

- `templates/professor.html`: Este é o arquivo de modelo para a página Professor da aplicação.

- `templates/diretor.html`: Este é o arquivo de modelo para a página Diretor da aplicação.

- `static/`: Pasta com os arquivos em CSS.

## Instalação

Para instalar e executar este projeto, você precisa ter Python 3 e pip instalados em seu sistema.

1. Primeiro, clone o repositório para o seu sistema local:

   ```
   git clone https://github.com/seu_usuario/Projeto_Senac.git
   ```

2. Vá para o diretório do projeto

3. Em seguida, instale as dependências do projeto usando pip:

   ```
   pip install -r requirements.txt
   ```

## Executando a aplicação

Após instalar as dependências, você pode executar a aplicação com o seguinte comando:

```
python app.py
```

## Como contribuir

Para contribuir para este projeto, siga os seguintes passos:

1. Faça um fork deste repositório.
2. Crie um novo branch em seu fork.
3. Faça as alterações desejadas em seu branch.
4. Faça um commit de suas alterações.
5. Abra um pull request para mesclar seu branch com o branch principal deste repositório.

Por favor, certifique-se de testar suas alterações antes de abrir um pull request.

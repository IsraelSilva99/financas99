# Finanças99 - Sistema de Gerenciamento Financeiro

Bem-vindo ao repositório do **Finanças99**, um sistema de gerenciamento financeiro desenvolvido para ajudar usuários a organizar suas finanças pessoais. Este projeto foi construído com Flask (Python) para o backend, MySQL (MariaDB) para o banco de dados, e HTML/CSS/JavaScript para o frontend. Ele permite que os usuários cadastrem transações, gerenciem categorias, configurem lembretes e acompanhem seu desempenho financeiro por meio de um dashboard interativo.

Este documento detalha o desenvolvimento do projeto, incluindo a estrutura do banco de dados, a configuração do backend, o design do frontend, a inserção de dados de teste e as funcionalidades implementadas.

## Índice

- [Finanças99 - Sistema de Gerenciamento Financeiro](#finanças99---sistema-de-gerenciamento-financeiro)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Screenshots do Sistema](#screenshots-do-sistema)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
    - [Tabela `user`](#tabela-user)
    - [Tabela `transacao`](#tabela-transacao)
    - [Tabela `lembrete`](#tabela-lembrete)
    - [Tabela `badge`](#tabela-badge)
  - [Backend (Flask)](#backend-flask)
  - [Frontend](#frontend)
    - [Dashboard](#dashboard)
    - [Página de Login](#página-de-login)
  - [Como Executar o Projeto](#como-executar-o-projeto)
    - [Pré-requisitos](#pré-requisitos)
    - [Passos](#passos)
  - [Próximos Passos](#próximos-passos)

## Visão Geral

O Finanças99 foi desenvolvido para atender às seguintes necessidades:
- **Gerenciamento de Transações**: Os usuários podem adicionar transações (receitas e despesas), categorizá-las e filtrá-las por ano e tipo.
- **Lembretes Financeiros**: Configuração de lembretes para despesas recorrentes, como aluguel ou consultas médicas.
- **Badges de Conquistas**: Sistema de recompensas que concede badges por metas financeiras alcançadas.
- **Dashboard Interativo**: Visualização de resumos financeiros, gráficos de fluxo de caixa, entradas vs. saídas, gastos por categoria e uma tabela de transações.

O desenvolvimento foi realizado em várias etapas, começando pela criação do banco de dados, seguida pela implementação do backend e frontend, e finalizando com a inserção de dados de teste e ajustes visuais.

## Screenshots do Sistema

Aqui estão algumas capturas de tela do sistema em funcionamento:

![Dashboard Principal](https://i.imgur.com/DXxmrnU.png)
*Dashboard principal com visão geral das finanças*

![Gráfico de Despesas](https://i.imgur.com/dB5WdPc.png)
*Análise detalhada de despesas por categoria*

![Controle de Transações](https://i.imgur.com/bKfPk4K.png)
*Interface de controle e gerenciamento de transações*

![Relatório Mensal](https://i.imgur.com/pQ8jfFj.png)
*Relatório mensal com análise comparativa*

![Visão Geral de Categorias](https://i.imgur.com/MIq5uOi.png)
*Visão geral das categorias de despesas e receitas*

## Tecnologias Utilizadas

- **Backend**:
  - Flask (Python) para o servidor web.
  - MySQL/MariaDB para o banco de dados.
  - `mysql-connector-python` para integração com o banco.
  - `werkzeug.security` para verificação de senhas hasheadas.
- **Frontend**:
  - HTML, CSS e JavaScript.
  - Tailwind CSS para estilização (página de login).
  - Chart.js para gráficos no dashboard.
  - Font Awesome para ícones.
  - Fonte Roboto para consistência visual.
- **Outros**:
  - XAMPP para ambiente de desenvolvimento local (MySQL e Apache).

## Estrutura do Projeto

A estrutura do projeto foi definida para organizar os arquivos de forma clara e modular:

```
financas99/
├── config/
│   └── database.php (configuração do banco de dados, não usado diretamente no Flask)
├── includes/
│   └── (futuras funções ou classes reutilizáveis)
├── public/
│   └── (arquivos estáticos como CSS e JS, usados pelo Flask)
│       └── css/
│           └── style.css
├── templates/
│   ├── dashboard.html (página principal com resumo financeiro e gráficos)
│   ├── login.html (página de login)
│   └── (outras páginas como register.html, adicionar_transacao.html, etc.)
└── app.py (aplicação Flask principal)
```

Essa estrutura foi sugerida em 20 de março de 2025, com a pasta `public` para arquivos estáticos e `templates` para os templates do Flask.

## Configuração do Banco de Dados

O banco de dados `financas99` foi criado no MySQL/MariaDB com as seguintes tabelas:

### Tabela `user`
Armazena os dados dos usuários.

| Campo | Tipo         | Nulo | Chave | Padrão | Extra          |
|-------|--------------|------|-------|--------|----------------|
| id    | int(11)      | NO   | PRI   | NULL   | auto_increment |
| nome  | varchar(100) | NO   |       | NULL   |                |
| email | varchar(100) | NO   | UNI   | NULL   |                |
| senha | varchar(255) | NO   |       | NULL   |                |

### Tabela `transacao`
Registra as transações financeiras (receitas e despesas).

| Campo     | Tipo          | Nulo | Chave | Padrão | Extra          |
|-----------|---------------|------|-------|--------|----------------|
| id        | int(11)       | NO   | PRI   | NULL   | auto_increment |
| user_id   | int(11)       | NO   | MUL   | NULL   |                |
| categoria | varchar(50)   | NO   |       | NULL   |                |
| valor     | decimal(10,2) | NO   |       | NULL   |                |
| mes       | varchar(20)   | NO   |       | NULL   |                |
| ano       | int(11)       | NO   |       | NULL   |                |
| tipo      | varchar(20)   | NO   |       | NULL   |                |

### Tabela `lembrete`
Armazena lembretes financeiros.

| Campo     | Tipo          | Nulo | Chave | Padrão | Extra          |
|-----------|---------------|------|-------|--------|----------------|
| id        | int(11)       | NO   | PRI   | NULL   | auto_increment |
| user_id   | int(11)       | NO   | MUL   | NULL   |                |
| categoria | varchar(50)   | NO   |       | NULL   |                |
| valor     | decimal(10,2) | NO   |       | NULL   |                |
| dia       | int(11)       | NO   |       | NULL   |                |
| mes       | varchar(20)   | NO   |       | NULL   |                |
| mensagem  | text          | NO   |       | NULL   |                |

### Tabela `badge`
Registra badges conquistados pelos usuários.

| Campo         | Tipo         | Nulo | Chave | Padrão | Extra          |
|---------------|--------------|------|-------|--------|----------------|
| id            | int(11)      | NO   | PRI   | NULL   | auto_increment |
| user_id       | int(11)      | NO   | MUL   | NULL   |                |
| nome          | varchar(100) | NO   |       | NULL   |                |
| descricao     | text         | NO   |       | NULL   |                |
| data_conquista| date         | NO   |       | NULL   |                |

O script SQL para criar essas tabelas foi fornecido em 20 de março de 2025 e executado via XAMPP.

## Backend (Flask)

O backend foi implementado com Flask no arquivo `app.py`. As principais funcionalidades incluem:

1. **Rota de Login** (`/login`):
   - Aceita requisições GET (exibe a página de login) e POST (processa o formulário).
   - Verifica o e-mail e a senha no banco de dados usando `mysql-connector-python`.
   - Usa `werkzeug.security.check_password_hash` para comparar a senha fornecida com o hash PBKDF2-SHA256 armazenado.
   - Armazena os dados do usuário na sessão (`session['user_id']`, `session['user_nome']`, `session['user_email']`) e redireciona para o dashboard se o login for bem-sucedido.
   - Exibe mensagens de erro via `flash` se as credenciais estiverem incorretas.

2. **Rota de Logout** (`/logout`):
   - Limpa a sessão e redireciona para a página de login com uma mensagem de sucesso.

3. **Rota do Dashboard** (`/dashboard`):
   - Verifica se o usuário está logado; caso contrário, redireciona para o login.
   - Renderiza o template `dashboard.html` com dados financeiros (transações, totais, gráficos).

O trecho do `app.py` foi fornecido em 17 de abril de 2025, com instruções para substituir a chave secreta e a senha do MySQL.

## Frontend

### Dashboard

O arquivo `dashboard.html` é a página principal do sistema, exibindo um resumo financeiro, gráficos e uma tabela de transações. Foi ajustado em várias etapas:

1. **Estrutura Inicial** (fornecida em 17 de abril de 2025):
   - **Cabeçalho**: Inclui o logo "Finanças99" e links de navegação (Dashboard, Adicionar Transação, Gerenciar Categorias, Lembretes, Perfil, Sair).
   - **Filtros**: Formulário para filtrar transações por ano e tipo (todos, despesas, receitas).
   - **Resumo Financeiro**: Exibe "Entradas", "Saídas" e "Total Livre".
   - **Gráficos**:
     - Fluxo de Caixa (gráfico de linha com Chart.js).
     - Entradas vs. Saídas (gráfico de barras).
     - Gastos por Categoria (gráfico de pizza).
   - **Tabela de Transações**: Mostra transações por categoria e mês, com totais de despesas, receitas e saldo livre por mês.

2. **Ajuste no Formato dos Valores** (17 de abril de 2025):
   - Os valores financeiros (ex.: `3800.00`) estavam sem formatação adequada.
   - Adicionamos uma função JavaScript `formatarDinheiro` para exibir valores no formato `R$ 1.000,00`:
     - Símbolo `R$` no início.
     - Ponto como separador de milhares.
     - Vírgula como separador decimal.
     - Duas casas decimais.
   - Aplicamos a formatação nas seções "Resumo Financeiro" e "Suas Transações", adicionando a classe `valor-financeiro` aos elementos relevantes e usando JavaScript para pós-processar os valores renderizados pelo Flask.

### Página de Login

O arquivo `login.html` foi criado para permitir que os usuários façam login no sistema. Passou por duas iterações:

1. **Primeira Versão** (17 de abril de 2025):
   - Design com Tailwind CSS, fundo gradiente (azul escuro para azul claro), formulário centralizado em um card branco.
   - Campos para e-mail e senha, botão "Entrar" e link para registro.
   - Não incluía integração com o backend; o botão "Entrar" não funcionava.

2. **Versão Final** (17 de abril de 2025):
   - **Ajustes no Design**:
     - Adicionamos a fonte Roboto e ícones do Font Awesome para consistência com o dashboard.
     - Suavizamos o gradiente do fundo para tons mais claros (`#3b82f6` para `#60a5fa`).
     - Adicionamos ícones nos campos de e-mail, senha e botão "Entrar".
   - **Funcionalidade do Login**:
     - Configuramos o formulário para enviar uma requisição POST para a rota `/login`.
     - Adicionamos suporte para mensagens flash, exibindo erros (ex.: "E-mail ou senha incorretos") ou mensagens de sucesso.
     - Integramos com o backend para verificar as credenciais e redirecionar para o dashboard.

## Como Executar o Projeto

### Pré-requisitos
- Python 3.x instalado.
- MySQL/MariaDB (recomendado: XAMPP para ambiente local).
- Bibliotecas Python:
  ```bash
  pip install flask mysql-connector-python werkzeug
  ```

### Passos
1. **Clone o Repositório**
   ```bash
   git clone https://github.com/seu_usuario/financas99.git
   cd financas99
   ```

2. **Configure o Banco de Dados**
   - Inicie o MySQL via XAMPP.
   - Crie o banco de dados `financas99`:
     ```sql
     CREATE DATABASE financas99;
     ```
   - Execute o script de criação das tabelas (fornecido anteriormente).

3. **Configure o Backend**
   - Abra o arquivo `app.py` e substitua:
     - `'sua_chave_secreta_aqui'` por uma chave segura (ex.: gere com `os.urandom(24).hex()`).
     - `'sua_senha'` pela sua senha do MySQL.
   - Inicie o servidor Flask:
     ```bash
     python app.py
     ```

4. **Acesse o Sistema**
   - Abra o navegador e acesse `http://localhost:5000/login`.
   - Crie uma nova conta ou faça login com suas credenciais.

## Próximos Passos

- **Expansão dos Dados**: Inserir dados para os outros 9 usuários, totalizando 10 usuários, 2000 transações, 500 lembretes e 150 badges.
- **Novas Funcionalidades**:
  - Adicionar um botão "Esqueceu a senha?" na página de login.
  - Implementar a página de registro (`register.html`).
  - Criar páginas para "Adicionar Transação", "Gerenciar Categorias" e "Lembretes".
- **Melhorias no Dashboard**:
  - Formatar os valores financeiros nos gráficos (ex.: rótulos e tooltips).
  - Adicionar mais filtros (ex.: por categoria).
- **Segurança**:
  - Implementar validação no frontend para os campos de login.
  - Adicionar proteção contra ataques como CSRF.

---

**Desenvolvido por [Seu Nome]**  
Última atualização: 17 de abril de 2025
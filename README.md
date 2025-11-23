# 🐍 Meu Blog Pessoal - Projeto Full Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

> "Construindo conhecimento, uma linha de código por vez."

Um sistema de blog completo desenvolvido do zero, aplicando conceitos fundamentais de desenvolvimento web, arquitetura MVC, autenticação de usuários e design responsivo moderno.

---

## 🌐 Demonstração Online
O projeto está rodando ao vivo! Você pode testar aqui:
👉 **[Acesse o Blog Online](https://herval.pythonanywhere.com/home)**
*(Substitua o link acima pelo seu link real do PythonAnywhere)*

---

## 📸 Screenshots

| Tela Inicial (Dark Mode) | Área de Login |
|:---:|:---:|
| ![Home](https://via.placeholder.com/400x200?text=Print+da+Home) | ![Login](https://via.placeholder.com/400x200?text=Print+do+Login) |

---

## ✨ Funcionalidades

### 🔐 Autenticação e Segurança
* **Cadastro e Login:** Sistema completo com hash de senha (Bcrypt) para segurança dos dados.
* **Proteção de Rotas:** Apenas usuários logados podem criar, editar ou apagar posts.
* **Autorização:** Um usuário só pode apagar ou editar os posts que *ele mesmo* criou.
* **Formulários Seguros:** Validação de dados e proteção CSRF com Flask-WTF.

### 📝 Gestão de Conteúdo (CRUD)
* **Criar:** Editor de texto para novas publicações.
* **Ler:** Feed principal com listagem de posts ordenados por data.
* **Atualizar:** Edição de posts existentes (com pré-preenchimento dos dados).
* **Deletar:** Remoção segura de postagens.

### 🎨 Design e UI/UX
* **Modo Escuro (Dark Mode):** Interface moderna com paleta de cores "Dark Lounge".
* **Hero Section:** Fachada impactante com imagem de fundo e botões neon.
* **Cards Interativos:** Efeito de elevação (hover) e sombras suaves.
* **Responsividade:** Layout centralizado e adaptável.
* **Ícones:** Uso de FontAwesome para uma interface limpa.

---

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Flask, SQLAlchemy (ORM).
* **Front-end:** HTML5, CSS3 (Variáveis CSS, Flexbox), Jinja2.
* **Banco de Dados:** SQLite.
* **Deploy:** PythonAnywhere.

---

## 🚀 Como Rodar o Projeto Localmente

Se você quiser rodar este projeto no seu computador, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/meu_blog.git](https://github.com/Lucianoherval/Sistema_blog_pessoal)
    cd meu_blog
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o Banco de Dados:**
    ```bash
    python
    >>> from app import app, db
    >>> with app.app_context():
    ...     db.create_all()
    >>> exit()
    ```

5.  **Rode o servidor:**
    ```bash
    python app.py
    ```
    Acesse em: `http://127.0.0.1:5000`

---

## 👨‍💻 Autor

Desenvolvido por **[Seu Nome]** durante meus estudos de Full Stack Python.
Entre em contato!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://github.com/Lucianoherval)
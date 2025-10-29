# --- 1. IMPORTAÇÕES (As Ferramentas) ---
from flask import Flask, render_template, request, redirect, url_for, flash #páginas de renderização', as 'redireções', as 'solicitações' e o 'flash'
from flask_sqlalchemy import SQLAlchemy #banco de dados
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user #login e logout
from flask_bcrypt import Bcrypt #criptografia
import os

# --- 2. CONFIGURAÇÃO (Ligar o Fogão e conectar o Caderno) ---

# Define o caminho absoluto para o nosso projeto
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jucas27072017*' # Senha para proteger o "carimbo" (sessão)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')

db = SQLAlchemy(app) # Conectando o "caderno" (Banco de Dados)
bcrypt = Bcrypt(app) # # Conectando o "embaralhador" (Bcrypt)
login_manager = LoginManager(app) # Conectando o "segurança" (LoginManager)

# Configuração do "Segurança":
# Se um cliente tentar acessar uma página protegida (ex: /criar_post) sem "carimbo",
# o "segurança" deve mandá-lo para a página de 'login'.
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' # Categoria da mensagem flash (opcional)
#login_manager.login_message = 'Por favor, faça login para acessar esta página.' # Mensagem flash (opcional)

# --- 3. MOLDES DO CADERNO (Modelos do Banco de Dados) ---
# Esta função é usada pelo "segurança" (LoginManager) para
# carregar o usuário que está "carimbado" (logado)
@login_manager.user_loader

def carregar_usuario(user_id):
    return Usuario.query.get(int(user_id))

# Molde 1: O Usuário (Cliente)
# UserMixin é um "kit" que já vem com as regras que o "segurança" precisa
# (ex: is_authenticated, is_active, etc.)
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # O "Número de Cliente Fiel" (ID único)
    nome = db.Column(db.String(100), nullable=False) # O "Nome do Cliente" (obrigatório)
    email = db.Column(db.String(120), unique=True, nullable=False) # O "Email do Cliente" (obrigatório e único)
    senha = db.Column(db.String(60), nullable=False) # A "Senha do Cliente" (obrigatório)
    
    # O "Relacionamento": Diz ao Usuário "Você tem muitas postagens"
    # 'Postagem' é o nome da Classe (Molde)
    # 'backref='autor'' cria um "atalho" (podemos chamar post.autor para ver o usuário)
    # 'lazy=True' significa que o SQLAlchemy só vai carregar as postagens quando pedirmos
    postagens = db.relationship('Postagem', backref='autor', lazy=True)

# Molde 2: A Postagem (O Pedido)
class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True) # O id unico da postagem
    titulo = db.Column(db.String(200), nullable=False) # O titulo da postagem (obrigatório)
    conteudo = db.Column(db.Text, nullable=False) # O conteudo da postagem (obrigatório)

    # A "Chave Estrangeira" (A Conexão)
    # Diz que este campo está ligado à coluna 'id' da tabela 'usuario' (nome da tabela é minúsculo)
    # nullable=False significa que uma postagem NÃO PODE existir sem um autor.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# --- 4. ROTA PRINCIPAL E EXECUÇÃO ---

# (Vamos adicionar nossas rotas aqui em breve)
# --- 5. RECEITAS (Rotas) ---

# --- Receita de Registro (Portaria) ---
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    # 'methods' diz que esta rota aceita tanto 'GET' (cliente visitando a página)
    # quanto 'POST' (cliente enviando o formulário)

    # Se o cliente está ENVIANDO o formulário (POST)...
    if request.method == 'POST':
        # 1. Pegue os dados do "pacote" (formulário)
        nome_usuario = request.form.get('nome')
        email_usuario = request.form.get('email')
        senha_usuario = request.form.get('senha')

        # 2. Verifique se o email já existe no "caderno"
        usuario_existente = Usuario.query.filter_by(email=email_usuario).first()
        if usuario_existente:
            # Envie uma "mensagem de erro" para o "salão"
            flash('Este email já está cadastrado. Tente outro.', 'danger')
            return redirect(url_for('registrar')) # Mande o cliente de volta ao formulário

        # 3. Se não existe, "embaralhe" a senha
        # Isso transforma '1234' em algo como '$2b$12$E...etc'
        senha_embaralhada = bcrypt.generate_password_hash(senha_usuario).decode('utf-8')

        # 4. Crie um novo "Cliente" (Usuario) usando o "molde"
        novo_usuario = Usuario(nome=nome_usuario, email=email_usuario, senha=senha_embaralhada)

        # 5. Mande o "caderno" (db) "anotar" (salvar) este novo usuário
        try:
            db.session.add(novo_usuario) # Coloca na "fila de espera"
            db.session.commit() # "Salva" permanentemente
            
            # Envie uma "mensagem de sucesso" para o "salão"
            flash('Conta criada com sucesso! Por favor, faça o login.', 'success')
            
            # Mande o cliente para a página de 'login' (que ainda vamos criar)
            return redirect(url_for('login')) # (Vamos criar 'login' em breve)

        except Exception as e:
            # Se der erro ao salvar (ex: o banco caiu)
            db.session.rollback() # "Desfaz" o que estava na fila
            flash(f'Erro ao criar conta: {e}', 'danger')
            return redirect(url_for('registrar'))

    # Se o cliente está apenas VISITANDO a página (GET)...
    # Apenas "sirva" (renderize) a página 'registrar.html' do "salão"
    return render_template('registrar.html')


# (Vamos adicionar a rota de Login e Home aqui)

# O "Botão de Play"
# Isso garante que o servidor só rode quando executamos o arquivo app.py diretamente
if __name__ == '__main__':
    app.run(debug=True)
# --- 1. IMPORTAÇÕES (As Ferramentas) ---
from flask import Flask, render_template, request, redirect, url_for, flash #páginas de renderização', as 'redireções', as 'solicitações' e o 'flash'
from flask_sqlalchemy import SQLAlchemy #banco de dados
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user #login e logout
from flask_bcrypt import Bcrypt #criptografia
import os
# ... (outras importações do Flask)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# ... (outras importações, como 'db', 'bcrypt')

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


# Função de validação customizada
def validate_email_custom(form, field):
    if Usuario.query.filter_by(email=field.data).first():
        raise ValidationError('Este email já está cadastrado. Tente outro.')

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

# --- 3. MOLDES DO CADERNO (Modelos do Banco de Dados) ---
# ... (sua classe Usuario e Postagem estão aqui) ...

# --- 3.5 MOLDES DOS FORMULÁRIOS (WTForms) ---
class FormularioRegistro(FlaskForm):
    # O "molde" do campo 'nome'
    nome = StringField('Nome', 
                       validators=[DataRequired(), Length(min=2, max=100)])

    # O "molde" do campo 'email'
    email = StringField('Email',
                        validators=[DataRequired(), Email(), validate_email_custom])

    # O "molde" do campo 'senha'
    senha = PasswordField('Senha', 
                          validators=[DataRequired(), Length(min=6)])

    # O "molde" do campo 'confirmar_senha'
    confirmar_senha = PasswordField('Confirmar Senha',
                                    validators=[DataRequired(), EqualTo('senha', message='As senhas não batem.')])

    # O "molde" do botão
    submit = SubmitField('Registrar')

# --- 4. ROTA PRINCIPAL E EXECUÇÃO ---

# (Vamos adicionar nossas rotas aqui em breve)
# --- 5. RECEITAS (Rotas) ---

# --- Receita de Registro (Portaria) ---
# --- Receita de Registro (Portaria) ---
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    # 1. Crie uma "instância" do nosso molde de formulário
    form = FormularioRegistro()

    # 2. A MÁGICA: 'validate_on_submit()' faz tudo:
    #    - Verifica se é um 'POST'
    #    - Verifica se o token CSRF (segurança) é válido
    #    - Roda TODOS os 'validators' que definimos (DataRequired, Email, etc.)
    if form.validate_on_submit():

        # 3. Se tudo for válido, pegue os dados "limpos"
        nome_usuario = form.nome.data
        email_usuario = form.email.data

        # 4. Embaralhe a senha
        senha_embaralhada = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

        # 4. Crie um novo "Cliente" (Usuario) usando o "molde"
        novo_usuario = Usuario(nome=nome_usuario, email=email_usuario, senha=senha_embaralhada)

        # 6. Salve no "caderno"
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso! Por favor, faça o login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar conta: {e}', 'danger')
            return redirect(url_for('registrar'))

    # 7. Se for um 'GET' ou se a validação FALHAR (ex: email já existe):
    #    Apenas "sirva" a página, passando o 'form' (que agora contém as mensagens de erro)
    return render_template('registrar.html', form=form)

# --- Receita da Página Principal (Home) ---
# Esta será a página principal do blog
@app.route('/')
@app.route('/home')
def home():
    # 1. LEIA O "CADERNO" (Banco de Dados):
    # Vá até o "molde" Postagem e "pegue" (query) TUDO (all).
    # Vamos também ordenar pela data/ID mais recente primeiro (opcional, mas legal)
    postagens = Postagem.query.order_by(Postagem.id.desc()).all()

    # 2. "Sirva" (renderize) a página 'home.html' E
    # "ENTREGUE" (passe) a lista de 'postagens' que encontramos para o HTML.
    # O HTML agora terá acesso a uma variável chamada 'lista_de_posts'
    return render_template('home.html', lista_de_posts=postagens)


# --- Receita de Login (Portaria) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o cliente está ENVIANDO o formulário (POST)...
    if request.method == 'POST':
        # 1. Pegue os dados do formulário
        email_form = request.form.get('email')
        senha_form = request.form.get('senha')

        # 2. Procure no "caderno" (db) se existe um usuário com esse email
        usuario_db = Usuario.query.filter_by(email=email_form).first()

        # 3. A VERIFICAÇÃO PRINCIPAL:
        # O usuário existe E a senha que ele digitou BATE com a senha embaralhada no banco?
        if usuario_db and bcrypt.check_password_hash(usuario_db.senha, senha_form):
            
            # 4. SIM! O "segurança" (Flask-Login) vai "dar o carimbo" (sessão)
            login_user(usuario_db) 
            
            flash('Login feito com sucesso!', 'success')
            
            # 5. Mande o cliente para a 'home'
            return redirect(url_for('home'))
        else:
            # 6. NÃO! Ou o email não existe ou a senha está errada
            flash('Login falhou. Verifique seu email e senha.', 'danger')
            return redirect(url_for('login')) # Manda de volta para a tela de login

    # Se o cliente está apenas VISITANDO a página (GET)...
    # Apenas "sirva" (renderize) a página 'login.html'
    return render_template('login.html')


# --- Receita de Logout (Saída) ---
@app.route('/logout')
def logout():
    logout_user() # O "segurança" (Flask-Login) "apaga o carimbo"
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('home')) # Manda o cliente de volta para a home

# --- Receita para Criar Postagem (Ação Protegida) ---
@app.route('/criar_post', methods=['GET', 'POST'])
@login_required # <-- O "SEGURANÇA"!
def criar_post():
    # @login_required: Esta é a mágica do "segurança" (Flask-Login).
    # Se um cliente não "carimbado" (logado) tentar acessar esta URL,
    # o Flask-Login o REDIRECIONA AUTOMATICAMENTE para a página de 'login'.
    # O código abaixo só executa se o cliente ESTIVER logado.

    # Se o cliente está ENVIANDO o formulário (POST)...
    if request.method == 'POST':
        # 1. Pegue os dados do formulário
        titulo_form = request.form.get('titulo')
        conteudo_form = request.form.get('conteudo')

        # 2. Crie uma nova "Postagem" usando o "molde"
        # AQUI ESTÁ A MÁGICA DA AUTORIA:
        # Usamos o 'current_user' (o cliente "carimbado" que o Flask-Login nos dá)
        # para preencher o campo 'autor' que definimos no nosso 'relacionamento'.
        nova_postagem = Postagem(titulo=titulo_form, 
                                 conteudo=conteudo_form, 
                                 autor=current_user)
        
        # 3. Mande o "caderno" (db) "anotar" (salvar)
        try:
            db.session.add(nova_postagem)
            db.session.commit()
            flash('Postagem criada com sucesso!', 'success')
            
            # 4. Mande o cliente de volta para a 'home'
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar postagem: {e}', 'danger')

    # Se o cliente está apenas VISITANDO a página (GET)...
    # Apenas "sirva" (renderize) a página 'criar_post.html'
    return render_template('criar_post.html')

# --- Receita para Apagar Postagem (Ação Super Protegida) ---
# Note que a rota espera um <int:post_id> - o número do post
@app.route('/post/<int:post_id>/apagar', methods=['POST'])
@login_required # 1ª Camada de Segurança: O cliente DEVE estar logado.
def apagar_post(post_id):
    
    # 2ª Camada de Segurança: Encontre o post no "caderno"
    # Se o post não existir (ex: URL digitada errada), isso dará um erro 404 (Não Encontrado)
    post_para_apagar = Postagem.query.get_or_404(post_id) 
    
    # 3ª Camada de Segurança (A MAIS IMPORTANTE: Autorização)
    # Verifique se o 'autor' do post é o MESMO cliente que está 'carimbado' (current_user)
    if post_para_apagar.autor != current_user:
        # Se não for o dono, ABORTE a operação.
        flash('Você não tem permissão para apagar este post.', 'danger')
        return redirect(url_for('home'))

    # Se todas as verificações passaram, o cliente é o dono.
    try:
        db.session.delete(post_para_apagar) # Mande o "caderno" apagar
        db.session.commit() # Salve a mudança
        flash('Postagem apagada com sucesso!', 'success')
        
        # Mande o cliente de volta para a home
        return redirect(url_for('home'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao apagar postagem: {e}', 'danger')
        return redirect(url_for('home'))

# --- Receita para Editar Postagem (Ação Duplamente Protegida) ---
@app.route('/post/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required # 1ª Camada: Tem que estar logado
def editar_post(post_id):
    
    # Busca o post no "caderno" ou falha (erro 404)
    post = Postagem.query.get_or_404(post_id)
    
    # 2ª Camada: Verificação de Autorização (dono do post)
    if post.autor != current_user:
        flash('Você não tem permissão para editar este post.', 'danger')
        return redirect(url_for('home'))
    
    # Se o cliente está ENVIANDO o formulário (POST)...
    if request.method == 'POST':
        # O cliente salvou as alterações
        
        # 1. Pegue os novos dados do formulário
        post.titulo = request.form.get('titulo')
        post.conteudo = request.form.get('conteudo')
        
        # 2. Mande o "caderno" (db) salvar (commit) as alterações
        # (Não precisamos de 'db.session.add()' pois o 'post' já está no caderno)
        try:
            db.session.commit()
            flash('Postagem atualizada com sucesso!', 'success')
            
            # 3. Mande o cliente de volta para a 'home'
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar postagem: {e}', 'danger')
    
    # Se o cliente está apenas VISITANDO a página (GET)...
    elif request.method == 'GET':
        # O cliente apenas clicou em "Editar"
        
        # 1. "Sirva" (renderize) a página 'editar_post.html'
        # 2. "Entregue" (passe) o 'post' que encontramos para o HTML
        #    (para que ele possa pré-preencher os campos)
        return render_template('editar_post.html', post=post)

# (Vamos adicionar a rota de Login e Home aqui)

# O "Botão de Play"
# Isso garante que o servidor só rode quando executamos o arquivo app.py diretamente
if __name__ == '__main__':
    app.run(debug=True)
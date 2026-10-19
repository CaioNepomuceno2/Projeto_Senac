import os
from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import db

app = Flask(__name__)
# Em produção defina a variável de ambiente SECRET_KEY; o valor abaixo é só para desenvolvimento.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-chave-insegura-troque-em-producao')

db.init_db()


def role_required(role):
    """Permite acessar a página apenas se o usuário logado tiver o perfil indicado."""
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if session.get('role') != role:
                return redirect(url_for('index'))
            return view(*args, **kwargs)
        return wrapper
    return decorator


def authenticate(username, password, role):
    user = db.find_user(username)
    return bool(user and user['role'] == role and check_password_hash(user['password'], password))


@app.route('/login_with_role', methods=['POST'])
def login_with_role():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # O botão "Entrar" não envia perfil e faz login como aluno;
    # os botões "Direção" e "Professor" enviam o perfil correspondente.
    role = request.form.get('role') or 'aluno'

    if role not in db.ROLES:
        return 'Perfil inválido.', 400

    if authenticate(username, password, role):
        session.clear()
        session['username'] = username
        session['role'] = role
        return role
    return 'Usuário ou senha inválidos.', 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@role_required('professor')
def dashboard():
    return render_template('dashboard.html')


@app.route('/diretor')
@role_required('diretor')
def diretor():
    return render_template('diretor.html')


@app.route('/professor')
@role_required('professor')
def professor():
    return render_template('professor.html')


@app.route('/aluno')
@role_required('aluno')
def aluno():
    return render_template('aluno.html')


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')

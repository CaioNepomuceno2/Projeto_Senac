"""Acesso ao banco SQLite: criação da tabela de usuários e carga de usuários de demonstração."""
import os
import sqlite3
from contextlib import contextmanager

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROLES = ('aluno', 'professor', 'diretor')

# Usuários criados automaticamente na primeira execução (apenas para demonstração).
DEMO_USERS = [
    ('diretor01', 'senha123', 'diretor'),
    ('professor01', 'senha123', 'professor'),
    ('aluno01', 'senha123', 'aluno'),
]

HASH_PREFIXES = ('scrypt:', 'pbkdf2:')


def get_db_path():
    return os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'users.db'))


@contextmanager
def get_connection():
    """Abre a conexão, confirma as alterações ao final do bloco e fecha a conexão."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def create_users_table():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL,
                         password TEXT NOT NULL,
                         role TEXT NOT NULL)''')


def add_user(username, password, role):
    """Cadastra o usuário com a senha armazenada como hash (se ainda não existir)."""
    if role not in ROLES:
        raise ValueError(f'Perfil inválido: {role}')
    with get_connection() as conn:
        exists = conn.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone()
        if not exists:
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                         (username, generate_password_hash(password), role))


def find_user(username):
    with get_connection() as conn:
        return conn.execute('SELECT username, password, role FROM users WHERE username = ?',
                            (username,)).fetchone()


def hash_plaintext_passwords():
    """Converte senhas antigas em texto puro (versões anteriores do projeto) para hash."""
    with get_connection() as conn:
        rows = conn.execute('SELECT id, password FROM users').fetchall()
        for row in rows:
            if not row['password'].startswith(HASH_PREFIXES):
                conn.execute('UPDATE users SET password = ? WHERE id = ?',
                             (generate_password_hash(row['password']), row['id']))


def init_db():
    """Cria a tabela (se necessário), migra senhas antigas e cadastra os usuários de demonstração."""
    create_users_table()
    hash_plaintext_passwords()
    for username, password, role in DEMO_USERS:
        add_user(username, password, role)


if __name__ == '__main__':
    init_db()
    print(f'Banco de dados pronto em {get_db_path()}')

import sqlite3

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE username = ?', (username,))
    user_exists = c.fetchone()
    if not user_exists:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        conn.commit()
    conn.close()

create_users_table()

add_user("diretor01", "senha123", "diretor")
add_user("professor01", "senha123", "professor")
add_user("aluno01", "senha123", "aluno")
add_user("Caio01","senha123","professor")

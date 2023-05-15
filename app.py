from flask import Flask, request, jsonify, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

@app.route('/logout')
def logout():
    return redirect(url_for('index')) 


def get_role(username, password):
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    role = request.form.get('role')
    if role:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username, password FROM users WHERE role = ?', (role,))
        user_data = c.fetchone()
        conn.close()
        if user_data:
            return jsonify({"username": user_data[0], "password": user_data[1]})
        else:
            return jsonify({"error": "Nenhum usuário encontrado para o papel selecionado."})
    else:
        return jsonify({"error": "Papel não fornecido."})

@app.route('/login_with_role', methods=['POST'])
def login_with_role():
    username = request.form['username']
    password = request.form['password']
    role = request.form.get('role')

    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        if role:
            cur.execute("SELECT role FROM users WHERE username = ? AND password = ? AND role = ?", (username, password, role))
        else:
            cur.execute("SELECT role FROM users WHERE username = ? AND password = ? AND role = 'aluno'", (username, password))
        result = cur.fetchone()

    if result:
        return result[0]
    else:
        return "Usuário ou senha inválidos.", 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diretor')
def diretor():
    return render_template('diretor.html')

@app.route('/professor')
def professor():
    return render_template('professor.html')

@app.route('/aluno')
def aluno():
    return render_template('aluno.html')


if __name__ == '__main__':
    app.run(debug=True)

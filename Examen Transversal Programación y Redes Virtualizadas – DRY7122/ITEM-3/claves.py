import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
      )
    ''')
    conn.close()

def store_user(u, p):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
    conn.commit()
    conn.close()

def validate_user(u, p):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.execute(
      "SELECT * FROM users WHERE username=? AND password=?", (u, p)
    )
    ok = cur.fetchone() is not None
    conn.close()
    return ok

@app.route('/')
def home():
    return "Bienvenido al control de credenciales"

@app.route('/register', methods=['POST'])
def register():
    user = request.form['username']
    pwd  = request.form['password']
    store_user(user, pwd)
    return jsonify(message="Usuario registrado exitosamente")

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    pwd  = request.form['password']
    if validate_user(user, pwd):
        return jsonify(message="Inicio de sesión exitoso")
    return jsonify(message="Usuario o contraseña incorrectos")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5800)

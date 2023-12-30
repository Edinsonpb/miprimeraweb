from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurar la conexión a la base de datos
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el registro de usuarios
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        conn.close()
        return redirect('/login')
    return render_template('signup.html')

# Ruta para el inicio de sesión de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['logged_in'] = True
            return redirect('/')
        else:
            return 'Login incorrecto. Inténtalo de nuevo.'
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

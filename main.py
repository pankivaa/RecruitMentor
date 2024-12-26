from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = '111'  # Добавьте секретный ключ для работы сессии

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("SELECT password FROM passwords WHERE login = ?", (Login,))
        pas = cursor_db.fetchone()

        cursor_db.close()
        db_lp.close()

        if pas and pas[0] == Password:
            session['logged_in'] = True  # Отметить, что пользователь вошел
            session['user'] = Login  # Сохранить имя пользователя в сессии
            return render_template('successfulauth.html', select_candidate=True)

        return render_template('auth_bad.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute("INSERT INTO passwords (login, password) VALUES (?, ?)", (Login, Password))
        db_lp.commit()

        cursor_db.close()
        db_lp.close()

        # Автоматический вход после регистрации
        session['logged_in'] = True
        session['user'] = Login
        return redirect(url_for('form_authorization'))

    return render_template('registration.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('form_authorization'))





if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for,jsonify, session
import sqlite3
import os
import time
import re

app = Flask(__name__)
app.secret_key = '111'  # Секретный ключ для работы сессией

DATABASE = 'login_pass.db'

def validate_field(field_value, field_name):
    """Проверяет, что поле не содержит цифр."""
    if field_value and re.search(r'\d', field_value):
        raise ValueError(f"Недопустимое значение в поле '{field_name}': {field_value}. Поле не должно содержать цифры.")


def init_db():
    """Создание базы данных и таблицы, если они ещё не существуют."""
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    last_name TEXT CHECK(last_name NOT LIKE '%0%' AND last_name NOT LIKE '%1%' 
                                          AND last_name NOT LIKE '%2%' AND last_name NOT LIKE '%3%' 
                                          AND last_name NOT LIKE '%4%' AND last_name NOT LIKE '%5%' 
                                          AND last_name NOT LIKE '%6%' AND last_name NOT LIKE '%7%' 
                                          AND last_name NOT LIKE '%8%' AND last_name NOT LIKE '%9%'),
                    first_name TEXT CHECK(first_name NOT LIKE '%0%' AND first_name NOT LIKE '%1%' 
                                          AND first_name NOT LIKE '%2%' AND first_name NOT LIKE '%3%' 
                                          AND first_name NOT LIKE '%4%' AND first_name NOT LIKE '%5%' 
                                          AND first_name NOT LIKE '%6%' AND first_name NOT LIKE '%7%' 
                                          AND first_name NOT LIKE '%8%' AND first_name NOT LIKE '%9%'),
                    middle_name TEXT CHECK(middle_name NOT LIKE '%0%' AND middle_name NOT LIKE '%1%' 
                                          AND middle_name NOT LIKE '%2%' AND middle_name NOT LIKE '%3%' 
                                          AND middle_name NOT LIKE '%4%' AND middle_name NOT LIKE '%5%' 
                                          AND middle_name NOT LIKE '%6%' AND middle_name NOT LIKE '%7%' 
                                          AND middle_name NOT LIKE '%8%' AND middle_name NOT LIKE '%9%'),
                    industry TEXT CHECK(industry NOT LIKE '%0%' AND industry NOT LIKE '%1%' 
                                         AND industry NOT LIKE '%2%' AND industry NOT LIKE '%3%' 
                                         AND industry NOT LIKE '%4%' AND industry NOT LIKE '%5%' 
                                         AND industry NOT LIKE '%6%' AND industry NOT LIKE '%7%' 
                                         AND industry NOT LIKE '%8%' AND industry NOT LIKE '%9%'),
                    company TEXT CHECK(company NOT LIKE '%0%' AND company NOT LIKE '%1%' 
                                        AND company NOT LIKE '%2%' AND company NOT LIKE '%3%' 
                                        AND company NOT LIKE '%4%' AND company NOT LIKE '%5%' 
                                        AND company NOT LIKE '%6%' AND company NOT LIKE '%7%' 
                                        AND company NOT LIKE '%8%' AND company NOT LIKE '%9%'),
                    position TEXT CHECK(position NOT LIKE '%0%' AND position NOT LIKE '%1%' 
                                         AND position NOT LIKE '%2%' AND position NOT LIKE '%3%' 
                                         AND position NOT LIKE '%4%' AND position NOT LIKE '%5%' 
                                         AND position NOT LIKE '%6%' AND position NOT LIKE '%7%' 
                                         AND position NOT LIKE '%8%' AND position NOT LIKE '%9%'),
                    tariff TEXT DEFAULT 'Базовый'
                )
            ''')

                        # Создание таблицы results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    profession TEXT NOT NULL,
                    name TEXT NOT NULL,
                    experience TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES querities(id) ON DELETE CASCADE
                )
            ''')

            # Создание таблицы querities
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS querities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recruiter_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    FOREIGN KEY (recruiter_id) REFERENCES recruiters(id) ON DELETE CASCADE
                )
            ''')
            db.commit()
        print("База данных и таблицы успешно созданы.")
    else:
        print("База данных уже существует.")

def add_record(login, password, last_name, first_name, middle_name, industry, company, position, tariff='Базовый'):
    """Добавление записи в таблицу с проверкой."""
    try:
        validate_field(last_name, "Фамилия")
        validate_field(first_name, "Имя")
        validate_field(middle_name, "Отчество")
        validate_field(industry, "Сфера деятельности")
        validate_field(company, "Компания")
        validate_field(position, "Должность")
        
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO passwords (login, password, last_name, first_name, middle_name, industry, company, position, tariff)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (login, password, last_name, first_name, middle_name, industry, company, position, tariff))
            db.commit()
            print("Запись успешно добавлена.")
    except ValueError as e:
        print(f"Ошибка добавления записи: {e}")

# Инициализация базы данных при запуске приложения
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        with sqlite3.connect(DATABASE) as db_lp:
            cursor_db = db_lp.cursor()
            cursor_db.execute("SELECT password FROM passwords WHERE login = ?", (Login,))
            pas = cursor_db.fetchone()

        if pas and pas[0] == Password:
            session['logged_in'] = True
            session['user'] = Login
            return redirect(url_for('dashboard'))  # Перенаправление на страницу аккаунта

        return render_template('auth_bad.html')

    return render_template('authorization.html')

# Новый маршрут для главной страницы аккаунта
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('form_authorization'))

    # Можно передать любые данные для отображения на главной странице аккаунта
    return render_template('dashboard.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        with sqlite3.connect(DATABASE) as db_lp:
            cursor_db = db_lp.cursor()
            cursor_db.execute("INSERT INTO passwords (login, password) VALUES (?, ?)", (Login, Password))
            db_lp.commit()

        session['logged_in'] = True
        session['user'] = Login
        return redirect(url_for('form_authorization'))

    return render_template('registration.html')


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' not in session:
        return redirect(url_for('form_authorization'))

    errors = {}  # Словарь для хранения сообщений об ошибках

    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        industry = request.form['industry']
        company = request.form['company']
        position = request.form['position']

        # Валидация данных
        try:
            validate_field(last_name, "Фамилия")
        except ValueError as e:
            errors['last_name'] = str(e)

        try:
            validate_field(first_name, "Имя")
        except ValueError as e:
            errors['first_name'] = str(e)

        try:
            validate_field(middle_name, "Отчество")
        except ValueError as e:
            errors['middle_name'] = str(e)

        try:
            validate_field(industry, "Сфера деятельности")
        except ValueError as e:
            errors['industry'] = str(e)

        try:
            validate_field(company, "Компания")
        except ValueError as e:
            errors['company'] = str(e)

        try:
            validate_field(position, "Должность")
        except ValueError as e:
            errors['position'] = str(e)

        # Если ошибок нет, обновляем профиль
        if not errors:
            with sqlite3.connect(DATABASE) as db:
                cursor = db.cursor()
                cursor.execute('''
                    UPDATE passwords
                    SET last_name = ?, first_name = ?, middle_name = ?, industry = ?, company = ?, position = ?
                    WHERE login = ?
                ''', (last_name, first_name, middle_name, industry, company, position, session['user']))
                db.commit()
            
            return redirect(url_for('dashboard'))  # Перенаправление на главную страницу аккаунта

    # Загрузка данных профиля из базы данных
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT last_name, first_name, middle_name, industry, company, position, tariff
            FROM passwords WHERE login = ?
        ''', (session['user'],))
        profile_data = cursor.fetchone()
    
    return render_template('profile.html', profile_data=profile_data, errors=errors)

@app.route('/start_search', methods=['POST'])
def start_search():
    # Получаем данные из формы
    city = request.form.get('city')
    university = request.form.get('university')
    faculty = request.form.get('faculty')
    experience = request.form.get('experience')
    position = request.form.get('position')
    skills = request.form.get('skills')
    soft_skills = request.form.getlist('soft_skills')
    english_level = request.form.get('english_level')

    # Логика поиска кандидатов (например, сохранение в базу данных или вызов API)

    # После обработки данных перенаправляем пользователя на страницу с результатами поиска
    return redirect(url_for('search_results', city=city, experience=experience, position=position))

@app.route('/search-form', methods=['GET'])
def search_form():
    return render_template('search_form.html')

@app.route('/process', methods=['POST'])
def process_request():
    # Получаем данные из формы
    description = request.form.get('description')
    
    # Имитируем обработку данных
    time.sleep(5)  # Эмуляция долгой работы

    # Заглушка: результат обработки
    results = [
        {
    "name": "Fahed",
    "experience": "1+ year in Data Science, 1+ year in managing business, data science consulting, and leading innovation projects",
    "skills": "Python, Tableau, Data Visualization, R Studio, Machine Learning, Statistics, IABAC Certified Data Scientist"
},
{
    "name": "Bhawana Aggarwal",
    "experience": "2 years in Wipro Technologies in Machine Learning, Deep Learning, Data Science, Python, Software Development",
    "skills": "Python, Machine Learning, Deep Learning, Data Science, Algorithms, Neural Network, NLP, Google Cloud Platform (GCP), Numpy, Pandas, Seaborn, Matplotlib, TensorFlow, KNN, Decision Tree, Logistic Regression, SVM, SQL, Oracle, Linux, Ubuntu, Windows"
}
    
    ]
    
    return jsonify({"message": f"Опираясь на ваше описание запроса, мы нашли следующих кандидатов, мы можем сказать, что ты ищите специалистов в области Data Science:", 
                    "candidates": results})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('form_authorization'))


if __name__ == '__main__':
    app.run(debug=True)


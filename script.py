import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import scipy.sparse as sp

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Загрузка данных из CSV
df = pd.read_csv('resumes_data_cleaned.csv', encoding='utf-8-sig')

# Функция для очистки текста
def clean_text(text):
    # Приводим текст к нижнему регистру
    text = text.lower()
    # Убираем ненужные символы
    text = re.sub(r'[^а-яА-ЯёЁ0-9\s]', '', text)
    # Убираем стоп-слова
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Применяем очистку ко всем текстовым столбцам
df['Description'] = df['Description'].apply(clean_text)
df['Experience'] = df['Experience'].apply(clean_text)
df['Education'] = df['Education'].apply(clean_text)

# Инициализация TF-IDF векторизатора
tfidf_vectorizer = TfidfVectorizer(max_features=5000)

# Векторизация текста
X_description = tfidf_vectorizer.fit_transform(df['Description'])
X_experience = tfidf_vectorizer.fit_transform(df['Experience'])
X_education = tfidf_vectorizer.fit_transform(df['Education'])

# Соединяем все текстовые данные в одну матрицу признаков
X = sp.hstack([X_description, X_experience, X_education])

# Преобразуем столбец 'City' с помощью OneHotEncoder
encoder = OneHotEncoder(sparse=False)
city_encoded = encoder.fit_transform(df[['City']])

# Соединяем категориальные данные с текстовыми признаками
X_final = sp.hstack([X, city_encoded])

# Создаем целевую переменную (метку)
df['is_relevant'] = df['Title'].apply(lambda x: 1 if 'Инженер отдела проектирования' in x else 0)

# Целевая переменная
y = df['is_relevant']

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Инициализация модели
model = LogisticRegression()

# Обучаем модель
model.fit(X_train, y_train)

# Прогнозируем на тестовых данных
y_pred = model.predict(X_test)

# Оценка модели
print(f"Точность: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# Пример: прогноз для одного резюме
sample_resume = "Строительство объектов, контроль качества, проектирование и т.д."  # Пример
sample_resume_cleaned = clean_text(sample_resume)
sample_resume_vectorized = tfidf_vectorizer.transform([sample_resume_cleaned])

# Прогноз
predicted = model.predict(sample_resume_vectorized)
print("Релевантность:", "Да" if predicted[0] == 1 else "Нет")






def clear_fun(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', ' ', text)  # Префикс 'r' добавлен
    text = re.sub(r"\\W", " ", text)      # Префикс 'r' добавлен
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)  # Префикс 'r' добавлен
    text = re.sub(r'<.*?>+', ' ', text)   # Префикс 'r' добавлен
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\n', ' ', text)       # Префикс 'r' добавлен
    text = re.sub(r'\w*\d\w*', ' ', text)  # Префикс 'r' добавлен
    return text

df['Resume']=df['Resume'].apply(clear_fun)



from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
le.fit(df['Category'])
df['Category']=le.transform(df['Category'])

df['Category'].unique()

import pandas as pd
import pickle  # Добавьте этот импорт
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re 
import string

# Загрузка данных из CSV
df = pd.read_csv('C:/Users/User/Desktop/RM/Timeweb/UpdatedResumeDataSet.csv', encoding='utf-8-sig')

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

df['Resume'] = df['Resume'].apply(clear_fun)

# Загрузка обученного TfidfVectorizer
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

# Функция для нахождения наиболее подходящих резюме
def match_resume(query, df, tfidf):
    # Преобразуем запрос рекрутера в TF-IDF вектор
    query_vector = tfidf.transform([query])
    
    # Получаем список всех резюме
    resumes = df['Resume']
    
    # Преобразуем все резюме в TF-IDF вектора
    resumes_vector = tfidf.transform(resumes)
    
    # Вычисляем схожесть между запросом и каждым резюме
    similarities = cosine_similarity(query_vector, resumes_vector).flatten()
    
    # Создаем DataFrame с резюме и степенью соответствия
    results = pd.DataFrame({
        'Resume': resumes,
        'Similarity': similarities
    })
    
    # Сортируем по убыванию сходства и выводим топ-5 резюме
    top_matches = results.sort_values(by='Similarity', ascending=False).head(5)
    
    return top_matches

# Пример запроса
query ="The ideal candidate should have:Proven experience with Python and R for data analysis and modeling.Strong knowledge of machine learning algorithms and practical experience in deploying predictive models.Expertise in working with SQL databases and handling large datasets.Proficiency in using data visualization tools such as Tableau, Power BI, or Matplotlib.Familiarity with cloud platforms (AWS, Azure, or Google Cloud) for data storage and processing is preferred.A bachelors degree in Computer Science, Statistics, or a related field (a master's degree is a plus).The role requires at least 3 years of experience in the Data Science field and a track record of delivering actionable business insights.Soft skills: problem-solving, teamwork, and adaptability."

# Найти подходящие резюме
top_matches = match_resume(query, df, tfidf)

# Выводим результаты: текст резюме и степень соответствия
for index, row in top_matches.iterrows():
    print(f"Resume: {row['Resume']}")
    print(f"Similarity: {row['Similarity']}\n")

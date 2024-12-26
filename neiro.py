import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re 
import string

df=pd.read_csv('C:/Users/User/Desktop/RM/Timeweb/UpdatedResumeDataSet.csv')



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

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer (stop_words='english')

tfidf.fit(df['Resume'])
requredTaxt = tfidf.transform(df['Resume'])

requredTaxt

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(requredTaxt,df['Category'], test_size=0.2, random_state=42)

X_train.shape
#print(X_train.shape)

X_test.shape
#print(X_test.shape)
#print(df['Resume'][0])

from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
clf = OneVsRestClassifier(KNeighborsClassifier())
clf.fit(X_train,y_train)
ypred = clf.predict(X_test)
print (accuracy_score(y_test,ypred))

import pickle
pickle.dump(tfidf,open('tfidf.pkl','wb'))
pickle.dump(clf,open('clf.pkl','wb'))


myresume="The ideal candidate should have:Proven experience with Python and R for data analysis and modeling.Strong knowledge of machine learning algorithms and practical experience in deploying predictive models.Expertise in working with SQL databases and handling large datasets.Proficiency in using data visualization tools such as Tableau, Power BI, or Matplotlib.Familiarity with cloud platforms (AWS, Azure, or Google Cloud) for data storage and processing is preferred.A bachelors degree in Computer Science, Statistics, or a related field (a master's degree is a plus).The role requires at least 3 years of experience in the Data Science field and a track record of delivering actionable business insights.Soft skills: problem-solving, teamwork, and adaptability."

import pickle
clf = pickle.load(open('clf.pkl','rb'))
cleaned_resume = clear_fun(myresume)
input_features = tfidf.transform([cleaned_resume])
prediction_id = clf.predict(input_features)[0]
category_mapping={
    6:'Data Science',
    12: 'HR',
    0:'Advocate',
    1:'Arts', 
    24:'Web Designing',
    16:'Mechanical Engineer',
    22:'Sales',
    14:'Health and fitness',
    5:'Civil Engineer',  
    15:'Java Developer',
    4:'Business Analyst',
    21:'SAP Developer', 
    2:'Automation Testing',
    11:'Electrical Engineering',
    18:'Operations Manager',
    20:'Python Developer', 
    8:'DevOps Engineer',
    17:'Network Security Engineer',
    19:'PMO', 
    7:'Database',
    13:'Hadoop',
    10:'ETL Developer',
    9:'DotNet Developer', 
    3:'Blockchain',
    23:'Testing',
    
}
category_name = category_mapping.get(prediction_id,'Unknown')
print('predicted Category:', category_name)
print(prediction_id)

"""df.head()
#print(df.head())

df.shape
#print(df.shape)

df.Category.value_counts()
#print(df.Category.value_counts())

plt.figure(figsize=(15,5))
sns.histplot(df['Category'])
plt.xticks(rotation=90)
#plt.show()

counts=df['Category'].value_counts()
labels=df['Category'].nunique()
labels

df['Category'].unique()
#print(df['Category'].unique())


counts=df['Category'].value_counts()
labels=df['Category'].unique()
plt.figure(figsize=(15,10))
plt.pie(counts,labels=labels,autopct='%1.1f%%',shadow=True,colors=plt.cm.plasma(np.linspace(0,1,3)))
#plt.show()

df['Resume'][0]
#print(df['Resume'][0])"""


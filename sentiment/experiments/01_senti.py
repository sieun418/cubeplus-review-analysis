# -*- coding: utf-8 -*-

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# NLTK 다운로드 (한 번만 실행)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# CSV 파일 읽기
file_path = "data/reviews_style.csv"  # 파일 경로를 수정하세요.
df = pd.read_csv(file_path)
# 텍스트 데이터 전처리
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # 텍스트를 소문자로 변환하고 토큰화
    tokens = [token for token in tokens if token.isalpha()]  # 알파벳 문자만 포함
    tokens = [token for token in tokens if token not in stop_words]  # 불용어 제거
    tokens = [lemmatizer.lemmatize(token) for token in tokens]  # 토큰들을 표준형으로 변환
    return ' '.join(tokens)

df['clean_text'] = df['review_text'].apply(preprocess_text)

# TF-IDF 특징 벡터 생성
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['clean_text'])
y = df['label']  # label은 'positive' 또는 'negative'

# 훈련 데이터와 테스트 데이터로 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 감성 분석 모델 훈련
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# 테스트 데이터에 대해 예측
y_pred = svm_model.predict(X_test)

# 정확도 계산
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# -*- coding: utf-8 -*-

import pandas as pd
import nltk
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score


# CSV 파일 읽기
file_path = "data/reviews_style.csv" 
df = pd.read_csv(file_path)

# 텍스트 데이터 전처리
okt = Okt()

def preprocess_text(text):
    tokens = okt.morphs(text)  # 형태소 분석을 통해 토큰화
    tokens = [token for token in tokens if token != ' ' and len(token) > 1]  # 공백 및 길이가 1인 토큰 제거
    return ' '.join(tokens)

df['clean_text'] = df['review_text'].apply(preprocess_text)

# TF-IDF 특징 벡터 생성
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['clean_text'])
y = df['rating']  # rating은 평가 등급

# 훈련 데이터와 테스트 데이터로 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 감성 분석 모델 훈련
svr_model = SVR(kernel='linear')
svr_model.fit(X_train, y_train)

# 테스트 데이터에 대해 예측
y_pred = svr_model.predict(X_test)

# 회귀 평가 지표 계산
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

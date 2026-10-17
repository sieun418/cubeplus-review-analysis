# -*- coding: utf-8 -*-
import pandas as pd
import nltk
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# CSV 파일 읽기
file_path = "data/reviews_style.csv" 
df = pd.read_csv(file_path)
positive_words = ["예쁘다", "만족스럽다", "편하다"]
negative_words = ["크다", "불편하다", "나쁘다"]

# 리뷰 텍스트를 감성 점수로 변환하는 함수
def sentiment_analysis(review_text):
    positive_count = sum(review_text.count(pos_word) for pos_word in positive_words)
    negative_count = sum(review_text.count(neg_word) for neg_word in negative_words)
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"


# 텍스트 데이터 전처리
okt = Okt()

def preprocess_text(text):
    tokens = okt.morphs(text)  # 형태소 분석을 통해 토큰화
    tokens = [token for token in tokens if token != ' ' and len(token) > 1]  # 공백 및 길이가 1인 토큰 제거
    return ' '.join(tokens)

df['clean_text'] = df['review_text'].apply(preprocess_text)

# 등급 추가
def assign_rating(rating):
    if rating == 5:
        return 'positive'
    else:
        return 'negative'

df['rating_class'] = df['rating'].apply(assign_rating)

# TF-IDF 특징 벡터 생성
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['clean_text'])
y = df['rating_class']  # rating_class는 'positive' 또는 'negative'

# 훈련 데이터와 테스트 데이터로 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 로지스틱 회귀 모델 훈련
logreg_model = LogisticRegression()
logreg_model.fit(X_train, y_train)

# 테스트 데이터에 대해 예측
y_pred = logreg_model.predict(X_test)

# 정확도 계산
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

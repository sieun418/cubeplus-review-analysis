# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 데이터셋 읽기
file_path = "data/reviews_style.csv" 
df = pd.read_csv(file_path)
# rating 열 기준으로 긍정과 부정 레이블링
df['rating_label'] = df['rating'].apply(lambda x: 'positive' if x >= 4 else 'negative')

# review_text 열을 텍스트 기반으로 긍정과 부정 레이블링
# 감성 레이블링 함수
def sentiment_label(text):
    positive_keywords = ['이쁘다', '만족스럽다', '좋다']  # 긍정적인 단어
    negative_keywords = ['아쉽다', '실망스럽다', '안좋다']  # 부정적인 단어
    
    for keyword in positive_keywords:
        if keyword in text:
            return 'positive'
    
    for keyword in negative_keywords:
        if keyword in text:
            return 'negative'
    
    return 'neutral'  # 위에서 정의된 키워드가 없으면 중립으로 간주

def sentiment_analysis(text_data, labels):
    # TF-IDF 특성 벡터 생성
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(text_data)
    
    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
    
    # SVM 분류기 훈련
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)
    
    # 테스트 데이터에 대한 예측
    y_pred = svm_model.predict(X_test)
    
    # 정확도 계산
    accuracy = accuracy_score(y_test, y_pred)
    
    return accuracy

df['text_label'] = df['review_text'].apply(sentiment_label)

print(df['text_label'].value_counts())

# 슬랙 봇 관련 토큰은 환경변수(.env)에서 읽음 — 원본에는 하드코딩되어 있었으나 공개 전 제거함
import os
from dotenv import load_dotenv
load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID", "")

# 슬랙 봇 관련 라이브러리
import os
import re
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

#######################################

# 크롤링 관련 라이브러리
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#######################################

# 감성분석 관련 라이브러리
import gru_sentiment as cap2  # 원본 파일명 cap2.py → sentiment/gru_sentiment.py 로 이동
'''import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from collections import Counter
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
'''
#######################################

# 리뷰 요약 및 키워드 추출 관련 라이브러리
'''
import openai
openai.organization = os.environ.get("OPENAI_ORG_ID")
openai.api_key = os.environ["OPENAI_API_KEY"]

#######################################

def get_openai_response(prompt, print_output=False):
	completions = openai.Completion.create(
		engine='text-davinci-003',
		temperature=0.5,
		prompt=prompt,
		max_tokens=3072,
		n=1,
		stop=None,
	)

	if print_output:
		print(completions)

	return completions.choices[0].text
'''

#######################################

# 웹 드라이버 초기화
driver = webdriver.Chrome()

# 리뷰를 저장할 리스트 초기화
results_list = []

def get_review(url, review_type):

    # 페이지 로드
	driver.get(url)
    
	if review_type == '상품 후기':
		# 상품 후기 클릭
		review_select = driver.find_element(By.XPATH, '//*[@id="estimateBox"]/div[2]/ul/li[2]')
		review_select.click()
	elif review_type == '일반 후기':
		# 일반 후기 클릭
		review_select = driver.find_element(By.XPATH, '//*[@id="estimateBox"]/div[2]/ul/li[3]')
		review_select.click()
	else:
		None
		
	time.sleep(2)

	j = 4
     
	# 다음 페이지로 이동하면서 리뷰를 가져옴
	while True:
		try:
			while j < 9:
				# 스크롤 해줘야 다음페이지로 넘어가짐
				driver.execute_script("window.scrollTo(300, 15000);")
			
				# 현재 페이지의 모든 리뷰 요소를 가져옵니다.
				review_elements = driver.find_elements(By.CSS_SELECTOR, "#reviewListFragment > div.review-list > div.review-contents > div.review-contents__text")
				
				for i in range(1, 11):
					css_selector_list = {
						'user_id' : f'#reviewListFragment > div:nth-child({i}) > div.review-profile > div > div.review-profile__text > p.review-profile__name',
						'review_text' : f'#reviewListFragment > div:nth-child({i}) > div.review-contents > div.review-contents__text',
						'size' : f'#reviewListFragment > div:nth-child({i}) > div.review-goods-information > div.review-goods-information__item > p > span',
						'review_text' : f'#reviewListFragment > div:nth-child({i}) > div.review-contents > div.review-contents__text'
						}
				
					result = {}
				# 현재 페이지의 모든 리뷰를 리스트에 추가합니다.				
					for key in css_selector_list:
						try:
							category = driver.find_element(By.CSS_SELECTOR, css_selector_list[key])
							result[key] = category.text
						except:
							result[key] = None
					if result[key] == None:
						None
					else:
						results_list.append(result)

			# 다음 페이지 버튼을 찾습니다.
				next_button = driver.find_element(By.XPATH, f'//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{j}]')
				#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > a.paging-btn.btn.active
			
				time.sleep(2)
			
			# 다음 페이지로 이동합니다.
				next_button.click()

				j += 1
				
				time.sleep(2)
			
			j = 4
		
		except :
			break

	#results_list = list(filter(('None', 'None', 'None'), results_list))
	df = pd.DataFrame(results_list)

	df.drop_duplicates(subset=['user_id', 'review_text'], inplace=True)

	print(df)
	
	return df


#############################################

# 슬랙 클라이언트 초기화
client = WebClient(token=SLACK_BOT_TOKEN)

# 메시지 출력할 채널 ID
channel_id = SLACK_CHANNEL_ID

# 슬랙봇 앱 초기화
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# 메시지 수신 시 실행하는 함수 작성
@app.event("message")
def handle_message_events(body, say):
	results_list = []
	event = body.get('event', {})
	text = event.get('text', '')

	# URL 추출 및 '>' 제거
	url_pattern = re.compile(r'https?://\S+')
	url_match = url_pattern.search(text)

	if url_match:
		url = url_match.group(0).strip('>')
		say(f"{url}")
		get_review(url, '스타일 후기')
		get_review(url, '상품 후기')
		df = get_review(url, '일반 후기')

		if df is not None:
			df.to_csv('reviews.csv', index=False)
			say(f"{url} 의 리뷰 정보를 CSV 파일로 저장했습니다.")
			cap2.sentiment_predict_from_csv('reviews.csv', 'review_text')

		else:
			say(f"유효하지 않은 URL: {url}")
	else:
		None
		#say("메시지에서 유효한 URL을 찾을 수 없습니다.")

    #link = message['text']

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
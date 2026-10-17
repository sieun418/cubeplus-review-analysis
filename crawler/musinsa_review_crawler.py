# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 웹 드라이버 초기화
driver = webdriver.Chrome()

# 첫 페이지 URL
url = "https://www.musinsa.com/app/goods/3606175"

# 리뷰를 저장할 리스트 초기화
results_list = []

# 페이지 로드
driver.get(url)

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
                    'product_name' : f'#reviewListFragment > div:nth-child({i}) > div.review-goods-information > div.review-goods-information__item > a' ,
                    'size' : f'#reviewListFragment > div:nth-child({i}) > div.review-goods-information > div.review-goods-information__item > p > span',
                    'review_text' : f'#reviewListFragment > div:nth-child({i}) > div.review-contents > div.review-contents__text',
                    'review_date' : f'#reviewListFragment > div:nth-child({i}) > div.review-profile > div > div.review-profile__text > p.review-profile__date',
                    'rating' : f'#reviewListFragment > div:nth-child({i}) > div.review-list__rating-wrap > span > span > span'
                    }
            
                result = {}
                
                # 현재 페이지의 모든 리뷰를 리스트에 추가합니다.
                # 안에서 for 문 돌려서 차라리 추가를 시켜버리는 것도 하나의 방법인듯?
                for key in css_selector_list:
                    category = driver.find_element(By.CSS_SELECTOR, css_selector_list[key])
                    result[key] = category.text
                
                # 별점 가져오기
                rating_element = driver.find_element(By.CSS_SELECTOR, css_selector_list['rating'])
                style_attribute = rating_element.get_attribute("style")
                width_value = style_attribute.split(":")[-1].strip("%;")
                rating = round(float(width_value) / 20)  # 별점 변환
                
                result['rating'] = rating  # 결과에 별점 추가
                
                results_list.append(result)

        # 다음 페이지 버튼을 찾습니다.
            next_button = driver.find_element(By.XPATH, f'//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{j}]')
        
            time.sleep(2)
        
        # 다음 페이지로 이동합니다.
            next_button.click()

            j += 1
            
            time.sleep(2)
        
        j = 4
    
    except Exception as e:
        print(e)
        break

# 모든 리뷰 출력

print(results_list)

df = pd.DataFrame(results_list)

df.to_csv('reviews_style1.csv', index=False)

# 웹 드라이버 종료
driver.quit()

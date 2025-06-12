import requests
from config import Config
import pandas as pd
import numpy as np
import re


def calculate(ml, price, cnt):
    "(100미리리터 당 가격) / 상품갯수로 리턴"
    cal_ml = round(ml / 100, 5)
    return round((price / cal_ml) / cnt, 2)


np_item_li = []
# 네이버 검색(쇼핑몰) API

# 검색어 및 API URL
query = "향수"

# 요청 헤더
headers = {
    # 애플리케이션 등록 시 발급받은 ID와 Secret
    "X-Naver-Client-Id": Config.NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": Config.NAVER_CLIENT_SECRET
}

start = 1
while_bool = True

try:

    while while_bool:

        url = f"https://openapi.naver.com/v1/search/shop.json?query={query}&display=10&start={start}&sort=sim&exclude=used:cbshop:rental"

        # 요청 전송
        response = requests.get(url, headers=headers)
        data_dict = response.json()


        # 응답 가공
        item_li = data_dict['items']

        for item in item_li:

            if not item['link'].startswith('https://smartstore.naver.com/main/products/'):
                continue

            if item['category2'] != '향수':
                continue

            if item['category3'] == '고체향수':
                continue

            if item['category3'] == '여성향수':
                item['category3'] = '여성'
            elif item['category3'] == '남성향수':
                item['category3'] = '남성'
            elif item['category3'] == '남녀공용향수':
                item['category3'] = '공용'
            else:
                continue


            ml = None

            title = item['title']

            match = re.search(r'(\d+)\s*[mM][lL]', title)
            
            if match:
                ml = int(match.group(1))
                # 매치된 부분을 제거 (중간에 있어도 됨)
                title = title[:match.start()] + title[match.end():]

            if ml == None:
                continue
            
            item['ml'] = int(ml)


            count = 1
            # 1. 수량 추출 (1차 시도: ~개 또는 ~ + ~ 개)
            count_match = re.search(r'(\d+)(\s*\+\s*\d+)?\s*개', title)
            if count_match:
                if count_match.group(2):  # 2 + 3 개
                    numbers = re.findall(r'\d+', count_match.group(0))
                    count = sum(map(int, numbers))
                else:
                    count = int(count_match.group(1))
                title = title[:count_match.start()] + title[count_match.end():]

            else:
                # 2. 수량 추출 (2차 시도: ~ + ~ 형식만 존재하고 '개'는 없음)
                plus_match = re.search(r'(\d+)\s*\+\s*(\d+)', title)
                if plus_match:
                    count = int(plus_match.group(1)) + int(plus_match.group(2))
                    title = title[:plus_match.start()] + title[plus_match.end():]

            item['count'] = count

            title = title.replace('<b>', '')
            title = title.replace('</b>', '')

            title = title.strip()
            title = title.rstrip(' ,')

            while title.find('[') != -1 and title.find(']') != -1:
                if title.find(']') + 1 == len(title):
                    title = title[0:title.find('[')]
                else:
                    title = title[0:title.find('[')] + title[title.find(']')+1:]

            item['lprice'] = int(item['lprice'])


            print(f'{len(np_item_li)+1}번 상품추가')
            print(item)

            np_item_li.append([item['productId'], title, item['lprice'], item['count'], item['ml'], item['category3'], item['link']])

            if len(np_item_li) == 500:
                while_bool = False
                break
        start += 10

except KeyError:
    print('키에러 발생')
    print('더 불러올 상품 없음.')

np_item_li = np.array(np_item_li)
print(np_item_li)


# 1. NumPy 배열을 DataFrame으로 변환
df = pd.DataFrame(np_item_li)

# (선택) 열 이름 지정하고 싶을 경우
df.columns = ['productId', '제목', '가격', '개수', '용량(ml)', '타겟', 'URL'] # 가격은 100ml 당 가격으로 가공할 예정

# 2. CSV 파일로 저장
df.to_csv('output.csv', index=False, encoding='utf-8-sig')
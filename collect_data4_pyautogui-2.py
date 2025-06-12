import pyautogui
import webbrowser
import pandas as pd
import pyperclip

# 환경설정
# $pip install opencv-python

def search_img(img_path):
    img = pyautogui.locateOnScreen(img_path, region=(0, 820, 1260-0, 1380-820), confidence=0.85)
    pyautogui.moveTo(img)
    x, y = pyautogui.position()
    pyautogui.sleep(0.5)
    if y > 1300:
        pyautogui.scroll(-150)
        search_img(img_path=img_path)
    else:
        return

# CSV 읽기
df = pd.read_csv('data2.csv', encoding='utf-8-sig')  # 인코딩은 상황에 따라 조정

try:
    webbrowser.open_new('https://naver.com') # 새 창에서 해당 주소 열기

    pyautogui.sleep(2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'up')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'left')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'left')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'left')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'left')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'left')
    pyautogui.sleep(0.2)
    pyautogui.press('esc')
    pyautogui.sleep(0.2)
    pyautogui.hotkey('win', 'down') # 이미지 검색을 위해 창이 작을수록 정확도 높아짐

    for i in range(len(df)):


        print(f'작업중: {i+1}/{len(df)}')
        if not pd.isna(df.loc[i, '평점']):
            continue

        url = df.loc[i, 'URL']
        webbrowser.open_new_tab(url) # 새 창에서 해당 주소 열기
        pyautogui.sleep(1)
        # 브라우저 열면 해당 창이 자동 활성화

        # 복붙방지 뚫기
        pyautogui.hotkey('alt', '1') # 크롬 드래크프리 깔려있어야 함.
        pyautogui.sleep(0.5)

        # 평점, 리뷰수
        pyperclip.copy('리뷰 보기')
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.sleep(0.3)
        try:
            # img = pyautogui.locateOnScreen(r".\img\review.png", region=(0, 820, 1260-0, 1380-820), confidence=0.85)
            # pyautogui.moveTo(img)
            # pyautogui.sleep(0.5)
            search_img(r".\img\review.png")

            # pyautogui.mouseInfo()
            # 465,1102 236,155,74 #EC9B4A

            # 198,1102 231,100,99 #E76463
            # 497,1105 255,255,255 #FFFFFF

            pyautogui.move(35, 0)
            x, y = pyautogui.position()
            # pyautogui.dragRel(-340, 0, duration=0.5)
            pyautogui.dragTo(162, y, duration=0.5)
            pyautogui.sleep(1.5)
            pyautogui.hotkey('ctrl', 'c')

            # 평점4.92(최근 6개월 4.91)1,875
            text = pyperclip.paste().strip()
            star = text[text.find('평점')+2:text.find('(')]
            if text.find('리') != -1:
                star_count = text[text.find(')')+1:text.find('리')]
            else:
                star_count = text[text.find(')')+1:]
            star_count = int(star_count.replace(',', ''))

            print(f'평점: {star}')
            print(f'리뷰수: {star_count}')
            pyautogui.click()

        except pyautogui.ImageNotFoundException:
            print('리뷰 이미지 못 찾음')

            # dataframe에 None으로 다 추가
            df.loc[i, '평점'] = None
            df.loc[i, '리뷰수'] = None
            df.loc[i, '향/냄새 만족도(%)'] = None
            df.loc[i, '지속력 만족도(%)'] = None
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'w')
            continue


        # 향/냄새 만족도
        pyperclip.copy('사용자 총 평점')
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.sleep(0.3)
        pyperclip.copy('향/냄새')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.sleep(0.3)
        try:
            # img = pyautogui.locateOnScreen(r".\img\fragrance.png", region=(0, 820, 1260-0, 1380-820), confidence=0.85)
            # pyautogui.moveTo(img)
            # pyautogui.sleep(0.5)
            search_img(r".\img\fragrance.png")

            # pyautogui.mouseInfo()

            # 기존
            # 906,1071 0,0,0 #000000
            # 1050,1069 207,249,233 #CFF9E9
            # 1027,1071 248,249,251 #F8F9FB

            # 수정(CSS가 독특해서 수정)
            # 906,1152 0,0,0 #000000
            # 1107,1152 227,184,138 #E3B88A
            # 931,1152 248,249,251 #F8F9FB

            pyautogui.move(201, 0)
            pyautogui.dragRel(-176, 0, duration=0.5)
            pyautogui.sleep(1.5)
            pyautogui.hotkey('ctrl', 'c')

            # 80
            # 아주 만족해요55%(999+명)
            fragrance = pyperclip.paste().strip()
            fragrance = int(fragrance[fragrance.find('요')+1:fragrance.find('%')])
            print(f'향/냄새 만족도(%): {fragrance}')
            pyautogui.click()

        except pyautogui.ImageNotFoundException:
            print('향/냄새 이미지 못 찾음')
            fragrance = None

        finally:
            pyautogui.click()
            

        # 지속력 만족도
        pyperclip.copy('지속력')
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.sleep(0.3)
        try:
            # img = pyautogui.locateOnScreen(r".\img\vitality.png", region=(0, 820, 1260-0, 1380-820), confidence=0.85)
            # pyautogui.moveTo(img)
            # pyautogui.sleep(0.5)
            search_img(r".\img\vitality.png")

            # pyautogui.mouseInfo()
            # 906,1071 0,0,0 #000000

            # 1050,1069 207,249,233 #CFF9E9
            # 1027,1071 248,249,251 #F8F9FB


            pyautogui.move(201, 0)
            pyautogui.dragRel(-176, 0, duration=0.5)
            pyautogui.sleep(1.5)
            pyautogui.hotkey('ctrl', 'c')

            # 80
            # 아주 만족해요55%(999+명)
            vitality = pyperclip.paste().strip()
            vitality = int(vitality[vitality.find('요')+1:vitality.find('%')])
            print(f'지속력(%): {vitality}')
            pyautogui.click()


        except pyautogui.ImageNotFoundException:
            print('지속력 이미지 못 찾음')
            vitality = None

        finally:
            pyautogui.click()


        pyautogui.hotkey('ctrl', 'w')

        df.loc[i, '평점'] = star
        df.loc[i, '리뷰수'] = star_count
        df.loc[i, '향/냄새 만족도(%)'] = fragrance
        df.loc[i, '지속력 만족도(%)'] = vitality

except Exception as e:
    print(e)

finally:
    # 결과 출력
    print(df)

    # (선택) 수정된 내용을 새 CSV로 저장
    df.to_csv('data3.csv', index=False, encoding='utf-8-sig')
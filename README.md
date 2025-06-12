# 향수 가격 예측 프로젝트

## 1. 프로젝트 개요
- **목표**: 네이버 쇼핑에서 수집한 향수 관련 데이터를 기반으로 머신러닝과 딥러닝을 활용해 향수 가격을 예측하는 모델 개발
- **주요 작업**: 데이터 수집 → 전처리 → 모델링 → 결과 비교 및 시각화

---

## 2. 데이터 수집

### 2-1. 수집 대상
- 상품명, 가격, 용량, 향종류 등 정량적 데이터
- 리뷰, 평점, 구매자 코멘트 등 정성적 데이터
- 이미지 및 기타 부가 정보

### 2-2. 데이터 수집 방법

- **네이버 쇼핑 API 활용**
  - 상품 리스트 및 상세 정보 수집
  - 수집된 JSON 데이터 구조 파악 및 저장

- **Selenium, PyAutoGUI, Pyperclip 이용 수집 자동화**
  - 네이버 쇼핑 검색 결과를 브라우저로 띄워 수집
  - 마우스와 키보드 자동 조작을 통해 스크롤 및 복사 작업 수행
  - 복사한 데이터를 클립보드에서 가져와 파싱 및 저장

```python
import pyautogui
import pyperclip
import time

def search_and_copy(keyword):
    # 네이버 쇼핑 검색창에 키워드 입력
    pyautogui.click(x=300, y=100)  # 검색창 위치 (예시)
    pyautogui.write(keyword)
    pyautogui.press('enter')
    time.sleep(3)  # 페이지 로딩 대기

    # 상품 리스트 영역 복사
    pyautogui.click(x=400, y=400)  # 리스트 시작점
    pyautogui.dragTo(400, 800, duration=1)  # 드래그
    pyautogui.hotkey('ctrl', 'c')  # 복사
    time.sleep(1)

    data = pyperclip.paste()
    return data

# 예시: '향수' 키워드 검색 및 데이터 복사
raw_data = search_and_copy("향수")
print(raw_data[:500])  # 일부 출력
````

* **수집 데이터 저장**

  * CSV, JSON 등 다양한 포맷으로 저장하여 이후 전처리 단계에 활용

---

## 3. 데이터 전처리

* **결측치 처리**

  * 누락된 값 제거 또는 평균/중앙값 대체
* **이상치 탐지 및 제거**

  * 가격, 용량 등의 비정상적인 값 필터링
* **범주형 변수 인코딩**

  * 향종류 등 텍스트 데이터를 원-핫 인코딩 혹은 라벨 인코딩으로 변환
* **수치 데이터 정규화**

  * Min-Max 스케일링 혹은 표준화 수행

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# 데이터 불러오기
df = pd.read_csv('perfume_data.csv')

# 결측치 처리
df.dropna(inplace=True)

# 라벨 인코딩 예시
le = LabelEncoder()
df['향종류_encoded'] = le.fit_transform(df['향종류'])

# 정규화 예시
scaler = MinMaxScaler()
df[['가격_scaled']] = scaler.fit_transform(df[['가격']])
```

---

## 4. 모델링

### 4-1. 머신러닝 모델

* 랜덤포레스트, XGBoost 등 앙상블 모델 활용
* 교차검증으로 과적합 방지 및 성능 평가

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

X = df[['용량', '향종류_encoded']]
y = df['가격']

model = RandomForestRegressor(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')

print("평균 RMSE:", (-scores.mean())**0.5)
```

### 4-2. 딥러닝 모델

* 간단한 DNN 모델 설계 및 학습

```python
import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2)
```

---

## 5. 결과 비교 및 시각화

* RMSE, MAE, R² 점수를 기준으로 모델 성능 평가
* 실제 가격 vs 예측 가격 그래프 시각화

```python
import matplotlib.pyplot as plt
import numpy as np

y_pred = model.predict(X).flatten()

plt.scatter(y, y_pred, alpha=0.5)
plt.xlabel('실제 가격')
plt.ylabel('예측 가격')
plt.title('실제 가격 vs 예측 가격')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.show()
```

---

## 6. 결론 및 향후 연구 방향

* 수집 데이터 품질 향상 필요
* 추가 피처 엔지니어링 시도
* 모델 튜닝 및 앙상블 기법 적용 검토
* 이미지 데이터 및 리뷰 텍스트 분석 추가

---

## 부록: 주요 라이브러리

* pandas, numpy
* scikit-learn
* tensorflow/keras
* selenium, pyautogui, pyperclip

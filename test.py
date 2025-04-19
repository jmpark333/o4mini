# test.py
# 수정: 전체 코드를 EIA API v2 직접 호출 방식으로 변경 및 영어 타이틀 적용 (2025-04-18 06:01:30)
import os  # 환경변수 로드용
import requests
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 1) 환경변수에서 EIA API 키 로드 및 유효성 검사
EIA_API_KEY = os.getenv("EIA_API_KEY")
if not EIA_API_KEY:
    print("환경 변수 EIA_API_KEY에 유효한 API 키를 설정해주세요.")
    exit(1)

# 2) EIA API 호출: v2 직접 호출 방식으로 변경 (2025-04-17 23:04:21)
# 전력 소비 데이터 가져오기 (캘리포니아 주 데이터)
url = "https://api.eia.gov/v2/electricity/retail-sales/data"
params = {
    "api_key": EIA_API_KEY,
    "frequency": "monthly",
    "data[]": "sales",
    "facets[stateid][]": "CA",  # 캘리포니아
    "facets[sectorid][]": "ALL",  # 모든 섹터
    "start": "2010-01",
    "end": "2023-12",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc"
}

resp = requests.get(url, params=params)
if resp.status_code != 200:
    print(f"EIA API 요청 실패: HTTP {resp.status_code}: {resp.text}")
    exit(1)

data_json = resp.json()
if "response" not in data_json or "data" not in data_json["response"]:
    print("EIA API 응답 오류:", data_json)
    exit(1)

# 데이터 추출 및 DataFrame 생성
records = data_json["response"]["data"]
if not records:
    print("데이터가 없습니다.")
    exit(1)

# Prophet 형식에 맞게 데이터 변환
df = pd.DataFrame(records)
df = df.rename(columns={"period": "ds", "sales": "y"})
df["ds"] = pd.to_datetime(df["ds"])
df["y"] = df["y"].astype(float)

# 3) Prophet 모델 학습 및 예측
m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m.fit(df)
future = m.make_future_dataframe(periods=12, freq="ME")  # 'M' 대신 'ME' 사용 (2025-04-18 06:01:30)
forecast = m.predict(future)

# 4) 결과 시각화
fig1 = m.plot(forecast)
plt.title("California Monthly Electricity Consumption Forecast")  # 수정: 영어 글꼴로 변경 (2025-04-18 06:00:37)
fig2 = m.plot_components(forecast)
plt.tight_layout()
plt.show()
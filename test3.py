import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 경로 직접 지정 (2025-04-19 05:49:02 적용)
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 시스템에 실제 존재하는 경로
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# --- 그래프 1: 연도별 전기차 평균 1회 충전 주행 거리 변화 (예시 데이터) ---
# 실제 데이터를 기반으로 연도별 평균 주행 거리 데이터를 구성하세요.
data_range = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Average Range (km)': [200, 220, 250, 280, 320, 380, 450, 500, 550, 600] # WLTP 기준 등 명확한 기준 사용 권장
}
df_range = pd.DataFrame(data_range)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_range, x='Year', y='Average Range (km)', marker='o')
plt.title('연도별 전기차 평균 1회 충전 주행 거리 변화', fontproperties=fontprop)
plt.xlabel('연도', fontproperties=fontprop)
plt.ylabel('평균 주행 거리 (km)', fontproperties=fontprop)
plt.grid(True)
plt.show()


# --- 그래프 2: 특정 EV 모델/기술 세대별 10% -> 80% 충전 시간 비교 (예시 데이터) ---
# 실제 데이터를 기반으로 특정 모델 또는 기술 세대의 충전 시간 데이터를 구성하세요.
data_charging_time = {
    'Model/Tech Generation': ['Early EV (50kW)', 'Mid-Gen (150kW)', 'Recent (250kW)', '800V System (350kW+)'],
    'Charging Time (10-80% in min)': [60, 40, 30, 20] # 평균적인 충전 시간. 모델 및 충전 환경에 따라 다름
}
df_charging_time = pd.DataFrame(data_charging_time)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_charging_time, x='Model/Tech Generation', y='Charging Time (10-80% in min)', palette='viridis')
plt.title('EV 모델/기술 세대별 10% -> 80% 충전 시간 비교', fontproperties=fontprop)
plt.xlabel('모델/기술 세대', fontproperties=fontprop)
plt.ylabel('충전 시간 (분)', fontproperties=fontprop)
plt.ylim(0, 70) # y축 범위 설정
plt.show()


# --- 그래프 3: 연도별 배터리 팩 평균 가격 변화 (예시 데이터) ---
# 실제 산업 보고서 (예: BloombergNEF) 기반 데이터를 구성하세요.
data_battery_price = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Average Pack Price (USD per kWh)': [400, 350, 300, 250, 200, 150, 140, 151, 139, 132] # 예시 데이터, 실제 데이터와 다를 수 있음
}
df_battery_price = pd.DataFrame(data_battery_price)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_battery_price, x='Year', y='Average Pack Price (USD per kWh)', marker='o', color='red')
plt.title('연도별 배터리 팩 평균 가격 변화', fontproperties=fontprop)
plt.xlabel('연도', fontproperties=fontprop)
plt.ylabel('평균 팩 가격 (USD/kWh)', fontproperties=fontprop)
plt.grid(True)
plt.show()


# --- 그래프 4: 연도별 글로벌 전기차 시장 점유율 변화 (예시 데이터) ---
# 실제 시장 데이터 (예: IEA, EV-volumes.com 등) 기반 데이터를 구성하세요.
data_market_share = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Global EV Market Share (%)': [0.5, 0.8, 1.2, 1.8, 2.5, 3.2, 4.8, 7.5, 10.0, 12.5] # 예시 데이터, 실제 데이터와 다를 수 있음
}
df_market_share = pd.DataFrame(data_market_share)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_market_share, x='Year', y='Global EV Market Share (%)', marker='o', color='green')
plt.title('연도별 글로벌 전기차 시장 점유율 변화', fontproperties=fontprop)
plt.xlabel('연도', fontproperties=fontprop)
plt.ylabel('시장 점유율 (%)', fontproperties=fontprop)
plt.grid(True)
plt.show()
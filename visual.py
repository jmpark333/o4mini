# visual.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    '도시': ['바르셀로나','파리','암스테르담','로마','프라하','방콕','싱가포르','도쿄','서울','홍콩'],
    '관광 성장률': [5.2,4.1,3.8,2.9,2.5,7.4,3.3,2.8,3.6,2.1],
    '최고 점유율': [88,85,80,82,78,92,90,87,89,85],
    '최저 점유율': [65,60,58,55,53,70,68,65,67,60],
    'GDP 성장률': [2.7,2.4,1.9,1.5,2.1,3.9,2.6,1.0,2.5,1.2]
}
df = pd.DataFrame(data)

# 관광 성장률
plt.figure(figsize=(8,4))
sns.barplot(x='도시', y='관광 성장률', data=df)
plt.xticks(rotation=45)
plt.title('2025 Tourism Growth Rate Comparison')  # 그래프 제목을 영어로 수정, 2025-04-18 17:41:55
plt.tight_layout()
plt.savefig('tourism_growth.png')

# 점유율 패턴
plt.figure(figsize=(8,4))
sns.lineplot(x='도시', y='최고 점유율', label='최고 점유율', data=df)
sns.lineplot(x='도시', y='최저 점유율', label='최저 점유율', data=df)
plt.xticks(rotation=45)
plt.title('Quarterly Max and Min Occupancy Rates')  # 그래프 제목을 영어로 수정, 2025-04-18 17:41:55
plt.tight_layout()
plt.savefig('occupancy_pattern.png')

# GDP 성장률
plt.figure(figsize=(8,4))
sns.barplot(x='도시', y='GDP 성장률', data=df, palette='coolwarm')
plt.xticks(rotation=45)
plt.title('2025 GDP Growth Rate Comparison')  # 그래프 제목을 영어로 수정, 2025-04-18 17:41:55
plt.tight_layout()
plt.savefig('gdp_growth.png')

plt.show()
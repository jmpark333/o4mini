import plotly.graph_objects as go

# 유럽 관광 성장률 & 점유율 데이터
cities = ["Barcelona", "Madrid", "Paris", "Amsterdam"]
growth = [4.8, 3.5, 2.2, 3.0]
occupancy = [78, 75, 82, 80]

fig = go.Figure([
    go.Bar(name="관광객 성장률 (%)", x=cities, y=growth),
    go.Bar(name="평균 점유율 (%)",   x=cities, y=occupancy)
])
fig.update_layout(
    barmode="group",
    title="유럽 후보 도시 비교",
    xaxis_title="도시",
    yaxis_title="비율 (%)"
)
fig.show()
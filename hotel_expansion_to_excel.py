# hotel_expansion_to_excel.py
# hotel_expansion_cities.xlsx 파일을 생성하는 스크립트
# 2025-04-18 16:39:56 기준 문법 오류 수정 및 주석 추가
# 2025-04-18 16:42:49 SyntaxError: unterminated string literal 문제 수정 (data 행별 문자열 닫힘 및 불필요한 괄호/대괄호 제거)

import pandas as pd

data = [
    ["방콕", "태국", 8.2, "11~3월(성수기), 6~8월(우기)", 1200, "★★★★☆", "https://www.statista.com/topics/2437/tourism-in-thailand/"],
    ["파리", "프랑스", 6.9, "4~10월(성수기)", 8700, "★★★★★", "https://en.parisinfo.com/"],
    ["도쿄", "일본", 7.5, "3~5월, 9~11월(성수기)", 2000, "★★★★☆", "https://www.jnto.go.jp/"],
    ["바르셀로나", "스페인", 5.1, "5~10월(성수기)", 1800, "★★★★☆", "https://professional.barcelonaturisme.com/"],
    ["싱가포르", "싱가포르", 9.0, "연중 고른 분포", 4000, "★★★★★", "https://www.stb.gov.sg/"],
    ["프라하", "체코", 6.3, "4~10월(성수기)", 900, "★★★★", "https://www.czechtourism.com/home/"],
    ["이스탄불", "튀르키예", 7.7, "4~10월(성수기)", 1500, "★★★★", "https://www.goturkiye.com/"],
    ["쿠알라룸푸르", "말레이시아", 8.6, "5~9월(성수기)", 700, "★★★☆", "https://www.malaysia.travel/"],
    ["시드니", "호주", 4.8, "12~2월(성수기)", 1300, "★★★★", "https://www.sydney.com/"],
    ["뉴욕", "미국", 3.9, "5~9월(성수기)", 17000, "★★★★★", "https://www.nycgo.com/"]
]

columns = [
    "도시", "국가", "관광 성장률(2024, %)", "계절별 점유율 패턴", "지역 GDP(억 달러)", "추천도", "출처"
]

df = pd.DataFrame(data, columns=columns)
df.to_excel("hotel_expansion_cities.xlsx", index=False)
print("hotel_expansion_cities.xlsx 파일이 생성되었습니다.")
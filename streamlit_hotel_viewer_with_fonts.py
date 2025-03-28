import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = fm.findfont("Malgun Gothic")  # 윈도우 기본 폰트
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 경로
data_path = "final_all"
df = pd.read_csv(data_path, encoding='euc-kr')

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# 지역 선택 (radio 스타일)
df = df.dropna(subset=['Hotel', 'Location'])  # NaN 제거
locations = df['Location'].unique()
selected_location = st.radio("지역을 선택하세요", sorted(locations), horizontal=True)

# 지역 기반 호텔 리스트
hotels = df[df['Location'] == selected_location]['Hotel'].unique()
selected_hotel = st.selectbox("호텔을 선택하세요", sorted(hotels))

# 선택한 호텔 정보 필터링
hotel_data = df[(df['Hotel'] == selected_hotel) & (df['Location'] == selected_location)].iloc[0]

# 컬럼 나누기
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ 긍정 요약")
    st.write(hotel_data['Refined_Positive'])

with col2:
    st.subheader("🚫 부정 요약")
    st.write(hotel_data['Refined_Negative'])

# 감성 점수 시각화
st.markdown("---")
st.subheader("📊 항목별 평균 점수")

aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']
aspect_scores = hotel_data[aspect_columns]

# 시각화: 음수는 빨간색, 양수는 파란색
fig, ax = plt.subplots()
colors = ['red' if val < 0 else 'skyblue' for val in aspect_scores]
ax.bar(aspect_columns, aspect_scores, color=colors)
ax.set_ylabel("점수")
ax.set_ylim(min(-1, aspect_scores.min() - 0.5), max(2, aspect_scores.max() + 0.5))
ax.set_title("호텔별 항목별 감성 점수")
st.pyplot(fig)

# Raw 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df[df['Hotel'] == selected_hotel].reset_index(drop=True))

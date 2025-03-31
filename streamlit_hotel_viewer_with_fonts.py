import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

# CSV 파일 경로
data_path = "hotel_fin_0331_1.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# NaN 제거
df = df.dropna(subset=['Hotel', 'Location', 'Latitude', 'Longitude'])

aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']

# -------------------------- 지역 선택 (본문 상단) --------------------------
locations = df['Location'].unique()
selected_location = st.radio("지역을 선택하세요", sorted(locations), horizontal=True)

# 지역 내 호텔 필터링
location_hotels_df = (
    df[df['Location'] == selected_location]
    .drop_duplicates(subset='Hotel')
    .sort_values(by='Hotel')
)

# 본문에서 호텔 selectbox 선택
selected_hotel_main = st.selectbox("📌 호텔을 직접 선택하세요", location_hotels_df['Hotel'].tolist())

# -------------------------- 사이드바 --------------------------
st.sidebar.title("🔍 항목별 상위 호텔")

# 정렬 기준 선택
aspect_to_sort = st.sidebar.selectbox("정렬 기준", aspect_columns)

# 지역 내 정렬된 호텔 리스트
sorted_hotels = (
    df[df['Location'] == selected_location]
    .sort_values(by=aspect_to_sort, ascending=False)
    .drop_duplicates(subset='Hotel')
)

# Top 5 호텔 리스트 (점수 포함 라벨)
top_hotels = sorted_hotels[['Hotel', aspect_to_sort]].head(5)
hotel_labels = [f"{row['Hotel']} - ⭐ {row[aspect_to_sort]:.2f}" for _, row in top_hotels.iterrows()]
hotel_map = dict(zip(hotel_labels, top_hotels['Hotel']))
selected_hotel_label = st.sidebar.radio("상위 호텔 선택", hotel_labels)

# ✅ 최종 선택 호텔: 본문 selectbox에서 고른 호텔이 우선
selected_hotel = selected_hotel_main or hotel_map[selected_hotel_label]

# -------------------------- 지도 --------------------------
st.markdown("---")
st.subheader("📍 호텔 위치 지도")

region_hotels = df[df['Location'] == selected_location].drop_duplicates(subset='Hotel')
region_hotels['색상'] = region_hotels['Hotel'].apply(
    lambda x: [0, 0, 255] if x == selected_hotel else [255, 0, 0]
)

hotel_layer = pdk.Layer(
    'ScatterplotLayer',
    data=region_hotels,
    get_position='[Longitude, Latitude]',
    get_fill_color='색상',
    get_radius=200,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=region_hotels['Latitude'].mean(),
    longitude=region_hotels['Longitude'].mean(),
    zoom=12,
    pitch=0
)

st.pydeck_chart(pdk.Deck(
    layers=[hotel_layer],
    initial_view_state=view_state,
    tooltip={"text": "{Hotel}"}
))

# -------------------------- 호텔 요약 --------------------------
hotel_data = df[(df['Hotel'] == selected_hotel) & (df['Location'] == selected_location)].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ 긍정 요약")
    st.write(hotel_data['Refined_Positive'])

with col2:
    st.subheader("🚫 부정 요약")
    st.write(hotel_data['Refined_Negative'])

# -------------------------- 항목별 점수 시각화 --------------------------
st.markdown("---")
st.subheader("📊 항목별 평균 점수")

aspect_scores = hotel_data[aspect_columns]

plot_df = pd.DataFrame({
    "항목": aspect_columns,
    "점수": aspect_scores.values,
    "색상": ['#FF6B6B' if v < 0 else '#4EA8DE' for v in aspect_scores.values]
})

chart = alt.Chart(plot_df).mark_bar().encode(
    x=alt.X('항목:N', sort=None),
    y=alt.Y('점수:Q'),
    color=alt.Color('색상:N', scale=None)
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)

# -------------------------- 원본 데이터 --------------------------
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df[df['Hotel'] == selected_hotel].reset_index(drop=True))




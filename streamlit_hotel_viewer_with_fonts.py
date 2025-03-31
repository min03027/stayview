import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

# CSV 파일 경로
data_path = "hotel_fin_0331_1.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

# 도시별 중심 좌표
region_coords = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8722, 128.6025),
    "전주": (35.8242, 127.1480),
    "제주": (33.4996, 126.5312),
    "강릉": (37.7519, 128.8761),
    "속초": (38.2044, 128.5912),
    "경주": (35.8562, 129.2247),
    "여수": (34.7604, 127.6622),
}

st.set_page_config(page_title="호텔 리뷰 감성 요약", layout="wide")
st.title("🏨 호텔 리뷰 요약 및 항목별 분석")

# 분석 항목
aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']

# -------------------------- 지역 선택 --------------------------
regions = df['Location'].unique()
selected_region = st.radio("📍 지역을 선택하세요", sorted(regions), horizontal=True)

# 해당 지역 호텔 필터링
region_df = df[df['Location'] == selected_region]
region_hotels = region_df['Hotel'].unique()

# -------------------------- 호텔 선택 --------------------------
selected_hotel = st.selectbox("🏨 호텔을 선택하세요", ["전체 보기"] + list(region_hotels))

# -------------------------- 사이드바 --------------------------
st.sidebar.title("🔍 항목별 상위 호텔")

# 정렬 기준 선택
aspect_to_sort = st.sidebar.selectbox("정렬 기준", aspect_columns)

# 정렬된 호텔 리스트 (중복 제거)
sorted_hotels = (
    region_df.sort_values(by=aspect_to_sort, ascending=False)
    .drop_duplicates(subset='Hotel')
)

# 상위 5개 출력
top_hotels = sorted_hotels[['Hotel', aspect_to_sort]].head(5)
st.sidebar.markdown("#### 🏅 정렬 기준 Top 5")
for idx, row in enumerate(top_hotels.itertuples(), 1):
    st.sidebar.write(f"**{idx}등!** {row.Hotel} - ⭐ {getattr(row, aspect_to_sort):.2f}")

# -------------------------- 색상 설정 --------------------------
def get_color(hotel):
    if selected_hotel == "전체 보기":
        return [30, 144, 255, 255]  # 파란색 (선택 없음)
    elif hotel == selected_hotel:
        return [255, 0, 0, 255]     # 선택한 호텔: 빨간색
    else:
        return [180, 180, 180, 80]  # 나머지: 투명한 회색

region_df["color"] = region_df["Hotel"].apply(get_color)

# -------------------------- 지도 표시 --------------------------
# 지도 데이터는 region_df를 사용 (pydeck)
layer = pdk.Layer(
    "ScatterplotLayer",
    data=region_df,
    get_position='[Longitude, Latitude]',
    get_color="color",
    get_radius=80,
    pickable=True,
)

mid_lat = region_df["Latitude"].mean()
mid_lon = region_df["Longitude"].mean()

view_state = pdk.ViewState(
    latitude=mid_lat,
    longitude=mid_lon,
    zoom=11,
    pitch=0
)

# 만약 "전체 보기" 선택 시에는 메인 지도만 표시
if selected_hotel == "전체 보기":
    st.subheader(f"🗺️ {selected_region} 지역 호텔 지도")
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{Hotel}"}
    ))
else:
    # 선택된 호텔의 데이터 추출 (상세 정보용)
    hotel_data = region_df[region_df['Hotel'] == selected_hotel].iloc[0]
    
    # 메인 지도와 미니맵을 양옆에 배치 (컬럼 배치)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🗺️ {selected_region} 지역 호텔 지도")
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{Hotel}"}
        ))
    
    with col2:
        st.subheader(f"📍 '{selected_hotel}' 위치 미리보기")
        st.map(pd.DataFrame({
            'lat': [hotel_data['Latitude']],
            'lon': [hotel_data['Longitude']]
        }))
    
    # -------------------------- 호텔 상세 정보 --------------------------
    st.markdown("### ✨ 선택한 호텔 요약")
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
    score_df = pd.DataFrame({
        '항목': aspect_scores.index,
        '점수': aspect_scores.values
    })
    chart = alt.Chart(score_df).mark_bar().encode(
        x=alt.X('항목', sort=None),
        y='점수',
        color=alt.condition(
            alt.datum.점수 < 0,
            alt.value('crimson'),
            alt.value('steelblue')
        )
    ).properties(width=600, height=400)
    st.altair_chart(chart, use_container_width=True)

# -------------------------- 원본 데이터 보기 --------------------------
with st.expander("📄 원본 데이터 보기"):
    if selected_hotel == "전체 보기":
        st.dataframe(region_df.reset_index(drop=True))
    else:
        st.dataframe(region_df[region_df['Hotel'] == selected_hotel].reset_index(drop=True))





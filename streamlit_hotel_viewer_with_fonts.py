import streamlit as st
import pandas as pd
import altair as alt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit as st
from PIL import Image

# CSV 파일 경로
data_path = "hotel_fin_0331_2.csv"
df = pd.read_csv(data_path, encoding='euc-kr')

# 페이지 설정
st.set_page_config(layout="wide")

# 배경 이미지
st.image("image.png", use_column_width=True)

# 상단 타이틀 + 부제
st.markdown("""
<style>
.big-title {
    font-size: 64px;
    font-weight: 900;
    color: black;
    margin-bottom: 0;
}
.sub-title {
    font-size: 36px;
    font-weight: 600;
    color: black;
    margin-top: 0;
}
.date-box {
    text-align: right;
    font-size: 14px;
    margin-top: -40px;
    color: #555;
}
.top-nav {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 10px;
}
.orange-circle {
    width: 120px;
    height: 120px;
    border-radius: 60px;
    background-color: #f97316;
    color: white;
    text-align: center;
    padding-top: 35px;
    font-weight: bold;
    position: absolute;
    left: 30px;
    top: 200px;
}
</style>

<div class="top-nav">PROFESSIONAL &nbsp;&nbsp;&nbsp; DATA</div>

<div class="big-title">Stay-view</div>
<div class="sub-title">리뷰 요약 기반 숙소 추천 AI</div>
<div class="date-box">Ai hotel recommendation<br>2025.04.14</div>

<div class="orange-circle">
권지원<br>김정민<br>김지민
</div>
""", unsafe_allow_html=True)

# 감성 항목
aspect_columns = ['소음', '가격', '위치', '서비스', '청결', '편의시설']

# ---------------- 지역 선택 ----------------
regions = sorted(df['Location'].unique())
selected_region = st.radio("📍 지역을 선택하세요", regions, horizontal=True)

region_df = df[df['Location'] == selected_region]
hotels = region_df['Hotel'].unique()
selected_hotel = st.selectbox("🏠 호텔을 선택하세요", ["전체 보기"] + list(hotels))

# ---------------- 사이드바: 정렬 기준 및 Top 5 ----------------
st.sidebar.title("🔍 항목별 상위 호텔")
aspect_to_sort = st.sidebar.selectbox("정렬 기준", aspect_columns)

sorted_hotels = (
    region_df.sort_values(by=aspect_to_sort, ascending=False)
    .drop_duplicates(subset='Hotel')
)

top_hotels = sorted_hotels[['Hotel', aspect_to_sort]].head(5)
st.sidebar.markdown("#### 🏅 정렬 기준 Top 5")
for idx, row in enumerate(top_hotels.itertuples(), 1):
    st.sidebar.write(f"👑**{idx}등!** {row.Hotel}")

# ---------------- 구글 지도 생성 함수 ----------------
def create_google_map(dataframe, zoom_start=12):
    center_lat = dataframe['Latitude'].mean()
    center_lon = dataframe['Longitude'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=zoom_start, 
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", 
        attr="Google"
    )
    
    if len(dataframe) > 1:
        marker_cluster = MarkerCluster().add_to(m)
        for idx, row in dataframe.iterrows():
            tooltip = f"{row['Hotel']}"
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=tooltip,
                icon=folium.Icon(color='blue', icon='hotel', prefix='fa')
            ).add_to(marker_cluster)
    else:
        for idx, row in dataframe.iterrows():
            tooltip = f"{row['Hotel']}"
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=tooltip,
                popup=f"<strong>{row['Hotel']}</strong>",
                icon=folium.Icon(color='red', icon='hotel', prefix='fa')
            ).add_to(m)
    
    return m

# ---------------- 지도 출력 ----------------
if selected_hotel == "전체 보기":
    st.subheader(f"🗺️ {selected_region} 지역 호텔 지도")
    map_df = region_df[['Hotel', 'Latitude', 'Longitude']].dropna()
    if not map_df.empty:
        m = create_google_map(map_df)
        folium_static(m, width=800)
    else:
        st.warning("지도에 표시할 위치 정보가 없습니다.")
else:
    st.subheader(f"🗺️ '{selected_hotel}' 위치")
    hotel_data = region_df[region_df['Hotel'] == selected_hotel].iloc[0]
    hotel_map_df = pd.DataFrame({
        'Hotel': [selected_hotel],
        'Latitude': [hotel_data['Latitude']],
        'Longitude': [hotel_data['Longitude']]
    })
    m = create_google_map(hotel_map_df, zoom_start=15)
    folium_static(m, width=800)

    # ---------------- 호텔 정보 ----------------
    st.markdown("### ✨ 선택한 호텔 요약")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ 긍정 요약")
        st.write(hotel_data['Refined_Positive'])
    with col2:
        st.subheader("🚫 부정 요약")
        st.write(hotel_data['Refined_Negative'])

    # ---------------- 항목별 점수 ----------------
    st.markdown("---")
    st.subheader("📊 항목별 평균 점수")

    scores = hotel_data[aspect_columns]
    score_df = pd.DataFrame({
        "항목": aspect_columns,
        "점수": scores.values
    })

    chart = alt.Chart(score_df).mark_bar().encode(
        x=alt.X('항목', sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('점수', axis=alt.Axis(titleAngle=0)),
        color=alt.condition(
            alt.datum.점수 < 0,
            alt.value('crimson'),
            alt.value('steelblue')
        )
    ).properties(width=600, height=400)

    st.altair_chart(chart, use_container_width=True)

# ---------------- 원본 데이터 보기 ----------------
with st.expander("📄 원본 데이터 보기"):
    if selected_hotel == "전체 보기":
        st.dataframe(region_df.reset_index(drop=True))
    else:
        st.dataframe(region_df[region_df['Hotel'] == selected_hotel].reset_index(drop=True))


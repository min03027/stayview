
# 🏨 Stay-view: 호텔 리뷰 요약 기반 숙소 추천 시스템

Streamlit과 지도 기반 시각화를 활용한 **AI 호텔 리뷰 요약 및 추천 시스템**입니다.  
숙소별 리뷰를 긍정/부정으로 요약하고, 항목별 평점을 시각화하며 지도 기반으로 탐색할 수 있는 기능을 제공합니다.

---

## 🎯 개발 목적

- 호텔 선택 시 유용한 정보를 시각적으로 쉽게 제공
- 리뷰 기반으로 긍정/부정 요약을 제공하여 사용자의 결정 지원
- Streamlit과 Folium을 활용한 직관적인 지도 기반 탐색 제공

---

## ⚙️ 주요 기능

- **Streamlit 기반 인터페이스**로 지역과 호텔 선택 가능
- **긍정/부정 리뷰 요약문** 시각화
- **소음, 가격, 위치, 서비스, 청결, 편의시설** 6개 항목별 평균 점수 제공
- **구글 지도 연동 지도 시각화** (호텔 정보, 길찾기 링크 포함)
- **사이드바에서 항목별 정렬 기준 설정 및 Top 5 호텔 확인 가능**

---

## 🛠 개발 환경

| 항목 | 내용 |
|------|------|
| 개발 언어 | Python 3.11 |
| 주요 라이브러리 | `streamlit`, `pandas`, `folium`, `altair`, `Pillow`, `streamlit-folium` |
| 사용 데이터 | `hotel_fin_0331_2.csv` (euc-kr 인코딩) |
| 운영 체제 | Windows / Mac / Linux 호환 가능 |

---

## 🚀 실행 방법

### 1️⃣ 라이브러리 설치

```bash
pip install streamlit pandas folium altair Pillow streamlit-folium
```

### 2️⃣ 실행

```bash
streamlit run streamlit_hotel_viewer_with_fonts.py
```

- `image.png`, `hotel_fin_0331_2.csv` 파일이 동일 경로에 있어야 함

---

## 🧭 작동 흐름 요약

```plaintext
지역 선택
  ↓
호텔 선택
  ↓
긍정/부정 요약 표시 + 점수 시각화
  ↓
지도 기반 호텔 위치 출력 + 구글 지도 연결
```

---

## 📊 시각화 예시

- Altair를 이용한 항목별 막대 시각화
- folium + MarkerCluster를 활용한 지도 클러스터링

---

## 🗂 파일 구성

| 파일명 | 설명 |
|--------|------|
| `streamlit_hotel_viewer_with_fonts.py` | 메인 실행 파일 |
| `hotel_fin_0331_2.csv` | 호텔 리뷰 및 점수 데이터 |
| `image.png` | 상단 배너용 이미지 |
| `README.md` | 프로젝트 설명 파일 |

---

## 📌 참고

- 리뷰 요약은 사전 분석된 텍스트로 구성됨 (`Refined_Positive`, `Refined_Negative`)
- 데이터는 지역(제주 등) 기반으로 분류되어 있음

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 및 타이틀 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 변화 및 추세를 시각화합니다.")

# 2. 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # YYYYMMDD 형태의 숫자를 real datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치 데이터 형변환
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
    st.sidebar.success(f"데이터 로드 완료! (총 {len(df):,}건)")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 사이드바 구성
st.sidebar.header("📌 도감 목차")
st.sidebar.markdown("- **1구역**: 개별 영화 날짜별 일관객 변화")
st.sidebar.markdown("- **2구역**: (추가 예정)")
st.sidebar.markdown("- **3구역**: (추가 예정)")

st.divider()

# ==========================================
# 구역 1: 개별 영화의 날짜별 일관객 변화
# ==========================================
st.header("1️⃣ 개별 영화의 날짜별 일관객 변화")
st.caption("특정 영화를 선택하여 개봉 후 일자별 관객수 추이를 확인합니다.")

# 영화 목록 추출 및 선택 드롭다운
movie_list = sorted(df['영화명'].dropna().unique())
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 데이터 필터링 및 날짜순 정렬
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
    
    # Plotly 선 그래프 생성
    fig = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객 추이",
        markers=True,
        custom_data=['순위', '누적관객']
    )
    
    # 마우스 오버(호버) 시 날짜, 일관객, 순위, 누적관객 표시 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<br><b>누적관객:</b> %{customdata[1]:,}명<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )
    
    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 그래프 해석 문구 공간
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 일일 관객 수 변화 추이 및 주말/평일 관객 격차를 한눈에 확인할 수 있습니다.")

st.divider()

# ==========================================
# 구역 2: [추가 그래프 예정 구역]
# ==========================================
st.header("2️⃣ [추가 예정] 시간 흐름에 따른 관객 분석")
st.info("🚧 새로운 시각화 그래프가 여기에 추가될 예정입니다.")

st.divider()

# ==========================================
# 구역 3: [추가 그래프 예정 구역]
# ==========================================
st.header("3️⃣ [추가 예정] 주말 vs 평일 추이 비교")
st.info("🚧 새로운 시각화 그래프가 여기에 추가될 예정입니다.")

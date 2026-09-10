import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 변화 및 추세를 시각화합니다.")

# 데이터 로드 및 전처리 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 정리
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

# 사이드바 안내 및 필터
st.sidebar.header("📌 도감 목차")
st.sidebar.markdown("- **1구역**: 개별 영화의 날짜별 일관객 변화")
st.sidebar.markdown("- **2구역**: 일관객 합계 Top 5 영화의 추이 비교")
st.sidebar.markdown("- **3구역**: 날짜별 Top 10 관객 합계 추이")

st.divider()

# ==========================================
# 구역 1: 개별 영화 날짜별 일관객 변화
# ==========================================
st.header("1️⃣ 개별 영화의 날짜별 일관객 변화")
st.caption("특정 영화를 선택하여 개봉 후 일자별 관객수 추이를 확인합니다.")

# 영화 목록 추출 및 선택 드롭다운
movie_list = sorted(df['영화명'].dropna().unique())
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택한 영화 데이터 필터링 및 날짜순 정렬
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
    
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객 추이",
        markers=True,
        custom_data=['순위', '누적관객']
    )
    
    # 그래프 레이아웃 및 툴팁 서식 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<br><b>누적관객:</b> %{customdata[1]:,}명<extra></extra>"
    )
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )
    
    # Streamlit에 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)
    
    # 사용자 작성용 '이 그래프로 알 수 있는 것' 빈 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 작성할 문구를 입력하세요)")

st.divider()

# ==========================================
# 구역 2: 일관객 합계 Top 5 영화의 날짜별 일관객 추이
# ==========================================
st.header("2️⃣ 기간 내 일관객 합계 Top 5 영화의 추이 비교")
st.caption("해당 기간 일관객 합계가 가장 큰 5편의 영화를 선정하여 일별 관객 수 추이를 비교합니다. 오른쪽 범례 항목을 클릭하여 특정 영화 선을 켜고 끌 수 있습니다.")

# 일관객 합계 상위 5개 영화 선정
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# Top 5 영화 데이터 필터링 및 날짜순 정렬
top5_df = df[df['영화명'].isin(top5_movies)].sort_values(['날짜', '영화명'])

# Plotly 다중 선 그래프 생성
fig2 = px.line(
    top5_df,
    x='날짜',
    y='일관객',
    color='영화명',
    title="기간 내 일관객 합계 Top 5 영화 일관객 추이 비교",
    markers=True,
    custom_data=['순위', '누적관객']
)

# 호버 서식 및 레이아웃 설정
fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위<br><b>누적관객:</b> %{customdata[1]:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객 수 (명)",
    hovermode="x unified",
    template="plotly_white",
    legend_title_text="영화명 (클릭하여 토글)"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 사용자 작성용 '이 그래프로 알 수 있는 것' 빈 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 작성할 문구를 입력하세요)")

st.divider()

# ==========================================
# 구역 3: 날짜별 10위권 일관객 합계 영역 그래프
# ==========================================
st.header("3️⃣ 날짜별 10위권 일관객 총합 추이")
st.caption("매일 박스오피스 Top 10 영화들의 일관객 합계를 계산하여 영역 그래프(Area Chart)로 표시합니다. 일관객 합계가 가장 컸던 상위 3일이 강조되어 표시됩니다.")

# 날짜별 10위권 일관객 합계 데이터 집계
daily_sum = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

# 영역 그래프 생성
fig3 = px.area(
    daily_sum,
    x='날짜',
    y='일관객',
    title="날짜별 BoxOffice Top 10 일관객 총합 추이",
    markers=False
)

fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>10위권 총 관객수:</b> %{y:,}명<extra></extra>",
    fillcolor="rgba(31, 119, 180, 0.3)",
    line=dict(color="#1f77b4", width=2)
)

# Top 3 관객수 많은 날 추출
top3_days = daily_sum.nlargest(3, '일관객').sort_values('일관객', ascending=False)

# 그래프 상에 Top 3 주석(Annotation) 및 마커 추가
rank_labels = ["🥇 1위", "🥈 2위", "🥉 3위"]
for idx, (_, row) in enumerate(top3_days.iterrows()):
    date_str = row['날짜'].strftime('%Y-%m-%d')
    audience_cnt = int(row['일관객'])
    
    # 강조 포인트 마커 표기
    fig3.add_scatter(
        x=[row['날짜']],
        y=[audience_cnt],
        mode='markers+text',
        marker=dict(size=10, color='red', symbol='circle'),
        showlegend=False,
        hoverinfo='skip'
    )
    
    # 주석 텍스트 추가 (순위, 날짜, 관객 수)
    fig3.add_annotation(
        x=row['날짜'],
        y=audience_cnt,
        text=f"<b>{rank_labels[idx]} ({date_str})</b><br>{audience_cnt:,}명",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="red",
        ax=0,
        ay=-45 - (idx * 10),
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.9
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="Top 10 관객 합계 (명)",
    hovermode="x unified",
    template="plotly_white"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 사용자 작성용 '이 그래프로 알 수 있는 것' 빈 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 작성할 문구를 입력하세요)")

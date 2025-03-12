import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl   # 한글 폰트 설정
import seaborn as sns
import plotly.express as px

import streamlit as st

from utils import make_donut

# 배너 이름/아이콘(맨 윗줄에 위치)
st.set_page_config(
    layout = 'wide',
    page_title = 'Semiconductor Dashboard',
    page_icon=":computer:"
)

# # 주기적으로 자동 새로고침 (1000ms=1초, 60000=1분, 3600000=1시간)
# st_autorefresh(interval=3600000, key="refresh")

# 스트림릿 상단 메뉴 바/하단 Made with Streamlit 숨김
st.markdown(
    """
    <style>
        footer {display: none}     /* Streamlit의 기본 푸터(하단 Made with Streamlit 문구)를 숨김 */
        [data-testid="stHeader"] {display: none}     /* Streamlit의 기본 헤더(상단 메뉴 바)를 숨김 */
    </style>
    """, unsafe_allow_html = True
)


# st.title("Dashboard")
# st.write("자세한 분석은 왼쪽 사이드바를 선택하세요.")

# df_eqp = st.session_state["df_eqp"]
df_oxid = st.session_state["df_oxid"]
df_sorted = df_oxid['No_Die'].value_counts().sort_values(ascending=False)





################################ 사이드바 ################################
with st.sidebar:

    # clr_btn = st.button("대화 초기화")  # 대화 내용을 초기화하는 버튼
    # 공정 선택 selectbox
    process = st.selectbox(
        "process 선택",
        df_oxid['process'].unique()
        )
    df_oxid = df_oxid[df_oxid["process"]==process]

    # # CSV 파일 업로드
    # uploaded_file = st.file_uploader(
    #     "csv 파일을 업로드 해주세요.", type=['csv'], accept_multiple_files=False)
    # print("/n", "업로드된 파일:", uploaded_file, "/n")

    # # 대시보드 생성 버튼
    # apply_btn = st.button("대시보드 생성")  

########################### 1번째 컨테이너 ###########################

st.markdown('#### Basic statistics')
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(label = "Oxid_time",
        value = df_oxid['Oxid_time'].mean().round(1),
        delta = 12.4)

c2.metric(label = "ppm",
            value = df_oxid['ppm'].mean().round(1),
            delta = -5)

c3.metric(label = "Pressure",
            value = df_oxid['Pressure'].mean().round(1),
            delta = 0.1)

# st.dataframe(df_oxid.head())
# st.dataframe(df_oxid[df_oxid["process"]==process].head())

# st.write("#### 데이터 타입 확인")
# st.write(df_oxid.dtypes)


st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)
########################### 2번째 컨테이너 ###########################

c6, c7, c8, c9, c10 = st.columns([0.8, 2, 0.2, 1, 0.01])

# Donut chart 생성
c6.markdown('#### Error rate')
donut_chart_greater = make_donut(55, 'Error rate', 'green')
c6.write('Dry Oxidation')
c6.altair_chart(donut_chart_greater)

c6.write('Wet Oxidation')
donut_chart_less = make_donut(80, 'Error rate', 'red')
c6.altair_chart(donut_chart_less)

# Scatter chart 생성
c7.markdown('#### Etching rate & Errors')
fig_scatter = px.scatter(df_oxid, x='ppm', y='Pressure', 
                color='type', 
            #  labels={'sepal_width':'Sepal width', 
            #        'sepal_length':'Sepal length'}, 
            #  title='Correlation between BMI and charges of smokers' 
    )
fig_scatter.update_layout(width=500, height=500)  # 그래프 사이즈 조절
c7.plotly_chart(fig_scatter, use_container_width=True)

# DataFrame 생성
c9.markdown('#### No_Dies')
# st.markdown("<br><br>", unsafe_allow_html=True)
c9.dataframe(df_sorted, 
            column_config={
                "Name": st.column_config.TextColumn(
                    "Name",
                ),
                "Fare_int": st.column_config.ProgressColumn(
                    "Fare",
                    format="%f",
                    min_value=0,
                    # max_value=max(fare_sorted["Fare_int"]),
                    )}
                )






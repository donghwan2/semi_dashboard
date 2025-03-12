import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl   # 한글 폰트 설정
import seaborn as sns
import plotly.express as px

import streamlit as st

# # 상단 마진/패딩 제거하는 CSS 적용
# st.markdown("""
#     <style>
#         /* 기본 여백 제거 */
#         .block-container {
#             padding-top: 0px !important;
#         }
#     </style>
# """, unsafe_allow_html=True)

# 분석 목표
# inspection_step 별 px.bar() - inspection_step 별 count 확인
# 날짜 별 value px.scatter() by inspection_step - step 별 value 차이 비교
# px.scatter() 기반 Control Chart - spec out 확인

# 제목
st.title('Fab_control_chart')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_inspect = pd.read_csv('data/inspection.csv')

# 세션 스테이트에 데이터 저장
if "df_inspect" not in st.session_state:
    st.session_state["df_inspect"] = df_inspect

st.write("#### 데이터 확인")
st.write("날짜, 검사 단계, 검사값, 상한선, 목표값, 하한선 등의 정보를 담고 있습니다.")
st.write(df_inspect.shape)
st.dataframe(df_inspect.head())

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_inspect.dtypes)

################# 데이터 전처리 #################
# 결측치 확인
st.write("#### 결측치 확인")
st.dataframe(df_inspect.isnull().sum())
# df = df.dropna()

################# 날짜 데이터 다루기 #################
st.write("#### 날짜 데이터 타입 변환") 

# 시간 컬럼 datetime 형식으로 변환
df_inspect['date'] = pd.to_datetime(df_inspect['date'], errors='coerce')  # 에러 시 NaT(Not a Time)로 처리
df = df_inspect.sort_values(['date'])

st.dataframe(df_inspect)
st.write(df_inspect.dtypes)
st.markdown("<br><br>", unsafe_allow_html=True)

################# inspection_step 바차트 #################

# inspection_step count 내림차순 정렬
inspection_step_sort = df_inspect['inspection_step'].value_counts().sort_values(ascending=False)

# inspection_step count bar chart
st.write("#### inspection_step 별 count") 
fig = px.bar(x=inspection_step_sort.index, y=inspection_step_sort.values)
st.plotly_chart(fig, use_container_width=True)

################# 날짜 별 value 산점도 #################

# 날짜 별 value 산점도
st.write("#### value 산점도")
fig_value = px.scatter(df_inspect, x='date', y='value',
                )
st.plotly_chart(fig_value, use_container_width=True)

# 검사 스텝 별 value 산점도
st.write("#### step 별 value 산점도")
fig = px.scatter(df_inspect, x='date', y='value',
                facet_col='inspection_step', facet_col_spacing=0.1
                )   # facet_col : 컬럼 별 차트 그리기

# fig.update_yaxes(matches=None)          # y축 통일(match) 여부
fig.update_yaxes(showticklabels=True)   # y축 눈금 표시 여부
st.plotly_chart(fig, use_container_width=True)

################# 관리도 차트 #################

st.write("#### step 별 value 산점도 + Control chart")

# 산점도(inspection_step 구분, 관리선 추가)
fig = px.scatter(df_inspect, x='date', y='value',
                facet_col='inspection_step', facet_col_spacing=0.1
                )   # facet_col : 컬럼 별 차트 그리기

for idx in range(df_inspect['inspection_step'].nunique()):
    step = fig.layout.annotations[idx].text.split('=')[1]
    # st.write(step)   # A, B, C 
    
    fig.add_hline(    # 하한선 추가 
        y = df_inspect.query('inspection_step == @step')['lower_spec'].iloc[-1],
        line_color='red', line_width=0.5, row=1, col=idx+1
    )
    
    fig.add_hline(    # 상한선 추가
        y = df_inspect.query('inspection_step == @step')['upper_spec'].iloc[-1],
        line_color='red', line_width=0.5, row=1, col=idx+1
    )
    
    fig.add_hline(    # 타겟값 추가
        y = df_inspect.query('inspection_step == @step')['target'].iloc[-1],
        line_color='red', line_width=0.5, row=1, col=idx+1
    )

fig.update_yaxes(matches=None)          # y축 통일 여부
fig.update_yaxes(showticklabels=True)   # y축 눈금 표시 여부

st.plotly_chart(fig, use_container_width=True)







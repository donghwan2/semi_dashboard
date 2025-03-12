# fc 반도체 P4_CH3 groupby - 불량 유발 공정 찾아내기
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
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
# 장비별 stepA_CD px.box() - eqp 별 CD 차이 확인


# 제목
st.title('CD 품질 이슈 설비 찾기')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_eqp = pd.read_csv('data/eqp.csv')

# 세션 스테이트에 데이터 저장
if "df_eqp" not in st.session_state:
    st.session_state["df_eqp"] = df_eqp

st.write("#### 데이터 확인")
st.write("Line, eqp, lottype, step 별 CD, THK 데이터")
st.write(df_eqp.shape)
st.dataframe(df_eqp.head())

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_eqp.dtypes)

################# 데이터 전처리 #################
# 결측치 확인
st.write("#### 결측치 확인 및 처리")
st.dataframe(df_eqp.isnull().sum())
df_eqp = df_eqp.dropna()

################# stepA 상자그림 #################

# eqp A, B, C 각각 stepA_CD 상자그림
st.write("#### 장비별 stepA_CD 분포")
fig = px.box(
    data_frame=df_eqp, x='eqp', y='stepA_CD',
    width=650, height=400, points='all'
)\
# .update_yaxes(range=[-150, 200])

st.plotly_chart(fig, use_container_width=True)


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
# Oxid_time strip plot - 마이너스 이상치 확인
# Temp_OXid(산화 온도) 히스토그램 - type(공정 타입; dry, wet)별 차이 확인
# type & vapor groupby - dry 공정은 o2, wet 공정은 h2o 사용하는지 확인


# 제목
st.title('Oxidation ')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_oxid = pd.read_csv('data/Oxid_000.csv')

# 세션 스테이트에 데이터 저장
if "df_oxid" not in st.session_state:
    st.session_state["df_oxid"] = df_oxid

st.write("#### 데이터 확인")
st.write("Oxidation 공정 데이터")
st.write(df_oxid.shape)
st.dataframe(df_oxid.head())

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_oxid.dtypes)

################# 데이터 전처리 #################
# 결측치 확인
st.write("#### 결측치 확인 및 처리")
st.dataframe(df_oxid.isnull().sum())
df_oxid = df_oxid.dropna()

################# 기초통계량 확인 #################
st.write("#### 변수 별 기초통계량 확인")
# 변수 별 기초통계량 확인
st.dataframe(df_oxid.describe())
st.write("""
         -> Oxid_time 에 마이너스 값이 존재. 이상치로 처리 필요
""")

################# 날짜 데이터 다루기 #################
st.write("#### 날짜 데이터 타입 변환") 

# 시간 컬럼 datetime 형식으로 변환
df_oxid['Datetime'] = pd.to_datetime(df_oxid['Datetime'], 
                                     format="%d-%m-%Y %p %I:%M:%S", errors='coerce')  
                                    # coerce : 에러 시 NaT(Not a Time)로 처리
df_oxid = df_oxid.sort_values(['Datetime'])

st.dataframe(df_oxid)
st.write(df_oxid.dtypes)
st.markdown("<br><br>", unsafe_allow_html=True)

################# Oxid_time 분포 분석 #################
st.write("#### Oxid_time 분포 분석")  
fig = px.strip(df_oxid, x='Oxid_time') 
st.plotly_chart(fig, use_container_width=True) 

# 마이너스 값 제거
df_oxid = df_oxid[df_oxid['Oxid_time'] >= 0]

st.write("""
-> Oxid_time 마이너스 값 이상치 제거 완료
         """)

################# Temp_OXid 분포 분석 #################
st.write("#### Temp_OXid 히스토그램")  
fig2 = plt.figure(figsize=(6, 6))  # 새로운 Figure 생성
sns.histplot(data=df_oxid, x='Temp_OXid', hue='type')
st.pyplot(fig2)  # seaborn 그래프를 streamlit에 출력
st.write("""
-> wet 공정이 dry 공정보다 산화 온도가 높은 경향이 있음
         """)

################# type(dry, wet)과 vapor(o2, h2o) 사용 분석 #################
st.write("#### type(dry, wet)과 vapor(o2, h2o) 사용 분석")  
st.dataframe(df_oxid.groupby(['type', 'Vapor']).size())  
             # size는 전체 데이터 수, count는 컬럼별 데이터 수
st.write("""
-> dry 공정은 o2를 사용, wet 공정은 h2o를 사용하는 것을 알 수 있음
         """)

# 분석 후 데이터 세션 스테이트에 저장
st.session_state["df_oxid"] = df_oxid









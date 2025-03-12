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
# 제품별 생산량 px.bar() - 제품 생산량 순위 확인
# lottype px.bar() - lottype 별 생산량 확인(MP: 양산, Eng: 개발)
# lottype_product 별 결함(defectcount) groupby 평균 - 제품 별 결함 비교
# lottype_product vs 결함 px.scatter() with Trendline - 상관관계 파악

# 제목
st.title('Semiconductor process defect analysis')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_product = pd.read_csv("data/product_inspection.csv")

# 세션 스테이트에 데이터 저장
if "df_product" not in st.session_state:
    st.session_state["df_product"] = df_product

st.write("#### 데이터 확인")
st.write("시작 시간, 종료 시간, lottype, product, defectcount(결함 개수) 등의 정보를 담고 있습니다.")
st.write(df_product.shape)
st.dataframe(df_product.head(20))

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_product.dtypes)
# 시간 데이터가 Object -> datetime으로 변경 필요

################# 데이터 전처리 #################
# 결측치 확인
st.write("#### 결측치 확인 및 처리")
st.write(df_product.isnull().sum())
df_product = df_product.dropna()

################# 날짜 데이터 다루기 #################
st.write("#### 날짜 데이터") 

# 시간 컬럼 datetime 형식으로 변환
# errors='coerce' : 변환할 수 없는 값이 있으면 오류내는 대신 NaT(결측치)로 변환
df_product['start_time'] = pd.to_datetime(df_product['start_time'], errors='coerce')
df_product['end_time'] = pd.to_datetime(df_product['end_time'], errors='coerce')

df_product = df_product.sort_values(['start_time', 'end_time'])

st.dataframe(df_product)
st.write(df_product.dtypes)
st.markdown("<br><br>", unsafe_allow_html=True)

################# product 확인 #################

# product count 내림차순 정렬
product_sort = df_product['product'].value_counts().\
sort_values(ascending=False)

# product count bar chart
st.write("#### 제품별 생산량") 
fig = px.bar(x=product_sort.index, y=product_sort.values)
st.plotly_chart(fig, use_container_width=True)


################# lottype 별 결함(defectcount) 확인 #################

# lottype 고유값 확인
lottype_sort = df_product['lottype'].value_counts().sort_values(ascending=False)

st.write("#### lottype - Mass Product(양산 제품), Eng(개발 제품) ") 
fig = px.bar(x=lottype_sort.index, y=lottype_sort.values) 
st.plotly_chart(fig, use_container_width=True) 


# lottype_product 별 결함(defectcount) 수 비교
# 가설 : lottype_product 별로 defectcount(결함 개수) 가 다를 것이다.
st.write("#### lottype_product 별 결함(defectcount) 통계량")
group_defect = df_product.groupby(['lottype', 'product'])['defectcount'].agg(['mean', 'std', 'count'])
st.dataframe(group_defect)

# 인사이트
st.write("""test_vehicle_A가 다른 제품들보다 defectcount(결함 개수) 평균이 낮다. 수율이 더 좋다.  
MP(Mass Production, 양산) 단계에서도 불량 편차가 크다.  
-> 양산 공정이 아직 최적화되지 않았음을 의미.
""")

st.markdown("<br>", unsafe_allow_html=True)

################# 파생변수 생성 및 상관관계 파악 #################

# inspection_time(검사 시간, time delta) 파생변수 추가
st.write("### inspection_time 파생변수 생성 및 상관관계 파악") 
df_product['inspection_time'] = (df_product['end_time'] - df_product['start_time']).dt.total_seconds() / 60  # 분 단위
st.dataframe(df_product.head())

# 상관관계 : inspection_time 과 defectcount 상관계수 파악
# 산점도 그래프
st.write("산점도")
fig = px.scatter(data_frame=df_product, x='inspection_time', y='defectcount', width=500, height=400, 
                trendline='ols', trendline_scope='overall')
st.plotly_chart(fig, use_container_width=True)

# 상관계수 확인 : defectcount 와 inspection_time 은 높은 양의 상관관계를 가진다.
# -> inspection_time 이 증가하면 defectcount 도 증가한다.
st.write("상관계수")
st.dataframe(df_product[['defectcount', 'inspection_time']].corr())
st.write("""inspection_time과 defectcount는 0.84로 높은 양의 상관관계를 가진다.
즉, inspection_time 이 증가하면 defectcount 도 증가하는 경향이 있다.""")



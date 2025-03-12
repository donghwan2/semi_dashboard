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
# Error_message 카운트플랏 - 어떤 에러메시지가 많이 발생하는지 확인한다.
# Target(불량갯수) 상자그림 - 이상치 확인
# Etching_rate(식각 속도)와 Target 산점도 - 상관관계 확인
# 공정 경로별 불량률(error_rate) 바플랏 - 어떤 공정 경로에서 불량률이 높은지 확인


# 제목
st.title('반도체 공정 error rate')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_preprocess = pd.read_csv('data/preprocessing_data.csv')
df_preprocess = df_preprocess.drop(columns=['Unnamed: 0'])

# 세션 스테이트에 데이터 저장
if "df_preprocess" not in st.session_state:
    st.session_state["df_preprocess"] = df_preprocess

st.write("#### 데이터 확인")
st.write("반도체 공정 전반적인 데이터")
st.write(df_preprocess.shape)
st.dataframe(df_preprocess.head())

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_preprocess.dtypes)

################# 데이터 전처리 #################
# 결측치 확인
st.write("#### 결측치 확인 및 처리")
st.dataframe(df_preprocess.isnull().sum())
st.write("""
        -> 결측치 없음.
""")

################# Error_message 분석 #################
st.write("#### Error_message 카운트 바플랏")

error_counts = df_preprocess['Error_message'].value_counts().reset_index()
error_counts.columns = ['Error_message', 'Count']

# Error_message 바플랏
fig = px.bar(error_counts, 
             x='Error_message', 
             y='Count', 
             title='Error Message Count',
             labels={'Error_message': 'Error Message', 'Count': 'Count'},
             text='Count')
st.plotly_chart(fig, use_container_width=True)


################# Target 분포 분석 #################
st.write("#### Target 분포 분석")
st.write("Target : 불량(error) 개수")

# # 히스토그램
# fig = px.histogram(df, x='Target')    
# st.plotly_chart(fig, use_container_width=True)

# 상자그림(이상치 파악)
fig = px.box(data_frame=df_preprocess, y='Target', width=650, height=400)
st.plotly_chart(fig, use_container_width=True)
st.write("""
         -> Upper fence 217을 넘어서는 이상치 데이터들이 존재.
         """)

################# Etching_rate와 target 상관관계 분석 #################
st.write("#### Etching_rate vs Target 상관관계")

# Scatter plot of Etching_rate vs Target
st.write("scatterplot with histogram")
fig = px.scatter(df_preprocess, 
                 x='Etching_rate', 
                 y='Target',
                 marginal_x="histogram",  # X축 주변 히스토그램
                 marginal_y="histogram",  # Y축 주변 히스토그램 
                #  title='Scatter Plot of Etching_rate vs Target',
                #  labels={'Etching_rate': 'Etching Rate', 'Target': 'Target'}
                 )
st.plotly_chart(fig, use_container_width=True)

# 상관계수 파악
st.write("상관계수")
st.dataframe(df_preprocess[['Etching_rate', 'Target']].corr())
st.write("""-> Etching_rate 과 Target 는 0.5 로 적당한 양의 상관관계를 가진다.  
즉, Etching_rate 이 증가하면 Target 도 증가하는 경향이 있다.""")

################# 공정 경로별 에러율 시각화 #################
# count 컬럼 추가 
df_preprocess['count'] = 1 

cnt_chamber_route = df_preprocess.pivot_table(index='Chamber_Route', 
                                    values='count',
                                    aggfunc='sum').reset_index().sort_values(by='count', ascending=False)
# index : 구분하고자 하는 항목 
# values : 계산하고자 하는 값 
# aggfunc : 계산하려는 통계 값 

# 공정경로 별 에러수(target), 프로세스 수(count) 합계
st.write("#### 공정경로(Chamber_Route) 별 불량률(error rate)")
Chamber_error_cnt = df_preprocess.pivot_table(index='Chamber_Route',
                                    values=['Target', 'count'],
                                    aggfunc='sum').reset_index()

Chamber_error_cnt['error_rate'] = Chamber_error_cnt['Target'] / Chamber_error_cnt['count'] 
# error_rate : 한 공정에서 발생한 불량칩의 평균값을 공정 경로별로 계산 
error_sorted = Chamber_error_cnt.sort_values(by='error_rate', ascending=False) 
st.dataframe(error_sorted)

# Chamber_Route 별 에러율(error_rate)
mpl.rc('font', family='Malgun Gothic')
fig = plt.figure(figsize=[7, 10])
plt.title("Chamber_Route 별 불량률(error_rate)")
sns.barplot(error_sorted, y='Chamber_Route', x='error_rate', palette='coolwarm');
st.pyplot(fig)  # seaborn 그래프를 streamlit에 출력




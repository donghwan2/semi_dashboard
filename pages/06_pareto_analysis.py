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
# 에러 메시지 px.bar
# 에러 메시지 파레토 차트 sns.barplot, sns.pointplot, sns.lineplot


# 제목
st.title('에러원인 파레토 차트')
st.markdown("<br>", unsafe_allow_html=True)   # 줄바꿈(공백)

# 데이터 로드
df_error = pd.read_csv('data/Error.csv')
# df = df.drop(columns=['Unnamed: 0'])

# 세션 스테이트에 데이터 저장
if "df_error" not in st.session_state:
    st.session_state["df_error"] = df_error

st.write("#### 데이터 확인")
st.write("에러 데이터")
st.write(df_error.shape)
st.dataframe(df_error.head())

################# 데이터 타입 확인 #################
st.write("#### 데이터 타입 확인")
st.write(df_error.dtypes)


################# 에러 메시지 분석 #################
st.write("#### 에러 메시지 분석")
msg_cnt = df_error['message'].value_counts().reset_index().sort_values(by='count', ascending=True)

st.dataframe(msg_cnt)

# # 에러 메시지 별 카운트 순위
# mpl.rc('font',family='Malgun Gothic')
# message_counts = msg_cnt['메세지'].value_counts().reset_index()

# Plotly 그래프 생성
fig = px.bar(msg_cnt, 
             x='count', 
             y='message', 
             orientation='h', 
             ) 

st.plotly_chart(fig, use_container_width=True)

################# 발생비율 구하기 #################
st.write("#### 발생비율 구하기")
msg_cnt['ratio'] = msg_cnt['count'] / msg_cnt['count'].sum()
msg_cnt = msg_cnt.sort_values(by='ratio', ascending=False)
msg_cnt['sum_ratio'] = msg_cnt['ratio'].cumsum()
st.dataframe(msg_cnt)

mpl.rc('font',family='Malgun Gothic')
fig = plt.figure(figsize=[15, 5])
order_list = msg_cnt.sort_values(by='count', ascending=False)['message']
sns.barplot(data=msg_cnt, x='message', y='count', palette='rocket', order=order_list)
plt.xticks(rotation=45)
st.pyplot(fig)  # seaborn 그래프를 streamlit에 출력

# 메시지 그룹 별 누적발생비율 포인트플롯
mpl.rc('font',family='Malgun Gothic')
fig = plt.figure(figsize=[15,5])
sns.pointplot(data=msg_cnt, x='message', y='sum_ratio', order=order_list)
plt.xticks(rotation=45)
st.pyplot(fig)  # seaborn 그래프를 streamlit에 출력

################# 파레토 차트 그리기 #################
st.write("#### 파레토 차트 그리기")

# 트윈축 - 발생빈도 바플롯, 누적발생비율 포인트플롯
msg_cnt['Line'] = 0.8

fig = plt.figure(figsize=[10,5])
x1 = sns.barplot(data=msg_cnt, x='message', y='count', palette='rocket') # y 축 범위 : 0~ 140
x2 = x1.twinx()
sns.pointplot(data=msg_cnt, x='message', y='sum_ratio')
sns.lineplot(data=msg_cnt, x='message', y='Line', color='r')

x1.set_xticklabels(x1.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)   # seaborn 그래프를 streamlit에 출력
st.write("-> Door Open부터 롯트 종료까지 누적 에러가 0.8이다. -> 주요 에러 원인이다.")



import pandas as pd
import streamlit as st
import plotly.express as px

kakao = pd.read_csv('../sample/feargreed_kakao_rev.csv')
naver = pd.read_csv('../sample/feargreed_naver_rev.csv')

fig_kakao = px.line(kakao, x="LSTM", y="BERT")
fig_naver = px.line(naver, x="LSTM", y='BERT')

st.title = ("Fear-Greed Index")
st.write("test")

st.plotly_chart(fig_kakao)
st.plotly_chart(fig_naver)

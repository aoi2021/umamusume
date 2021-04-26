import streamlit as st
import pandas as pd

st.title('レース一覧')

df = pd.read_csv('DB作成1.csv')
#st.table(df)
#st.write(df)

st.dataframe(df, width=1500, height=500)
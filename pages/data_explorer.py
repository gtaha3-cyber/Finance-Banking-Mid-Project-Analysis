import streamlit as st

df = st.session_state['data']

st.title('🔍 Data Explorer')
st.write(f'Transactions: {len(df):,}')

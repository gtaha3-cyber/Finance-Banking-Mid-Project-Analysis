import streamlit as st

df = st.session_state['data']

st.title('💰 Large Transactions')
st.write(f'Transactions: {len(df):,}')
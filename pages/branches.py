import streamlit as st

df = st.session_state['data']

st.title('🏢 Branch Performance')
st.write(f'Transactions: {len(df):,}')
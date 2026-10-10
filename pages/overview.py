import streamlit as st

df = st.session_state['data']

st.title('📊 Executive Overview')
st.write(f'Transactions: {len(df):,}')
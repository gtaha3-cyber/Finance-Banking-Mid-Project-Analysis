import streamlit as st

df = st.session_state['data']

st.title('📱 Digital & Channels')
st.write(f'Transactions: {len(df):,}')
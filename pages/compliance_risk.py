import streamlit as st

df = st.session_state['data']

st.title('🛡️ Compliance & Risk')
st.write(f'Transactions: {len(df):,}')
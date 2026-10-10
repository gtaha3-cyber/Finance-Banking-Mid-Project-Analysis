import streamlit as st

df = st.session_state['data']

st.title('👥 Customers & Products')
st.write(f'Transactions: {len(df):,}')
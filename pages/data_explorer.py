import streamlit as st

df = st.session_state['data']

st.title('🔍 Data Explorer')
st.caption('Search and filter the clean transactions, then download the result.')

# ---------------- Search ----------------
col1, col2 = st.columns(2)
search = col1.text_input('Search by Customer ID or Transaction ID', placeholder='e.g. CUST-616210')
min_amount = col2.number_input('Minimum amount', min_value=0, value=0, step=10000)

col3, col4, col5 = st.columns(3)
dates = col3.date_input('Transaction date range',
                        value=(df['transaction_date'].min().date(), df['transaction_date'].max().date()))
channel = col4.selectbox('Channel', ['All'] + sorted(df['transaction_channel'].unique()))
sort_by = col5.selectbox('Sort by', ['transaction_date', 'amount', 'risk_score'])

order = st.radio('Order', ['Newest / Highest first', 'Oldest / Lowest first'], horizontal=True)

# ---------------- Apply the search ----------------
result = df[df['amount'] >= min_amount]

if search:
    result = result[result['customer_id'].str.contains(search, case=False) |
                    result['transaction_id'].str.contains(search, case=False)]

if len(dates) == 2:
    start, end = dates
    result = result[result['transaction_date'].dt.date.between(start, end)]

if channel != 'All':
    result = result[result['transaction_channel'] == channel]

result = result.sort_values(sort_by, ascending=(order == 'Oldest / Lowest first'))

# ---------------- Result ----------------
st.divider()
st.columns(4)[0].metric('Matching Transactions', f'{len(result):,}', border=True)

columns = ['transaction_id', 'transaction_date', 'customer_id', 'customer_segment', 'account_type',
           'account_status', 'transaction_type', 'transaction_channel', 'branch_city', 'amount', 'currency',
           'risk_score', 'fraud_flag', 'aml_check_status', 'kyc_status']
st.dataframe(result[columns].head(1000), hide_index=True, width='stretch',
             column_config={'transaction_date': st.column_config.DateColumn('transaction_date', format='YYYY-MM-DD')})
st.caption('The table shows up to 1,000 rows. Use the download button to get all matching rows.')

st.download_button('⬇️ Download the result as CSV', result[columns].to_csv(index=False),
                   file_name='filtered_transactions.csv', mime='text/csv')

st.divider()

# ---------------- Notes ----------------
st.subheader('📝 Your Notes')
notes = st.text_area('Write any notes or observations about the data', height=120)
if notes:
    st.success('Note saved for this session.')

import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('💰 Large Transactions')
st.caption('👤 Stakeholder: Relationship Managers & Executive Management')

large = df[df['is_outlier']]

if large.empty:
    st.warning('No large transactions for the selected filters.')
    st.stop()

# ---------------- KPIs ----------------
non_active = large['account_status'].isin(['Frozen', 'Dormant', 'Closed']).mean() * 100
aml_open = large['aml_check_status'].isin(['Skipped', 'Pending']).mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric('Large Transactions', f'{len(large):,}', border=True)
col2.metric('Share of All Transactions', f'{len(large) / len(df) * 100:.2f}%', border=True)
col3.metric('On Non-Active Accounts', f'{non_active:.0f}%', border=True)
col4.metric('AML Skipped or Pending', f'{aml_open:.0f}%', border=True)

st.caption('Large transactions are the outliers in `amount` (IQR method), from about 78K to 4.7 million.')

st.divider()

# ---------------- Where do large transactions come from? ----------------
st.subheader('Where do large transactions come from?')

options = {'Account Type': 'account_type', 'Customer Segment': 'customer_segment', 'Channel': 'transaction_channel'}
choice = st.radio('Compare by', list(options), horizontal=True)
col = options[choice]

plot_df = (df.groupby(col)['is_outlier'].mean() * 100).round(2).sort_values(ascending=False).reset_index()
fig = px.bar(data_frame=plot_df, x=col, y='is_outlier', text_auto=True,
             title=f'Large Transactions Rate by {choice} (%)',
             labels={col: choice, 'is_outlier': 'Large Transactions (%)'},
             color_discrete_sequence=['#7b1e3a'])
st.plotly_chart(fig, width='stretch')

st.divider()

# ---------------- Are they well controlled? ----------------
st.subheader('Are they well controlled?')

plot_df = large.groupby(['account_status', 'aml_check_status'])['transaction_id'].count().reset_index()
fig = px.bar(data_frame=plot_df, x='account_status', y='transaction_id', color='aml_check_status', text_auto=True,
             title='Large Transactions by Current Account Status and AML Check',
             labels={'transaction_id': 'Num of Large Transactions', 'account_status': 'Current Account Status',
                     'aml_check_status': 'AML Check'},
             color_discrete_sequence=['#7b1e3a', '#f6a96b', '#9aa0a6', '#c45c7a', '#f3d1b0'])
fig.update_traces(textangle=0).update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
st.plotly_chart(fig, width='stretch')

# ---------------- Insight ----------------
st.info('**Key insight:** large transactions are rare (0.42%) and most common in Loan and Mortgage accounts '
        'and the Mobile App. About half are linked to accounts that are now Frozen, Dormant or Closed, '
        'and about a third had their AML check Skipped or Pending.')
st.success("""**Recommendations:**
- Review the large transactions on accounts that are now Frozen, Dormant or Closed.
- Make a completed AML check mandatory for every large transaction.
- Assign relationship managers to the customers behind large transactions.""")
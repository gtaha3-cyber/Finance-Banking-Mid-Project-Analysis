import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('📊 Executive Overview')
st.caption('👤 Stakeholder: Executive Management')

# ---------------- KPIs for the selected year ----------------
years = sorted(df['year'].unique(), reverse=True)
year = st.columns(4)[0].selectbox('Select year', years)

this_year = df[df['year'] == year]
last_year = df[df['year'] == year - 1]


def change(now, before):
    """% change compared to the previous year (None if there is no previous year)."""
    return f'{(now / before - 1) * 100:.1f}%' if before else None


transactions_now, transactions_before = len(this_year), len(last_year)
customers_now, customers_before = this_year['customer_id'].nunique(), last_year['customer_id'].nunique()
digital_now = (this_year['channel_group'] == 'Digital').mean() * 100
digital_before = (last_year['channel_group'] == 'Digital').mean() * 100 if len(last_year) else None

col1, col2, col3 = st.columns(3)
col1.metric('Transactions', f'{transactions_now:,}', change(transactions_now, transactions_before), border=True)
col2.metric('Active Customers', f'{customers_now:,}', change(customers_now, customers_before), border=True)
col3.metric('Digital Share', f'{digital_now:.1f}%',
            f'{digital_now - digital_before:.1f} pts' if digital_before else None, border=True)

st.caption('Changes are compared to the previous year. '
           '**Active customers** = unique customers who made at least one transaction in the year.')

st.divider()

# ---------------- Trends ----------------
tab1, tab2 = st.tabs(['📈 Yearly Trend', '📅 Monthly Trend'])

with tab1:
    plot_df = df.groupby('year').agg(Transactions=('transaction_id', 'count'),
                                     **{'Active Customers': ('customer_id', 'nunique')}).reset_index()
    fig = px.bar(data_frame=plot_df, x='year', y=['Transactions', 'Active Customers'], barmode='group',
                 text_auto=',d', title='Transactions and Active Customers per Year',
                 labels={'value': 'Count', 'variable': '', 'year': 'Year'},
                 color_discrete_sequence=['#7b1e3a', '#f6a96b'])
    st.plotly_chart(fig.update_xaxes(dtick=1), width='stretch')

with tab2:
    plot_df = df.groupby(df['transaction_date'].dt.to_period('M').dt.to_timestamp())['transaction_id'].count().reset_index()
    fig = px.area(data_frame=plot_df, x='transaction_date', y='transaction_id',
                  title='Monthly Number of Transactions',
                  labels={'transaction_date': 'Month', 'transaction_id': 'Num of Transactions'},
                  color_discrete_sequence=['#7b1e3a'])
    st.plotly_chart(fig, width='stretch')

# ---------------- Insight ----------------
st.info('**Key insight:** transactions and active customers are stable at about 13,000 per year, '
        'with a small decline of about 1% in 2024 and 2025, coming from fewer customers, not less usage.')
st.success("""**Recommendations:**
- **Retain:** run retention campaigns and monitor active customers monthly as an early warning sign.
- **Acquire:** attract new customers through marketing campaigns and referral rewards.
- **Engage:** encourage customers to make more transactions (e.g., cashback, loyalty points or lower fees),
  since each active customer makes only about one transaction per year.""")
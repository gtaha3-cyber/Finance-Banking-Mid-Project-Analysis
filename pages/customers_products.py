import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('👥 Customers & Products')
st.caption('👤 Stakeholder: Marketing Team')

# ---------------- KPIs ----------------
product_share = (df['account_type'].value_counts(normalize=True) * 100).round(1)

col1, col2, col3, col4 = st.columns(4)
col1.metric('Customers', f"{df['customer_id'].nunique():,}", border=True)
col2.metric('Customer Segments', df['customer_segment'].nunique(), border=True)
col3.metric('Products', df['account_type'].nunique(), border=True)
col4.metric('Most Used Product', product_share.index[0], f'{product_share.iloc[0]}% of transactions',
            delta_color='off', border=True)

st.divider()

# ---------------- Charts ----------------
tab1, tab2, tab3 = st.tabs(['🔥 Product Mix', '🔎 Segment Details', '👥 Customers per Segment'])

with tab1:
    plot_df = pd.crosstab(df['customer_segment'], df['account_type'], normalize='index').mul(100).round(1)
    fig = px.imshow(plot_df, text_auto=True, color_continuous_scale=['#f7f7f8', '#7b1e3a'], zmin=0,
                    title='Product Mix per Customer Segment (% of each segment)',
                    labels={'x': 'Account Type', 'y': 'Customer Segment', 'color': '%'})
    st.plotly_chart(fig, width='stretch')
    st.caption('Each row adds up to 100%.')

with tab2:
    segment = st.columns(3)[0].selectbox('Choose a customer segment', sorted(df['customer_segment'].unique()))
    plot_df = (df[df['customer_segment'] == segment]['account_type'].value_counts(normalize=True) * 100).round(1).reset_index()
    fig = px.bar(data_frame=plot_df, x='account_type', y='proportion', text_auto=True,
                 title=f'Products Used by {segment} Customers (%)',
                 labels={'account_type': 'Account Type', 'proportion': 'Share of Transactions (%)'},
                 color_discrete_sequence=['#7b1e3a'])
    st.plotly_chart(fig, width='stretch')

with tab3:
    plot_df = df.groupby('customer_segment')['customer_id'].nunique().sort_values(ascending=False).reset_index()
    fig = px.bar(data_frame=plot_df, x='customer_segment', y='customer_id', text_auto=',d',
                 title='Number of Customers per Segment',
                 labels={'customer_segment': 'Customer Segment', 'customer_id': 'Customers'},
                 color_discrete_sequence=['#f6a96b'])
    st.plotly_chart(fig, width='stretch')

# ---------------- Insight ----------------
st.info('**Key insight:** every customer segment uses all 6 products in almost equal shares (about 16–17% each), '
        'so products are not tailored to the needs of each segment.')
st.success("""**Recommendations:**
- Design segment-specific product packages (e.g., investment products for Private Banking and Premium customers,
  and business loans for Corporate customers).
- Use targeted marketing campaigns for each segment instead of one general campaign.""")
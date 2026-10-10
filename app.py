import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Finance & Banking Dashboard', page_icon='🏦', layout='wide')


@st.cache_data
def load_data():
    """Load the clean dataset once and add the helper columns used in the analysis."""
    df = pd.read_parquet('finance_banking_transactions_clean.parquet')
    df['year'] = df['transaction_date'].dt.year
    df['channel_group'] = np.where(df['transaction_channel'].isin(['Online', 'Mobile App']),
                                   'Digital', 'Non-Digital')
    return df


df = load_data()

# ---------------- Pages ----------------
pages = {
    '': [
        st.Page('pages/home.py', title='Home', icon='🏦', default=True),
    ],
    'Dashboards': [
        st.Page('pages/overview.py', title='Executive Overview', icon='📊'),
        st.Page('pages/large_transactions.py', title='Large Transactions', icon='💰'),
        st.Page('pages/digital_channels.py', title='Digital & Channels', icon='📱'),
        st.Page('pages/customers_products.py', title='Customers & Products', icon='👥'),
        st.Page('pages/branches.py', title='Branch Performance', icon='🏢'),
        st.Page('pages/compliance_risk.py', title='Compliance & Risk', icon='🛡️'),
    ],
    'Tools': [
        st.Page('pages/data_explorer.py', title='Data Explorer', icon='🔍'),
    ],
}

page = st.navigation(pages)

# ---------------- Sidebar filters (shown on all pages except Home) ----------------
filtered = df

if page.title != 'Home':
    st.sidebar.header('🔎 Filters')

    currencies = st.sidebar.multiselect('Currency', sorted(df['currency'].unique()),
                                        default=sorted(df['currency'].unique()))
    segments = st.sidebar.multiselect('Customer Segment', sorted(df['customer_segment'].unique()),
                                      default=sorted(df['customer_segment'].unique()))

    filtered = df[df['currency'].isin(currencies) & df['customer_segment'].isin(segments)]

    st.sidebar.caption(f'Showing **{len(filtered):,}** of {len(df):,} transactions')

# Save the filtered data so every page can use it
st.session_state['data'] = filtered

page.run()
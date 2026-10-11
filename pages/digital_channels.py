import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('📱 Digital & Channels')
st.caption('👤 Stakeholder: Digital & Product Team')

# ---------------- Change from 2022 to 2025 for each channel ----------------
channel_years = pd.crosstab(df['transaction_channel'], df['year'])
channel_years['change_%'] = ((channel_years[2025] / channel_years[2022] - 1) * 100).round(1)
channel_years = channel_years.sort_values('change_%')

# ---------------- KPIs ----------------
digital_share = (df['channel_group'] == 'Digital').mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric('Digital Share', f'{digital_share:.1f}%', border=True)
col2.metric('Digital Transactions', f"{(df['channel_group'] == 'Digital').sum():,}", border=True)
col3.metric('Fastest Growing Channel', channel_years.index[-1], f"{channel_years['change_%'].iloc[-1]}%", border=True)
col4.metric('Biggest Decline', channel_years.index[0], f"{channel_years['change_%'].iloc[0]}%", border=True)

st.caption('Digital channels = Online and Mobile App. Changes compare 2025 with 2022.')

st.divider()

# ---------------- Charts ----------------
tab1, tab2, tab3 = st.tabs(['🥧 Digital vs Non-Digital', '📊 Growth by Channel', '📈 Yearly Trend'])

with tab1:
    plot_df = df['channel_group'].value_counts().reset_index()
    fig = px.pie(data_frame=plot_df, names='channel_group', values='count', hole=0.45,
                 title='Digital vs Non-Digital Transactions',
                 color_discrete_sequence=['#7b1e3a', '#f6a96b'])
    st.plotly_chart(fig, width='stretch')

with tab2:
    plot_df = channel_years.reset_index()
    plot_df['trend'] = np.where(plot_df['change_%'] >= 0, 'Growing', 'Declining')
    fig = px.bar(data_frame=plot_df, x='change_%', y='transaction_channel', orientation='h', color='trend',
                 text_auto=True, color_discrete_map={'Growing': '#81c784', 'Declining': '#e57373'},
                 title='Change in Transactions from 2022 to 2025 by Channel (%)',
                 labels={'change_%': 'Change from 2022 to 2025 (%)', 'transaction_channel': 'Channel', 'trend': ''})
    st.plotly_chart(fig, width='stretch')

with tab3:
    channels = st.multiselect('Choose channels', sorted(df['transaction_channel'].unique()),
                              default=['Online', 'Mobile App', 'Branch'])
    plot_df = df[df['transaction_channel'].isin(channels)].groupby(['year', 'transaction_channel'])['transaction_id'].count().reset_index()
    fig = px.line(data_frame=plot_df, x='year', y='transaction_id', color='transaction_channel', markers=True,
                  title='Transactions per Year by Channel',
                  labels={'transaction_id': 'Num of Transactions', 'transaction_channel': 'Channel', 'year': 'Year'},
                  color_discrete_sequence=['#7b1e3a', '#f6a96b', '#9aa0a6', '#c45c7a', '#4a0f22', '#f3d1b0', '#5f6368'])
    st.plotly_chart(fig.update_xaxes(dtick=1), width='stretch')

# ---------------- Insight ----------------
st.info('**Key insight:** digital channels handle only about 29% of transactions and are not growing '
        '(Online -4.2%, Mobile App -3.6% from 2022 to 2025), while Branch is the only growing channel (+11.6%).')
st.success("""**Recommendations:**
- Launch a digital adoption campaign (e.g., rewards or lower fees for Mobile App and Online transactions).
- Study why customers are returning to branches, and move simple branch services to the app.""")
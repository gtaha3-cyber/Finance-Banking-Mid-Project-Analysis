import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('🏢 Branch Performance')
st.caption('👤 Stakeholder: Branch Operations')

# ---------------- Transactions per branch per year ----------------
branch_years = pd.crosstab(df['branch_city'], df['year'])
branch_years['change_%'] = ((branch_years[2025] / branch_years[2022] - 1) * 100).round(1)
branch_years['trend'] = np.where(branch_years['change_%'] >= 0, 'Growing', 'Declining')
branch_years = branch_years.sort_values('change_%')

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric('Branches', len(branch_years), border=True)
col2.metric('Growing Branches', (branch_years['trend'] == 'Growing').sum(), border=True)
col3.metric('Declining Branches', (branch_years['trend'] == 'Declining').sum(), border=True)
col4.metric('Top Growing Branch', branch_years.index[-1], f"{branch_years['change_%'].iloc[-1]}%", border=True)

st.caption('Growth compares the number of transactions in 2025 with 2022.')

st.divider()

# ---------------- Charts ----------------
tab1, tab2, tab3 = st.tabs(['🗺️ Branch Map', '📊 Total Change', '📅 Year by Year'])

with tab1:
    # Location of each branch city in Germany
    coordinates = pd.DataFrame({
        'branch_city': ['Berlin', 'Bremen', 'Cologne', 'Dortmund', 'Dresden', 'Duisburg', 'Dusseldorf', 'Essen',
                        'Frankfurt', 'Hamburg', 'Hanover', 'Leipzig', 'Munich', 'Nuremberg', 'Stuttgart'],
        'lat': [52.52, 53.08, 50.94, 51.51, 51.05, 51.43, 51.23, 51.46, 50.11, 53.55, 52.38, 51.34, 48.14, 49.45, 48.78],
        'lon': [13.40, 8.80, 6.96, 7.47, 13.74, 6.76, 6.77, 7.01, 8.68, 9.99, 9.73, 12.37, 11.58, 11.08, 9.18],
    })
    plot_df = branch_years.reset_index().merge(coordinates, on='branch_city')
    plot_df['transactions'] = branch_years[[2022, 2023, 2024, 2025]].sum(axis=1).values
    fig = px.scatter_geo(data_frame=plot_df, lat='lat', lon='lon', color='trend', size='transactions',
                         hover_name='branch_city', hover_data={'change_%': True, 'transactions': ':,',
                                                               'lat': False, 'lon': False, 'trend': False},
                         color_discrete_map={'Growing': '#81c784', 'Declining': '#e57373'},
                         title='Branch Cities in Germany (green = growing, red = declining)', height=600)
    fig.update_geos(fitbounds='locations', showcountries=True, countrycolor='#9aa0a6',
                    showland=True, landcolor='#ffffff', showocean=True, oceancolor='#e6e7eb')
    st.plotly_chart(fig, width='stretch')

with tab2:
    plot_df = branch_years.reset_index()
    fig = px.bar(data_frame=plot_df, x='change_%', y='branch_city', orientation='h', color='trend', text_auto=True,
                 color_discrete_map={'Growing': '#81c784', 'Declining': '#e57373'},
                 title='Total Change in Transactions from 2022 to 2025 by Branch City (%)',
                 labels={'change_%': 'Change from 2022 to 2025 (%)', 'branch_city': 'Branch City', 'trend': ''},
                 height=550)
    st.plotly_chart(fig, width='stretch')

with tab3:
    plot_df = df.groupby(['branch_city', 'year'])['transaction_id'].count().reset_index(name='transactions')
    plot_df['change_%'] = (plot_df.groupby('branch_city')['transactions'].pct_change() * 100).round(1)
    plot_df = plot_df.dropna()
    plot_df['trend'] = np.where(plot_df['change_%'] >= 0, 'Growth', 'Decline')
    fig = px.scatter(data_frame=plot_df, x='year', y='branch_city', color='trend', symbol='trend', text='change_%',
                     color_discrete_map={'Growth': '#81c784', 'Decline': '#e57373'},
                     symbol_map={'Growth': 'triangle-up', 'Decline': 'triangle-down'}, height=600,
                     title='Yearly Growth or Decline in Transactions by Branch City (%)',
                     labels={'year': 'Year (compared to previous year)', 'branch_city': 'Branch City', 'trend': ''})
    fig.update_traces(marker_size=16, textposition='middle right').update_xaxes(dtick=1)
    st.plotly_chart(fig, width='stretch')

st.divider()

# ---------------- Branch details (drop-down list) ----------------
st.subheader('🔎 Branch Details')

branch = st.columns(3)[0].selectbox('Choose a branch', sorted(branch_years.index))
yearly = branch_years.loc[branch, [2022, 2023, 2024, 2025]]

col1, col2, col3 = st.columns(3)
col1.metric('Transactions in 2025', f'{yearly[2025]:,}', border=True)
col2.metric('Change vs 2024', f'{(yearly[2025] / yearly[2024] - 1) * 100:.1f}%',
            f'{yearly[2025] - yearly[2024]:,} transactions', border=True)
col3.metric('Change vs 2022', f'{(yearly[2025] / yearly[2022] - 1) * 100:.1f}%',
            f'{yearly[2025] - yearly[2022]:,} transactions', border=True)

plot_df = yearly.reset_index()
plot_df.columns = ['year', 'transactions']
fig = px.line(data_frame=plot_df, x='year', y='transactions', markers=True, text='transactions',
              title=f'Transactions per Year in {branch}',
              labels={'year': 'Year', 'transactions': 'Num of Transactions'},
              color_discrete_sequence=['#7b1e3a'])
fig.update_traces(textposition='top center').update_xaxes(dtick=1)
st.plotly_chart(fig, width='stretch')

if st.toggle('Show the table for all branches'):
    st.dataframe(branch_years, width='stretch')

# ---------------- Insight ----------------
st.info('**Key insight:** 10 of 15 branches declined from 2022 to 2025. Dortmund, Duisburg and Leipzig dropped sharply '
        'in 2025 only, while Hamburg and Berlin recovered after bad years and Munich grew every year.')
st.success("""**Recommendations:**
- Investigate what changed in 2025 in Dortmund, Duisburg and Leipzig.
- Run a market scan and a Net Promoter Score (NPS) survey for the declining branches.
- Introduce staff incentives linked to branch targets, and apply the practices of Munich, Hamburg and Berlin.""")
import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state['data']

st.title('🛡️ Compliance & Risk')
st.caption('👤 Stakeholder: Compliance Team')

# ---------------- Red flags ----------------
red_flags = pd.DataFrame({
    'Account currently Closed or Frozen': df['account_status'].isin(['Closed', 'Frozen']),
    'KYC Expired or Pending': df['kyc_status'].isin(['Expired', 'Pending']),
    'AML Failed or Skipped': df['aml_check_status'].isin(['Failed', 'Skipped']),
})
red_flags['At least one red flag'] = red_flags.any(axis=1)

passed_bad_kyc = (df['kyc_status'].isin(['Expired', 'Pending']) & (df['aml_check_status'] == 'Passed')).sum()

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric('With at Least One Red Flag', f"{red_flags['At least one red flag'].mean() * 100:.1f}%", border=True)
col2.metric('KYC Expired or Pending', f"{red_flags['KYC Expired or Pending'].mean() * 100:.1f}%", border=True)
col3.metric('AML Failed or Skipped', f"{red_flags['AML Failed or Skipped'].mean() * 100:.1f}%", border=True)
col4.metric('Passed AML with Bad KYC', f'{passed_bad_kyc:,}', border=True)

st.divider()

# ---------------- Charts ----------------
tab1, tab2, tab3 = st.tabs(['🚩 Red Flags', '🔗 KYC vs AML', '🎯 Risk Score Test'])

with tab1:
    plot_df = (red_flags.mean() * 100).round(1).rename_axis('red_flag').reset_index(name='share_%')
    fig = px.bar(data_frame=plot_df, x='red_flag', y='share_%', text_auto=True,
                 title='Transactions with Compliance Red Flags (%)',
                 labels={'red_flag': 'Red Flag', 'share_%': 'Share of Transactions (%)'},
                 color_discrete_sequence=['#7b1e3a'])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    view = st.segmented_control('Show', ['Number of transactions', '% of each KYC status'],
                                default='Number of transactions')
    if view == '% of each KYC status':
        plot_df = pd.crosstab(df['kyc_status'], df['aml_check_status'], normalize='index').mul(100).round(1)
    else:
        plot_df = pd.crosstab(df['kyc_status'], df['aml_check_status'])
    fig = px.imshow(plot_df, text_auto=True, color_continuous_scale=['#f7f7f8', '#7b1e3a'],
                    title='KYC Status vs AML Check Status',
                    labels={'x': 'AML Check', 'y': 'KYC Status', 'color': 'Value'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption('With %, the AML "Passed" rate is about the same for every KYC status, '
               'so the AML check does not take the KYC status into account.')

with tab3:
    st.write('Move the slider to choose when a transaction is treated as **high risk**, '
             'and check whether high-risk transactions really have more fraud.')
    threshold = st.slider('High risk if risk score is at least', 0, 100, 70)

    high_risk = df['risk_score'] >= threshold
    col1, col2, col3 = st.columns(3)
    col1.metric('High-Risk Transactions', f'{high_risk.sum():,}', border=True)
    col2.metric('Fraud Rate (High Risk)', f"{df[high_risk]['fraud_flag'].mean() * 100:.1f}%", border=True)
    col3.metric('Fraud Rate (Others)', f"{df[~high_risk]['fraud_flag'].mean() * 100:.1f}%", border=True)

    df_bands = df.assign(risk_band=pd.cut(df['risk_score'], bins=[0, 20, 40, 60, 80, 100], include_lowest=True,
                                          labels=['0-20', '20-40', '40-60', '60-80', '80-100']))
    plot_df = (df_bands.groupby('risk_band', observed=True)['fraud_flag'].mean() * 100).round(2).reset_index()
    fig = px.bar(data_frame=plot_df, x='risk_band', y='fraud_flag', text_auto=True,
                 title='Fraud Rate by Risk Score Band',
                 labels={'risk_band': 'Risk Score Band', 'fraud_flag': 'Fraud Rate (%)'},
                 color_discrete_sequence=['#f6a96b'])
    st.plotly_chart(fig.update_yaxes(range=[0, 100]), use_container_width=True)

# ---------------- Insight ----------------
st.info('**Key insight:** about 73% of transactions have at least one compliance red flag, 6,982 transactions passed AML '
        'although KYC was Expired or Pending, and the fraud rate is about 50% at every risk score, '
        'so the risk score does not identify fraud.')
st.success("""**Recommendations:**
- Block transactions for customers with expired KYC until their documents are renewed.
- Do not allow an AML "Passed" status unless KYC is Verified or Not Required.
- Review and retrain the risk scoring model.""")
import streamlit as st

# ---------------- Banner (HTML + CSS) ----------------
st.markdown("""
<div style="
    background: linear-gradient(135deg, #4a0f22 0%, #7b1e3a 55%, #9c3b57 100%);
    border-radius: 18px;
    padding: 55px 30px;
    text-align: center;
    border-bottom: 6px solid #f6a96b;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);">
    <div style="font-size: 60px;">🏦</div>
    <h1 style="color: #ffffff; font-size: 44px; margin: 10px 0 5px 0;">
        Finance &amp; Banking Dashboard
    </h1>
    <p style="color: #e6e7eb; font-size: 19px; margin: 0;">
        Transactions Analysis &nbsp;|&nbsp; 2022 – 2025 &nbsp;|&nbsp; 15 Branches in Germany
    </p>
    <p style="color: #f6a96b; font-size: 16px; margin-top: 18px; letter-spacing: 1px;">
        GROWTH &nbsp;•&nbsp; DIGITAL &nbsp;•&nbsp; CUSTOMERS &nbsp;•&nbsp; BRANCHES &nbsp;•&nbsp; COMPLIANCE
    </p>
</div>
""", unsafe_allow_html=True)

st.write('')
st.write('')

# ---------------- Dashboards (one card for each stakeholder) ----------------
dashboards = [
    ('pages/overview.py', '📊', 'Executive Overview', 'Executive Management'),
    ('pages/large_transactions.py', '💰', 'Large Transactions', 'Relationship Managers'),
    ('pages/digital_channels.py', '📱', 'Digital & Channels', 'Digital & Product Team'),
    ('pages/customers_products.py', '👥', 'Customers & Products', 'Marketing Team'),
    ('pages/branches.py', '🏢', 'Branch Performance', 'Branch Operations'),
    ('pages/compliance_risk.py', '🛡️', 'Compliance & Risk', 'Compliance Team'),
]

# Show the cards in 2 rows of 3
for row in range(2):
    cols = st.columns(3)
    for col, (page, icon, title, stakeholder) in zip(cols, dashboards[row * 3:(row + 1) * 3]):
        with col.container(border=True):
            st.markdown(f'#### {icon} {title}')
            st.caption(f'👤 {stakeholder}')
            st.page_link(page, label='Open dashboard', icon='➡️')

st.write('')

# ---------------- Data notes ----------------
with st.expander('📌 Notes about the Data'):
    st.markdown("""
- **Counts instead of values:** the median amount is about 25,000 in all 5 currencies, so amounts were
  generated without considering the currency. The dashboards therefore compare **number of transactions**, not values.
- **One account per transaction:** the 52,000 transactions come from 52,000 different accounts, while in real banking
  one account makes many transactions.
- **Fraud and risk score:** about 50% of transactions are flagged as fraud (usually below 1% in real banking),
  and the risk score does not separate fraud from normal transactions.
- **Compliance checks:** the AML result is almost the same whatever the KYC status, so the two checks are not linked.
- **Account status:** shows the **current** status of the account, not its status at the time of the transaction.

These patterns show that the dataset is **synthetic**, so the findings demonstrate the analysis approach
rather than the behavior of a real bank.
""")
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="TLS Akinator Pro", layout="wide")
st.title("🛡️ Web Defense Command Center")
st.caption("Intelligence Decision Support System - Universidad Nacional de Colombia")

try:
    with open("final_report.json", "r") as f:
        data = json.load(f)
        df = pd.DataFrame(data)

    # Top KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Targets", len(df))
    m2.metric("Critical Findings", len(df[df['severity'] == 'CRITICAL']))
    m3.metric("High Risk Hosts", len(df[df['severity'] == 'HIGH']))
    m4.metric("TLS 1.3 Compliance", f"{(len(df[df['tls_versions'].apply(lambda x: 'TLSv1.3' in x)])/len(df)*100):.0f}%")

    st.divider()
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Relative Exposure by Target")
        cmap = {'CRITICAL':'black', 'HIGH':'red', 'MEDIUM':'orange', 'LOW':'green'}
        fig = px.bar(df, x='server', y='severity', color='severity', color_discrete_map=cmap, category_orders={"severity": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]})
        st.plotly_chart(fig, use_container_width=True)
    
    with col_r:
        st.subheader("Encryption Standards Distribution")
        fig2 = px.pie(df, names='key_info', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Actionable Intelligence Matrix")
    df_clean = df.copy()
    df_clean['findings'] = df_clean['findings'].apply(lambda x: " | ".join(x))
    df_clean['recommendations'] = df_clean['recommendations'].apply(lambda x: " | ".join(x))
    st.table(df_clean[['server', 'severity', 'key_info', 'cert_expiry', 'findings']])

except:
    st.info("Telemetry offline. Run a terminal scan to populate dashboard.")

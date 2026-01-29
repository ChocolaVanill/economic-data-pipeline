# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from config.database import get_engine

st.set_page_config(page_title="Labour Market", page_icon="👷", layout="wide")
st.title("Labour Market Statistics")
st.markdown("Employment, unemployment, and labour force data")

@st.cache_data(ttl=3600)
def load_labour_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM analytics_gold.labour_summary ORDER BY date DESC", engine)
    return df

try:
    labour_df = load_labour_data()

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    latest = labour_df.iloc[0] if len(labour_df) > 0 else None

    with col1:
        employed = latest.get('lf_employed', 0) if latest is not None else 0
        st.metric("Employed", f"{employed:,.0f}")

    with col2:
        unemployed = latest.get('lf_unemployed', 0) if latest is not None else 0
        st.metric("Unemployed", f"{unemployed:,.0f}")

    with col3:
        labour_force = latest.get('lf', 0) if latest is not None else 0
        st.metric("Labour Force", f"{labour_force:,.0f}")

    with col4:
        unemp_rate = latest.get('u_rate', 0) if latest is not None else 0
        st.metric("Unemployment Rate", f"{unemp_rate:.1f}%")

    # Prepare data for plotting
    plot_df = labour_df.sort_values('date').rename(columns={
        'lf_employed': 'Employed', 
        'lf_unemployed': 'Unemployed'
    })

    # Employment Trend
    st.subheader("Employment Trend")
    fig = px.line(
        plot_df,
        x='date',
        y=['Employed', 'Unemployed'],
        title='Employment vs Unemployment',
        labels={'date': 'Date', 'value': 'Count'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Unemployment Rate
    st.subheader("Unemployment Rate Trend")
    fig2 = px.area(
        labour_df.sort_values('date'),
        x='date',
        y='u_rate',
        title='Unemployment Rate (%)',
        labels={'date': 'Date', 'u_rate': 'Rate (%)'}
    )
    fig2.update_traces(fill='tozeroy', line_color='coral')
    st.plotly_chart(fig2, use_container_width=True)

    # Data Table
    with st.expander("View Raw Data"):
        st.dataframe(labour_df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the gold.labour_summary table is populated.")
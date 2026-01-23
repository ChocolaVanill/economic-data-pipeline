# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from config.database import get_engine

# Page config
st.set_page_config(
    page_title="Malaysia Economic Dashboard",
    page_icon="🇲🇾",
    layout="wide"
)

st.title("🇲🇾 Malaysia Economic Indicators Dashboard")
st.markdown("Real-time economic data from data.gov.my")

# Load data
@st.cache_data(ttl=3600)
def load_gdp_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM gold.gdp_trends ORDER BY trend_date", engine)
    return df

try:
    gdp_df = load_gdp_data()

    # KPI cards
    col1, col2, col3 = st.columns(3)

    latest = gdp_df.iloc[-1]

    with col1:
        st.metric(
            label="Latest GDP (RM Million)",
            value=f"{latest['gdp_value']:,.0f}",
            delta=f"{latest['yoy_change_pct']:.1f}% YoY" if pd.notna(latest['yoy_change_pct']) else None
        )

    with col2:
        st.metric(
            label="3-Quarter Moving Average",
            value=f"{latest['ma_3_quarter']:,.0f}" if pd.notna(latest['ma_3_quarter']) else "N/A"
        )

    with col3:
        st.metric(
            label="Trend Direction",
            value=latest['trend_direction'].title() if latest['trend_direction'] else "N/A"
        )

    # GDP Trend Chart
    st.subheader("GDP Trend Over Time")

    fig = px.line(
        gdp_df,
        x='trend_date',
        y='gdp_value',
        title='Malaysia GDP (Quarterly)',
        labels={'trend_date': 'Date', 'gdp_value': 'GDP (RM Million)'}
    )
    fig.add_scatter(
        x=gdp_df['trend_date'],
        y=gdp_df['ma_3_quarter'],
        name='3-Quarter MA',
        line=dict(dash='dash')
    )
    st.plotly_chart(fig, use_container_width=True)

    # YoY Growth Chart
    st.subheader("Year-over-Year Growth Rate")

    growth_df = gdp_df.dropna(subset=['yoy_change_pct'])
    fig2 = px.bar(
        growth_df,
        x='trend_date',
        y='yoy_change_pct',
        title='GDP Growth Rate (YoY %)',
        color='yoy_change_pct',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Raw Data Table
    with st.expander("View Raw Data"):
        st.dataframe(gdp_df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the gold layer tables are populated.")
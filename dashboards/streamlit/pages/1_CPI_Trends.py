# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from config.database import get_engine

st.set_page_config(page_title="CPI Trends", page_icon="📊", layout="wide")
st.title(" Consumer Price Index (CPI) Trends")
st.markdown("Monthly CPI data across different categories")

@st.cache_data(ttl=3600)
def load_cpi_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * from gold.cpi_trends ORDER BY date DESC", engine)
    # Map category codes to names
    category_map = {
        '01': 'Food & Non-Alcoholic Beverages',
        '02': 'Alcoholic Beverages & Tobacco',
        '03': 'Clothing & Footwear',
        '04': 'Housing, Water, Electricity, Gas & Other Fuels',
        '05': 'Furnishings, Household Equipment',
        '06': 'Health',
        '07': 'Transport',
        '08': 'Communication',
        '09': 'Recreation Services & Culture',
        '10': 'Education',
        '11': 'Restaurants & Hotels',
        '12': 'Miscellaneous Goods & Services',
        '13': 'Overall'
    }
    # Clean up category column: strip whitespace, map codes, then title case to merge 'overall'/'Overall'
    df['category'] = df['category'].astype(str).str.strip()
    df['category'] = df['category'].replace(category_map)
    df['category'] = df['category'].str.title()
    
    return df

try:
    cpi_df = load_cpi_data()

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        categories = ['All'] + sorted(cpi_df['category'].unique().tolist())
        selected_category = st.selectbox("Select Category", categories)

    with col2:
        years = sorted(cpi_df['date'].dt.year.unique(), reverse=True)
        selected_year = st.selectbox("Select Year", ['All'] + list(years))

    # Filter data
    filtered_df = cpi_df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['date'].dt.year == selected_year]

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        latest = filtered_df.iloc[0] if len(filtered_df) > 0 else None
        st.metric("Latest CPI Value", f"{latest['value']:.1f}" if latest is not None else "N/A")

    with col2:
        avg_mom = filtered_df['mom_change_pct'].mean() if 'mom_change_pct' in filtered_df.columns else 0
        st.metric("Average MoM Change", f"{avg_mom:.2f}%")

    with col3:
        avg_yoy = filtered_df['yoy_change_pct'].mean() if 'yoy_change_pct' in filtered_df.columns else 0
        st.metric("Avg YoY Change", f"{avg_yoy:.2f}%")

    # CPI Trend Chart
    st.subheader("CPI Trend Over Time")
    fig = px.line(
        filtered_df.sort_values('date'),
        x='date',
        y='value',
        color='category' if selected_category == 'All' else None,
        title='CPI Index Value',
        labels={'date': 'Date', 'value': 'CPI Index'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # YoY Change Chart
    if 'yoy_change_pct' in filtered_df.columns:
        st.subheader("Year-over-Year Inflation Rate")
        fig2 = px.bar(
            filtered_df.sort_values('date').dropna(subset=['yoy_change_pct']),
            x='date',
            y='yoy_change_pct',
            color='yoy_change_pct',
            color_continuous_scale=['green', 'yellow', 'red'],
            labels={'date': 'Date', 'yoy_change_pct': 'Inflation Rate (%)'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Data Table
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the gold.cpi_trends table is populated.")
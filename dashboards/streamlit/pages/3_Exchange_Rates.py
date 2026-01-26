# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from config.database import get_engine

st.set_page_config(page_title="Exchange Rates", page_icon="💱", layout="wide")
st.title("Exchange Rates Analytics")
st.markdown("Daily exchange rates and volatility analysis")

@st.cache_data(ttl=3600)
def load_exchange_data():
    engine = get_engine()
    df = pd.read_sql("""
        SELECT * FROM gold.exchange_rate_analytics
        WHERE date >= CURRENT_DATE - INTERVAL '365 days'
        ORDER BY date DESC
    """, engine)
    return df

try:
    fx_df = load_exchange_data()

    # Currency Names Mapping
    currency_names = {
        'AED': 'UAE Dirham',
        'AUD': 'Australian Dollar',
        'BND': 'Brunei Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Renminbi',
        'EGP': 'Egyptian Pound',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'HKD': 'Hong Kong Dollar',
        'IDR': 'Indonesian Rupiah',
        'INR': 'Indian Rupee',
        'JPY': 'Japanese Yen',
        'KHR': 'Cambodian Riel',
        'KRW': 'South Korean Won',
        'KWD': 'Kuwaiti Dinar',
        'LKR': 'Sri Lankan Rupee',
        'MMK': 'Myanmar Kyat',
        'NPR': 'Nepalese Rupee',
        'MYR': 'Malaysian Ringgit',
        'NZD': 'New Zealand Dollar',
        'PHP': 'Philippine Peso',
        'PKR': 'Pakistan Rupee',
        'SAR': 'Saudi Riyal',
        'SEK': 'Swedish Krona',
        'SGD': 'Singapore Dollar',
        'THB': 'Thai Baht',
        'TWD': 'New Taiwan Dollar',
        'USD': 'US Dollar',
        'VND': 'Vietnamese Dong',
        'ZAR': 'South African Rand'
    }

    # Clean and uppercase currency codes
    fx_df['currency_code'] = fx_df['currency_code'].str.upper()
    fx_df['currency_name'] = fx_df['currency_code'].map(currency_names).fillna('Unknown')
    fx_df['display_label'] = fx_df['currency_code'] + " - " + fx_df['currency_name']

    # Currency pair filter
    pairs = sorted(fx_df['display_label'].unique().tolist())
    selected_label = st.selectbox("Select Currency", pairs)
    
    # Extract code back from label for filtering (First 3 chars)
    selected_code = selected_label.split(' - ')[0]
    filtered_df = fx_df[fx_df['currency_code'] == selected_code].sort_values('date')

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    latest = filtered_df.iloc[-1] if len(filtered_df) > 0 else None

    with col1:
        rate = latest['rate'] if latest is not None else 0
        st.metric("Current Rate", f"{rate:.4f}")

    with col2:
        ma_30 = latest.get('ma_7_day', 0) if latest is not None else 0
        st.metric("7-Day MA", f"{ma_30:.4f}" if ma_30 else "N/A")

    with col3:
        volatility = latest.get('volatility_7d', 0) if latest is not None else 0
        st.metric("7-Day Volatility", f"{volatility:.4f}" if volatility else "N/A")

    with col4:
        change = latest.get('daily_change_pct', 0) if latest is not None else 0
        st.metric("Daily Change", f"{change:.2f}%" if change else "N/A")

    # Exchange Rate Chart
    st.subheader(f"{selected_label} Exchange Rate")
    fig = px.line(
        filtered_df,
        x='date',
        y='rate',
        title=f'{selected_label} Daily Rate',
        labels={'date': 'Date', 'rate': 'Exchange Rate'}
    )
    # Add moving average if exists
    if 'ma_7_day' in filtered_df.columns:
        fig.add_scatter(
            x=filtered_df['date'],
            y=filtered_df['ma_7_day'],
            name='7-Day MA',
            line=dict(dash='dash', color='orange')
        )
    st.plotly_chart(fig, use_container_width=True)

    # Volatility Chart
    if 'volatility_7d' in filtered_df.columns:
        st.subheader("7-Day Rolling Volatility")
        fig2 = px.area(
            filtered_df.dropna(subset=['volatility_7d']),
            x='date',
            y='volatility_7d',
            title='Currency Volatility',
            labels={'date': 'Date', 'volatility_7d': 'Volatility'}
        )
        fig2.update_traces(fill='tozeroy', line_color='purple')
        st.plotly_chart(fig2, use_container_width=True)

    # Data Table
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the gold.exchange_rate_analytics table is populated.")
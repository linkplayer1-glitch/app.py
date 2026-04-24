import streamlit as st
import yfinance as yf

# 1. Page Configuration
st.set_page_config(page_title="Gold Rate & PKR Tracker", page_icon="💰")
st.title("💰 Pakistan Gold Rate & USD/PKR Dashboard")

# 2. Fetch Live Financial Data
@st.cache_data(ttl=600)  # Updates every 10 minutes
def fetch_financial_data():
    gold = yf.Ticker("GC=F")  # Gold Futures symbol
    usd_pkr = yf.Ticker("USDPKR=X") # USD to PKR exchange rate
    
    gold_price_usd = gold.history(period="1d")['Close'].iloc[-1]
    exchange_rate = usd_pkr.history(period="1d")['Close'].iloc[-1]
    
    return round(gold_price_usd, 2), round(exchange_rate, 2)

try:
    gold_usd, current_pkr_rate = fetch_financial_data()
    
    # 3. Live Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Global Gold (USD/oz)", f"${gold_usd}")
    with col2:
        st.metric("USD to PKR Exchange Rate", f"Rs. {current_pkr_rate}")

    # 4. Gold Rates in Pakistan (Tola and Gram)
    st.divider()
    st.subheader("🇵🇰 Local Gold Rates")
    
    # Constants for conversion
    # 1 Troy Ounce = 31.1035 grams
    # 1 Tola = 11.6638 grams
    price_per_gram_pkr = (gold_usd / 31.1035) * current_pkr_rate
    price_per_tola_pkr = price_per_gram_pkr * 11.6638
    
    local_col1, local_col2 = st.columns(2)
    local_col1.info(f"**Price Per Tola (24K):**\n\nRs. {price_per_tola_pkr:,.0f}")
    local_col2.info(f"**Price Per 10 Grams (24K):**\n\nRs. {price_per_gram_pkr * 10:,.0f}")

    # 5. Conversion Tool (USD TO PKR)
    st.divider()
    st.subheader("💱 Quick Converter")
    usd_input = st.number_input("Enter Amount in USD:", min_value=0.0, value=1.0)
    pkr_output = usd_input * current_pkr_rate
    st.success(f"${usd_input:,.2f} is equal to **Rs. {pkr_output:,.2f}**")

except Exception as e:
    st.error("Wait! We couldn't fetch live data. Please check your internet connection.")

st.caption("Disclaimer: Prices are based on international spot rates and may differ from local Sarafa Bazaar rates.")

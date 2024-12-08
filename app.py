import streamlit as st
import requests
import pandas as pd
import os
import sys

# Hardcode the API key
API_KEY = "26cda667318b0fbc681e6a082412cfb8"

# Function to fetch stock data
def fetch_stock_data(symbol):
    url = f'http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={symbol}'
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return None

    data = response.json()
    return data

# Get the path to the banner image
def get_banner_path():
    # PyInstaller stores bundled files in a temporary folder during runtime
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "banner.png")
    return "banner.png"

# Streamlit app layout
st.set_page_config(page_title="Pocket Accountant", layout="wide")

# Use the banner image
st.image(get_banner_path(), use_container_width=True)

# App title and description
st.title("Pocket Accountant")
st.markdown("Track your favorite stocks with ease!")

# User input for stock symbol
st.sidebar.title("Stock Analysis")
st.sidebar.markdown("Enter a stock symbol below to retrieve its data:")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT):")

if st.sidebar.button("Get Stock Data"):
    if stock_symbol:
        data = fetch_stock_data(stock_symbol)
        if data and 'data' in data:
            df = pd.DataFrame(data['data'])

            # Convert 'date' column to datetime for better visualization
            df['date'] = pd.to_datetime(df['date'])

            # Display data
            st.subheader(f"Stock Data for {stock_symbol.upper()}")
            st.markdown("### Historical Stock Prices")
            st.write(df[['date', 'close', 'volume']])

            # Line chart for closing prices
            st.markdown("### Closing Prices Over Time")
            st.line_chart(df.set_index('date')['close'])

        else:
            st.error("No data found for the given stock symbol.")
    else:
        st.warning("Please enter a stock symbol.")

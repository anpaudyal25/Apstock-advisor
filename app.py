import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from logic import get_signals, get_recommendation

st.set_page_config(page_title="Pro Stock Analyst", layout="wide")

st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Ticker", value="NVDA")

if ticker:
    try:
        # Fetch Data
        data = yf.download(ticker, period="1y", interval="1d")
        
        if len(data) > 0:
            data = get_signals(data)
            rec, reason = get_recommendation(data)
            
            # Header Section
            col1, col2 = st.columns([2, 1])
            with col1:
                st.title(f"Market Analysis: {ticker}")
            with col2:
                st.metric("Recommendation", rec)

            # Technical Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                         low=data['Low'], close=data['Close'], name="Price"))
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name="20 EMA", line=dict(color='blue')))
            fig.update_layout(height=600, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            # Analysis Card
            st.subheader("Why this decision?")
            st.markdown(f"> **Summary:** {reason}")
            
            # Show Raw Data
            with st.expander("View Technical Indicators"):
                st.write(data.tail(10))
        else:
            st.error("No data found. Check the ticker symbol.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from sentiment_predictor import analyze_market_sentiment
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="FINANCE WEB APP",
    page_icon="💲",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('FINANCE WEB APP')
st.image('cover-superdark.png')

with st.sidebar:
    st.markdown("Start Date")
    di = st.date_input("Write the start date", datetime.date(2020, 1, 1))
    st.divider()
    st.markdown("End Date")
    df = st.date_input("Write the end date", datetime.date(2024, 1, 1))
if di<df:
    st.write("")
elif di>df:
    st.write("The end date must be greater than the start date ❌",color="r")
    

st.subheader('Stocks data visualization',divider='gray')
# Lista de símbolos de acciones
company = ['AAPL','AMZN','GOOGL','JPM','LVMUY','META','NVDA','TSLA','V','WNT','XOM']

# Crear una lista desplegable para seleccionar la acción
seleccion_accion = st.selectbox("Selecciona una acción", company)

st.header("Data Visualization")
stock_data = yf.Ticker(seleccion_accion)
last_price = stock_data.history(period='1d')['Close'].iloc[-1]
last_price_rounded = round(last_price, 2)
st.write('Actual Price')
# Mostrar el precio en Streamlit con formato

# Establecer el color de texto en verde y el tamaño de fuente a 24
st.write(
    f"<span style='color:green; font-size:24px;'>Actual Price for {seleccion_accion} is: <b>{last_price_rounded} $</b></span>", 
    unsafe_allow_html=True
)

datos_accion = yf.download(seleccion_accion, start=di, end=df)
df=pd.DataFrame(datos_accion)
df=df.drop(columns=['Adj Close'])
st.write("Historical data for ", seleccion_accion)
st.dataframe(df,use_container_width=True)

st.divider()
st.header("Chart Visualization")

chart_data=datos_accion
st.line_chart(chart_data,y=['High','Low'],use_container_width=True)
st.header(f'{seleccion_accion} Metrics')
empresa = yf.Ticker(seleccion_accion)
balance_general = empresa.balance_sheet
ingresos = empresa.financials
flujos_efectivo = empresa.cashflow
tab1, tab2, tab3 = st.tabs(["Balance Sheet", "Income Statement", "Cash Flow"])
with tab1:
    st.subheader("Balance Sheet")
    st.dataframe(balance_general,use_container_width=True,height=500) 
with tab2:
    st.subheader("Income Statement")
    st.dataframe(ingresos,use_container_width=True,height=500)   
with tab3:
    st.subheader("Cash Flow")
    st.dataframe(flujos_efectivo,use_container_width=True,height=500)  

st.subheader('Market Sentiment')
symbol=seleccion_accion
market_sentiment = analyze_market_sentiment(symbol)
if market_sentiment is not None:
    st.markdown(f"The average market sentiment for {symbol} is : {market_sentiment}")
    if market_sentiment<0 and market_sentiment<-0.4:
        st.write('***:red[Strong Sell]***')
    elif market_sentiment>0 and market_sentiment>0.4:
        st.markdown('***:green[Strong Buy]***')
    elif market_sentiment<0:
        st.write('***:red[Sell]***')
    elif market_sentiment>0:
        st.write('***:green[Buy]***')

else:
    st.write(f"No news found to analyze market sentiment for {symbol}")






    

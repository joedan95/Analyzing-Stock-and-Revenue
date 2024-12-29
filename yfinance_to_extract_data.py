import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore", category=FutureWarning)

gamestop=yf.Ticker('GME')
gamestop_data=gamestop.history(period='max')
gamestop_data.reset_index(inplace=True)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print(gamestop_data.head(5))

url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
data=requests.get(url).text
soup=BeautifulSoup(data,'html.parser')
gamestop_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for row in soup.find_all('tbody')[1].find_all('tr'):
    col = row.find_all('td')
    Date = col[0].text
    Revenue = col[1].text
    gamestop_revenue = pd.concat([gamestop_revenue, pd.DataFrame({"Date": [Date], "Revenue": [Revenue]})], ignore_index=True)

gamestop_revenue["Revenue"] = gamestop_revenue['Revenue'].str.replace('$',"")
gamestop_revenue["Revenue"] = gamestop_revenue['Revenue'].str.replace(',',"")
gamestop_revenue.dropna(inplace=True)
gamestop_revenue = gamestop_revenue[gamestop_revenue['Revenue'] != ""]
gamestop_revenue["Revenue"] = pd.to_numeric(gamestop_revenue["Revenue"], errors="coerce")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

print(gamestop_revenue.tail(5))

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(showlegend=False, height=900,title=stock, xaxis_rangeslider_visible=True)
    fig.show()

make_graph(gamestop_data,gamestop_revenue,"Gamestop")
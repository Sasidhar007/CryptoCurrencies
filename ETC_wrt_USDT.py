
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import time
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
from pandas import datetime
import datedelta
import plotly
plotly.tools.set_credentials_file(username='', api_key='')
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


# In[2]:


s = requests.get(url='https://poloniex.com/public?command=returnChartData&currencyPair=USDT_ETC&end=9999999999&period=14400&start=1405699200')


# In[3]:


dfETC = pd.DataFrame.from_records(s.json())


# In[4]:


start =time.time()#works but first create a column wiht DateTime
dfETC['DateTime'] = pd.Series(np.random.randn(len(dfETC)), index=dfETC.index)
for i, row in dfETC.iterrows():
    dfETC.loc[i,'DateTime'] = datetime.fromtimestamp(row['date']).strftime("%m-%d-%Y %H:%M:%S")#instead of .loc you can also use at for future purposes
dfETC['DateTime'] =  pd.to_datetime(dfETC['DateTime'], format='%m-%d-%Y %H:%M:%S')
end = time.time()
print(end - start)


# In[5]:


#Using Roller to generate Moving Averages(Simple). Here we re multiplying by 6 cos each day has 6 recordings
#roller = dfETC['close'].rolling(10*6)
#dfETC['10DayMA'] = roller.mean()

#roller = dfETC['close'].rolling(30*6)
#dfETC['30DayMA'] = roller.mean()

#roller = dfETC['close'].rolling(50*6)
#dfETC['50DayMA'] = roller.mean()

dfETC['5DayMA'] = dfETC['close'].ewm(span=30, adjust=False).mean()

dfETC['10DayMA'] = dfETC['close'].ewm(span=60, adjust=False).mean()

dfETC['30DayMA'] = dfETC['close'].ewm(span=180, adjust=False).mean()

dfETC['50DayMA'] = dfETC['close'].ewm(span=300, adjust=False).mean()


# In[6]:


data = [
    go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['close'],
        name = 'Closing Price ETC'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['50DayMA'],
        name = '50DayMA'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['30DayMA'],
        name = '30DayMA'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['10DayMA'],
        name = '10DayMA'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['5DayMA'],
        name = '5DayMA'
    )#,
    #go.Candlestick(x=dfETC.DateTime,
     #                  open=dfETC.open,
                       #high=dfETC.high,
                       #low=dfETC.low,
                       ##close=dfETC.close,
                       #increasing=dict(line=dict(color= '#17BECF')),
                       #decreasing=dict(line=dict(color= '#7F7F7F')))
]
# IPython notebook
plotly.offline.iplot(data)


# In[7]:


#Using Roller to generate Moving Averages(Simple) for Volume
#roller = dfETC['volume'].rolling(10*6)
#dfETC['Vol10DayMA'] = roller.mean()

#roller = dfETC['volume'].rolling(30*6)
#dfETC['Vol30DayMA'] = roller.mean()

#roller = dfETC['volume'].rolling(50*6)
#dfETC['Vol50DayMA'] = roller.mean()

dfETC['Vol5DayMA'] = dfETC['volume'].ewm(span=30, adjust=False).mean()

dfETC['Vol10DayMA'] = dfETC['volume'].ewm(span=60, adjust=False).mean()

dfETC['Vol30DayMA'] = dfETC['volume'].ewm(span=180, adjust=False).mean()

dfETC['Vol50DayMA'] = dfETC['volume'].ewm(span=300, adjust=False).mean()


# In[8]:


data = [
    go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['volume'],
        name = 'Volume ETC'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Vol50DayMA'],
        name = '50DayMA - Volume'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Vol30DayMA'],
        name = '30DayMA - Volume'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Vol10DayMA'],
        name = '10DayMA - Volume'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Vol5DayMA'],
        name = '5DayMA - Volume'
    )
    #,
    #go.Candlestick(x=dfETH.DateTime,
     #                  open=dfETH.open,
      #                 high=dfETH.high,
       #                low=dfETH.low,
        #               close=dfETH.close,
         #              increasing=dict(line=dict(color= '#17BECF')),
          #             decreasing=dict(line=dict(color= '#7F7F7F')))
]
# IPython notebook
plotly.offline.iplot(data)


# In[9]:


#New try, Volatility window is for 3 days shift should be done -1 since we are comparing results with 1 up 

dfETC['Returns'] = ((dfETC['close'] / dfETC['close'].shift(-1)) - 1)
dfETC['Volatility'] = pd.rolling_std(dfETC['Returns'], window=18)


# In[10]:


#Using Roller to generate Moving Averages(Simple) for Volatility
#roller = dfETC['Volatility'].rolling(10*6)
#dfETC['Volatility10DayMA'] = roller.mean()

#roller = dfETC['Volatility'].rolling(30*6)
#dfETC['Volatility30DayMA'] = roller.mean()

#roller = dfETC['Volatility'].rolling(50*6)
#dfETC['Volatility50DayMA'] = roller.mean()


dfETC['Volatility5DayMA'] = dfETC['Volatility'].ewm(span=30, adjust=False).mean()

dfETC['Volatility10DayMA'] = dfETC['Volatility'].ewm(span=60, adjust=False).mean()

dfETC['Volatility30DayMA'] = dfETC['Volatility'].ewm(span=180, adjust=False).mean()

dfETC['Volatility50DayMA'] = dfETC['Volatility'].ewm(span=300, adjust=False).mean()


# In[11]:


dfETC['meanLineVolatility'] = dfETC['Volatility'].mean()


# In[12]:


data = [
    go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['meanLineVolatility'],
        name = 'Volatility mean ETC'
    ),
    go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['Volatility'],
        name = 'Volatility'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Volatility10DayMA'],
        name = '10DayMA - Volatility'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Volatility5DayMA'],
        name = '5DayMA - Volatility'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Volatility30DayMA'],
        name = '30DayMA - Volatility'
    ),
    go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['Volatility50DayMA'],
        name = '50DayMA - Volatility'
    )#,
    #go.Candlestick(x=dfETH.DateTime,
     #                  open=dfETH.open,
      #                 high=dfETH.high,
       #                low=dfETH.low,
        #               close=dfETH.close,
         #              increasing=dict(line=dict(color= '#17BECF')),
          #             decreasing=dict(line=dict(color= '#7F7F7F')))
]
# IPython notebook
plotly.offline.iplot(data)



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
plotly.tools.set_credentials_file(username='sasi_ynwa', api_key='wEm5TtVT8TOVKzFyd8CA')
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

#Below I am defining various traces will then use them to plot subplots
trace1 = go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['5DayMA'],
        name = '5DayMA'
    )

trace2 = go.Scatter(
                x=dfETC['DateTime'], # assign x as the dataframe column 'x'
                y=dfETC['close'],
                name = 'Closing Price ETC'
            )
trace3 = go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['10DayMA'],
        name = '10DayMA'
    )

trace4 = go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['volume'],
        name = 'Volume ETC'
    )

trace5 = go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['Volatility'],
        name = 'Volatility'
    )

fig = tools.make_subplots(rows=3, cols=2, specs = [[{'rowspan': 2, 'colspan': 2}, None],
                                                   [None, None],
                                                   [{}, {}]
                                                  ],print_grid=True)

fig.append_trace(trace2, 1, 1)
fig.append_trace(trace4, 3, 1)
fig.append_trace(trace5, 3, 2)

fig['layout'].update(height=750, width=750, title='Price, Volume and Volatility')
plotly.offline.iplot(fig)


#this below is for stacked subplots
fig2 = tools.make_subplots(rows=3, cols=1)

fig2.append_trace(trace2, 1, 1)
fig2.append_trace(trace4, 2, 1)
fig2.append_trace(trace5, 3, 1)


fig2['layout'].update(height=600, width=600, title='Price, Volume and Volatility Stacked subplots')
plotly.offline.iplot(fig2)


#below is for generating Candlestick plot , Volume and Moving Averages
trace2 = go.Bar(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['volume'],
        name = 'Volume ETC'
    )


trace4 = go.Scatter(
                x=dfETC['DateTime'], # assign x as the dataframe column 'x'
                y=dfETC['close'],
                name = 'Closing Price ETC',
    yaxis = 'y2'
            )

trace3 = go.Scatter(
        x=dfETC['DateTime'], # assign x as the dataframe column 'x'
        y=dfETC['10DayMA'],
        name = '10DayMA', 
    yaxis = 'y2'
    )

trace7 = go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['30DayMA'],
        name = '30DayMA',
    yaxis = 'y2'
    )
trace8 =     go.Scatter(
        x = dfETC['DateTime'],
        y = dfETC['5DayMA'],
        name = '5DayMA',
    yaxis = 'y2'
    )
trace6 = go.Candlestick(x=dfETC.DateTime,
                       open=dfETC.open,
                       high=dfETC.high,
                       low=dfETC.low,
                       close=dfETC.close,
                       increasing=dict(line=dict(color= '#00ff00')),
                       decreasing=dict(line=dict(color= '#FF0000')),
                       yaxis='y2')


data = [trace2, trace3, trace6, trace7, trace8]#, trace6]
layout = go.Layout(
    title='Volume and Price (Candlestick) Overlayed with each other ',
    yaxis=dict(
        title='Volume ETC'
    ),
    yaxis2=dict(
        title='Closing Price of ETC',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    )
)
fig3 = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig3)

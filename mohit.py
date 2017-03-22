import quandl
import requests
import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame
import datetime
import numpy as np
import matplotlib.patches as mpatches
from math import sqrt
#http://techpaisa.com/stock/tcs/

quandl.ApiConfig.api_key = 'Hqu7HLNnBU4bxBU4jLaZ'


#dataset = [1,2,3,4,5,6,7,8,9,7,8,9,4,5,6,1,2,3,3,3,2,2,1,11,22,2,2,5,5,11,22,55,1,17,22,2,11,1,5,23,5,5,55,55,55,5,5]

def drawChartSMA(close,date,sma):
    y =close
    x =date
    plt.plot(x,y,'g',label='Stock Price')
    plt.plot(x,sma,'r',label='SMA')
    plt.xlabel('Date')
    plt.ylabel('Prices/SMA')
    plt.title('SMA')
    plt.legend()
    l=len(close)
    k=l-20;
    min = close[k]
    max = close[k]
    for t in range(k,l):
        if(close[t]<min):
          min=close[t]
        if(close[t]>max):
          max=close[t]

    if(sma[len(sma)-1]<close[len(close)-1]):
        print("SMA says Uptrend")
        print("Support is Rs." , min)
        print("Resistance is Rs.", max)
    elif(sma[len(sma)-1]>close[len(close)-1]):
        print("SMA says Downtrend")
        print("Support is Rs." , min)
        print("Resistance is Rs.", max)
    else:
        print("Trend Reversal may occur")
        print("Support is Rs." , min)
        print("Resistance is Rs.", max)
    plt.show() 

def movingaverage(values,window):
    weights = np.repeat(1.0,window)/window
    smas = np.convolve(values,weights,'valid').tolist()  
    listt=list()
    for c in range(0,window-1):
          listt.append(0)
    smas = listt+smas
    for m in range(0,len(smas)):
        smas[m] = float("{0:.2f}".format(smas[m]))     
    return smas


def ExpMovingAverage(values,window):
    weights=np.exp(np.linspace(-1.,0.,window))
    weights/=weights.sum()
    a=np.convolve(values,weights,mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def computeMACD(x,slow=26,fast=12):
    emaslow = ExpMovingAverage(x,slow)
    emafast = ExpMovingAverage(x,fast)    
    return emaslow,emafast,emafast-emaslow


def rsiFunc(close,n,date):
    deltas = np.diff(close)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down  = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(close)
    rsi[:n] = 100. - 100./(1+rs)
    for i in range(n,len(close)):
        delta = deltas[i-1]
        if delta > 0 :
           upval=delta
           downval = 0.
        else:
           upval = 0.
           downval = -delta
        up=(up*(n-1)+upval)/n
        down=(down*(n-1)+downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
        rsi[i] = float("{0:.2f}".format(rsi[i]))
    plt.plot(date,close.tolist(),label="Stock Price")
    plt.plot(date,rsi.tolist(),label="RSI")
    plt.legend()
    plt.title("RSI")
    plt.show()
    return rsi      



def bollinger_band(close,window):
    rolling_mean = 	close.rolling(window=20).mean()
    rolling_std = close.rolling(window=20).std()
    upper_band   = rolling_mean + (rolling_std * 2)
    lower_band   = rolling_mean - (rolling_std * 2)
    cl = close.tolist();
    lo = lower_band.tolist();
    up = upper_band.tolist();
    b = ((cl[len(cl)-1] - lo[len(lo)-1])/(up[len(up)-1]-lo[len(lo)-1]))
    print("%B is:",float("{0:.2f}".format(b*100)),'%')
    return rolling_mean, upper_band, lower_band
       


    


def plotMACD(close,ema9,emaslow,emafast,macd,date):
    plt.plot(date,emaslow.tolist(),label="slow")
    plt.plot(date,emafast.tolist(),label="fast")
    plt.plot(date,macd.tolist(),label="macd")
    plt.plot(date,ema9.tolist(),label="ema9")
    plt.plot(date,close,label="closing prices")
    plt.title("MACD")
    plt.legend()
    plt.show() 

    

def plotB_band(b,c,date,close):
    plt.title("Bollinger Band")
    plt.plot(date,b,label="upper band")
    plt.plot(date,c,label="lower band")
    plt.plot(date,close,label="closing prices")
    plt.title("Bollinger Bands")
    plt.legend()
    plt.show()


def plotEMA(ema50,ema20,date,close):
    plt.plot(date.tolist(),ema20,'g',label="EMA-20")
    plt.plot(date.tolist(),ema50,'o',label="EMA-50")
    plt.plot(date.tolist(),close,'r',label="Stock price")
    plt.legend()
    plt.title("EMA")
    plt.show()




try:
    name = input("Enter Ticker:")
    url = "https://www.quandl.com/api/v3/datasets/NSE/"+name+"/metadata.json"
    try:
        meta_data = requests.get(url)  
        parsed_meta_data = meta_data.json()
        print("Name: {}".format(parsed_meta_data['dataset']['name']))
        print("Technical Analysis Report:","".format(parsed_meta_data['dataset']['name']))
        searched_data = quandl.get("NSE/"+name)
        close = searched_data.Close
        n=20
        sma=movingaverage(close.tolist(),n)
        ema50=ExpMovingAverage(close,50)
        ema20=ExpMovingAverage(close,20)
        ema50 = ema50.tolist();
        ema20 = ema20.tolist();
        for x in range(0,len(ema50)):
            ema50[x] = float("{0:.2f}".format(ema50[x]))
            ema20[x] = float("{0:.2f}".format(ema20[x]))
    
     
        date=pandas.to_datetime(searched_data.index)
        drawChartSMA(close.tolist(),date.tolist(),sma)
        plotEMA(ema50,ema20,date,close)
        nema =9
        emaslow,emafast,macd = computeMACD(close)
        ema9 = ExpMovingAverage(macd,nema) 
        print("MACD:",float("{0:.2f}".format(macd[len(macd)-1])),"and Signal Line:",float("{0:.2f}".format(ema9[len(ema9)-1])))
        plotMACD(close,ema9,emaslow,emafast,macd,date.tolist())
        rsi = rsiFunc(close,14,date.tolist())
        print("RSI is:",rsi[len(rsi)-1])
        if rsi[len(rsi)-1]>70:
           print("Stock may be Overbought")
        if rsi[len(rsi)-1]<30:
           print("Stock may be Oversold")
        a,b,c = bollinger_band(close,20)
        a[:19]=0
        b[:19]=0
        c[:19]=0   
        plotB_band(b.tolist(),c.tolist(),date.tolist(),close.tolist())
    except Exception:
        print("May be No. Of Attempts for today by the key is finished")
except Exception:
    print("Check your Internet Connection")

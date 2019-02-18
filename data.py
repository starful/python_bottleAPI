from bottle import route, run, template, request, static_file
# from bottle import post, get, put, delete, request, response
from bottledaemon import daemon_run
import pandas as pd
import numpy as np
from pandas import *
from pylab import *
import matplotlib.pyplot as plt
from numpy.random import randn
import matplotlib.dates as mdates
from fbprophet import Prophet
from fbprophet import diagnostics

def serve_pictures(picture):
    plt.show()
    plt.savefig(picture)	
    return static_file(picture, root='/opt/api/data/')

def read_file():
    return pd.read_csv("/opt/api/data/USDJYP.csv")
    
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

@route('/chart1')
def chart():
    df = read_file()
    df['start_point'].plot()

    #白紙のキャンバス？を生成
    fig = plt.figure()
    #1行、1列の1個目の図を描くエリアを用意
    ax = fig.add_subplot(1,1,1)
    #dataを用意 xとyの個数は一致しておく必要あり
    x = df['day']
    y = df['start_point']
    #データをセット（プロット）
    ax.plot(x,y)

    return serve_pictures("image1.png")

@route('/chart2')
def chart():
	df = read_file()
	df['day'['start_point','high_point','low_point','end_point']].plot(figsize=(8,4), grid=True)
	return serve_pictures("image2.png")

@route('/chart3')
def chart():
    df = read_file()
    df.plot(kind='hist', x='day' , bins=10, figsize=(16,4), alpha=0.5)
    return serve_pictures("image3.png")

@route('/chart4')
def chart():
    df = read_file()
    df.plot(subplots=True, figsize=(6, 6)); plt.legend(loc='best')
    return serve_pictures("image4.png")

@route('/chart5')
def chart():
    df = read_file()
    fig, axes = plt.subplots(nrows=2, ncols=2)
    df['start_point'].plot(ax=axes[0,0]); axes[0,0].set_title('A')
    df['high_point'].plot(ax=axes[0,1]); axes[0,1].set_title('B')
    df['low_point'].plot(ax=axes[1,0]); axes[1,0].set_title('C')
    df['end_point'].plot(ax=axes[1,1]); axes[1,1].set_title('D')
    return serve_pictures("image5.png")

@route('/chart6')
def chart():
    df = read_file()
    # df.plot(subplots=True, figsize=(6, 6)); plt.legend(loc='best')
    
    # response_text = requests.get("https://raw.githubusercontent.com/pandas-dev/pandas/master/pandas/tests/data/iris.csv").text
    # df = pd.read_csv(io.StringIO(response_text))
    # df = pd.DataFrame(data = d)
    print("Data Frame")
    print(df)
    print()

    print("Correlation Matrix")
    print(df.corr())
    print()

    return serve_pictures("image6.png")

@route('/fb1')
def chart():
    df = read_file()
    df.head()

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    fig1 = m.plot(forecast,ylabel="USD_JYP")
    title('My Title')
    return serve_pictures("image1.png")

@route('/fb2')
def chart():
    df = read_file()
    df.head()

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    fig2 = m.plot_components(forecast)
    return serve_pictures("image2.png")

@route('/fb3')
def chart():
    df = read_file()
    df.head()

    m = Prophet()
    m.fit(df)

    cv = diagnostics.cross_validation(m, horizon='365 days')
    cv.tail()
    m.plot_components(cv)
    return serve_pictures("image3.png")

if __name__ == "__main__":
    run(host='0.0.0.0', port=80)
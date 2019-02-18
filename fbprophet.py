from bottle import route, run, template, request, static_file
import pandas as pd
from fbprophet import Prophet
from fbprophet import diagnostics

def serve_pictures(picture):
    plt.show()
    plt.savefig(picture)	
    return static_file(picture, root='/opt/api/fbprophet/img/')

def read_file():
    return pd.read_csv("/opt/api/fbprophet/data/USDJPY.csv")
    
@route('/fb1')
def chart():
    df = read_file()
    df.head()

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'y']].tail()

    fig1 = m.plot(forecast,ylabel="USDJPY")
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
    forecast[['ds', 'y']].tail()

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
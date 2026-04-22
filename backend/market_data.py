import requests

API_KEY = "068070ffbcf34c0995ce2921f3ba223b"

def get_xauusd_data():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": "15min",
        "outputsize": 50,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data
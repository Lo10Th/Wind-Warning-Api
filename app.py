from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return 'Here is space for Documentation'

@app.route('/api', methods=['GET'])
def api():
    lat = 51.273310
    long = 7.115120
    APIKEY = os.environ.get('API_KEY')
    if APIKEY is None:
        raise Exception('API_KEY not found in environment variables. You have to add the Apikey from OpenWeatherMap to your environment variables.')
    weatherList = []
    
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=minutely,daily,&appid={APIKEY}&units=metric'
    response = requests.get(url)
    
    now = datetime.now()
    current_hour = now.hour
    hours_until_21 = (21 - current_hour) % 24

    for i in range(13):
        weatherList.append(response.json()['hourly'][hours_until_21 + i]['wind_speed'])

    maxWind = max(weatherList)
    maxWindIndex = weatherList.index(maxWind)
    maxWindTime = 21 + maxWindIndex
    if maxWindTime > 24:
        maxWindTime = maxWindTime - 24

    if maxWind < 10:
        warning = 'green'
    elif maxWind < 20:
        warning = 'yellow'
    else:
        warning = 'red'

    data = {
        'warning': warning,
        'maxWind': maxWind,
        'maxWindTime': maxWindTime
    }

    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
from flask import Flask, render_template, request, Response, jsonify,make_response
from weather_station_BYO import measure_data
from database import MariaDBDatabase, WeatherDatabase
import datetime

app = Flask(__name__, template_folder='templates')

#------------------------Connect to the MariaDB-------------------------
#Connects to the database
db = WeatherDatabase()

@app.route("/")
def index():
    current_data = get_current_data()
    return render_template('current_weather.html', current_data=get_current_data)

# API endpoint to get the latest weather data
@app.route('/api/current_data')
def get_current_data():
    #data = measure_data(interval=10)  # Call your function to get the latest weather data
    data = db.get_latest_data()
    
    # List of column names in the order of the MariaDB returned as a tuple
    #column_names = ['ID', 'REMOTE_ID', 'AMBIENT_TEMPERATURE', 'GROUND_TEMPERATURE', 'AIR_QUALITY', 'AIR_PRESSURE', 'HUMIDITY', 'WIND_DIRECTION', 'WIND_SPEED', 'WIND_GUST_SPEED', 'RAINFALL', 'DEWPOINT', 'ALTITUDE','CREATED']
    
    # Create a dictionary from the tuple
    data_dict = data[0]
    if data_dict:
        result = {'ambient_temp': data_dict['AMBIENT_TEMPERATURE'],
        'ground_temp': data_dict['GROUND_TEMPERATURE'],
        'air_quality': data_dict['AIR_QUALITY'],
        'air_pressure': data_dict['AIR_PRESSURE'],
        'humidity': data_dict['HUMIDITY'],
        'wind_average': data_dict['WIND_DIRECTION'],
        'wind_speed': data_dict['WIND_SPEED'],
        'wind_gust': data_dict['WIND_GUST_SPEED'],
        'rainfall': data_dict['RAINFALL'],
        'dewpoint': data_dict['DEWPOINT'],
        'altitude': data_dict['ALTITUDE']
    }
        return jsonify(result)
    else:
        return jsonify({'error': 'No data returned'})

# API endpoint to get historical weather data
@app.route('/api/historical_data')
def get_historical_data():
    rain = database.get_rainfall_data_last_7_days()
    pressure = database.get_pressure_data_last_24_hours()
    historical_data = {
        'rainfallLabels': format_date_labels(rain[1]),
        'rainfallData': rain[0],
        'pressureLabels': format_time_labels(pressure[1]),
        'pressureData': pressure[0]
    }
    return jsonify(historical_data)

def format_date_labels(dates):
    # Convert dates from "YYYY-MM-DD" to "DD/MM" format
    formatted_labels = [datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m") for date in dates]
    return formatted_labels

def format_time_labels(times):
    # Convert times from "HH:MM" to "HH:MM" format
    formatted_labels = [datetime.strptime(time, "%H:%M:%S").strftime("%H:%M") for time in times]
    return formatted_labels

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
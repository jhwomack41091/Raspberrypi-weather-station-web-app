import time
from database import MariaDBDatabase, WeatherDatabase
from weather_station_BYO import measure_data

#------------------------Connect to the MariaDB-------------------------
#Connects to the database
db = WeatherDatabase()

# Set the interval for the loop
data_collection_interval = 10 # Interval to measure in sec (5min=5*60-->300)

# Continous loop to log data
try:
    while True:
        data = measure_data(interval=data_collection_interval)
        print("Inserting...")
        print('Air Temp: {:05.2f}*C \nGround Temp: {:05.2f}*C \nAir Quality: {:05.2f} \nPressure: {:05.2f}hPa \nHumidity: {:05.2f}% \nWind Direction: {:05.2f} \nWind Speed: {:05.2f}km/hr \nWind Gust: {:05.2f}km/hr \nRainFall: {:05.2f}mm \nDewpoint: {:05.2f}*C \nAltitude: {:05.2f}m'.format(*data))
        db.insert(*data)
        print("Done")
        time.sleep(data_collection_interval)
except KeyboardInterrupt:
    print("Script interrupted manually.")
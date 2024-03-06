from gpiozero import Button
from weather_data import WindData, RainData, GroundTemperatureData
from sensors.bme280_sensor0 import read_all as bme280_read_all
import math
import time
import statistics

# Instantiate objects from the modules
wind_data = WindData()
rain_data = RainData()
ground_temp_data = GroundTemperatureData()

#------------------------Rain Measurment Code--------------------------

#Rain variables
rain_sensor = Button(6)
    
rain_sensor.when_pressed = rain_data.bucket_tipped

#------------------------Wind Measurement Code-------------------------

#Wind variables
#wind_interval = 5 by default How often (secs) to report speed
store_speeds = []
store_directions = []
gust = 0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = wind_data.spin

#------------------------Air Quality Measurement Code-------------------
air_quality = 0

# Code for determining air quality goes here from appropriate sensor

#------------------------Main measurement Code-------------------------
def measure_data(interval=10, wind_interval=5):
    print(interval)
    print(wind_interval)
    global store_directions
    global store_speeds
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        wind_data.reset_wind()
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_data.get_wind_direction(duration=wind_interval))
        
        final_speed = wind_data.calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    
    #Get average wind direction, wind gust, mean windspeed values
    wind_average = wind_data.get_average_angle(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    
    #Get rain fall in mm
    rainfall = rain_data.calculate_rainfall()
    rain_data.reset_rainfall()
    
    #Get Humidity, Pressure, Ambient_Temp from the bme280
    humidity, pressure, ambient_temp, altitude, dewpoint = bme280_read_all()
    
    store_speeds = []
    store_directions = []
    
    #Get ground temp from probe
    ground_temp = ground_temp_data.get_ground_temp()
    
    return ambient_temp, ground_temp, air_quality, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall, dewpoint, altitude
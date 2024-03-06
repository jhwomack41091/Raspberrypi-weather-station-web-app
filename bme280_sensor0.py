import board
import time
import math #For calculating dew point
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C() # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level (mPa = mb)
bme280.sea_level_pressure = 1000.00

#Math for Calculating Dew Point
b = 17.62
c = 243.12
gamma = (b * bme280.temperature / (c + bme280.temperature)) + math.log(bme280.humidity / 100.0)
dewpoint = (c * gamma) / (b - gamma)
humidity = bme280.relative_humidity
pressure = bme280.pressure
temperature = bme280.temperature
altitude = bme280.altitude
#print('\nTemperature: {:05.2f}*C \nPressure: {:05.2f}hPa \nHumidity:{:05.2f}% \nAlt: {:05.2f}m \nDewpoint: {:05.2f}*C'.format(temperature, pressure, humidity, altitude, dewpoint))

def read_all():
    
    return humidity, pressure, temperature, altitude, dewpoint

#while True:
#    print("\nTemperature: %0.1fF" % (((bme280.temperature * 9) / 5) + 32),"/%0.1fC" % bme280.temperature)
#    print("Humidity: %0.1f %%" % bme280.relative_humidity)
#    print("Pressure: %0.1f mb" % bme280.pressure)
#    print("Altitude = %0.1fft" % (bme280.altitude * 3.28084),"/%0.1fm" % bme280.altitude)
#    print("Dew Point: %0.1fF" % (((dewpoint * 9) / 5) + 32),"/%0.1fC" % dewpoint)
#    time.sleep(2)
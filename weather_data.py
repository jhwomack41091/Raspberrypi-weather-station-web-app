# weather_data.py
from sensors.ds18b20_therm import DS18B20
from gpiozero import MCP3008
import math
import statistics
import time


CM_IN_A_KM = 100000.0
KM_IN_A_MI = 1.609344
SECS_IN_AN_HOUR = 3600

class WindData:
    values = []  # Class attribute
    volts = {0.4: 0.0,
             1.4: 22.5,
             1.2: 45.0,
             2.8: 67.5,
             2.7: 90.0,
             2.9: 112.5,
             2.2: 135.0,
             2.5: 157.5,
             1.8: 180.0,
             2.0: 202.5,
             0.7: 225.0,
             0.8: 247.5,
             0.1: 270.0,
             0.3: 292.5,
             0.2: 315.0,
             0.6: 337.5}  # Class attribute
    # wind_count: Counts how many half-rotations of the anemometer
    #radius_cm: Radius of the anemometer in cm
    def __init__(self):
        self.wind_count = 0
        self.gust = 0
        self.adc = MCP3008(channel=0)
    
    # Every half-rotation, add 1 to count
    def spin(self):
        self.wind_count += 1

    # Calculate the wind Speed
    def calculate_speed(self, time_sec, radius_cm=9.0, adjustment=1.18):
        circumference_cm = 2 * math.pi * radius_cm
        rotations = self.wind_count / 2.0
        
    # Calculate distance travelled by a cup in cm
        dist_km = (circumference_cm * rotations) / CM_IN_A_KM

    # Speed = distance / time
        km_per_sec = dist_km / time_sec
        km_per_hour = km_per_sec * SECS_IN_AN_HOUR
        final_speed = km_per_hour * adjustment
        return final_speed

    def reset_wind(self):
        self.wind_count = 0

    def reset_gust(self):
        self.gust = 0
        
    def get_average_angle(self, angles):
        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

    def get_wind_direction(self, duration=5):
        data = []
        print("Measuring wind direction for %d seconds..." % duration)
        start_time = time.time()

        while time.time() - start_time <= duration:
            wind = round(self.adc.value * 3.3, 1)
            if wind in self.volts:
                data.append(self.volts[wind])

        return self.get_average_angle(data)
    
    def degrees_to_cardinal(self, angle):
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                      "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        ix = int((angle + 11.25) / 22.5)
        return directions[ix % 16]

class RainData:
    #BUCKET_SIZE = 0.2794 mm is the volume of each bucket when tipped
    def __init__(self, bucket_size=0.2794):
        self.rain_count = 0
        self.bucket_size = bucket_size

    def calculate_rainfall(self):
        total_rainfall = self.rain_count * self.bucket_size # Measured in mm
        return total_rainfall

    def bucket_tipped(self):
        self.rain_count += 1

    def reset_rainfall(self):
        self.rain_count = 0

class GroundTemperatureData:
    def __init__(self):
        self.temp_probe = DS18B20()

    def get_ground_temp(self):
        return self.temp_probe.read_temp()

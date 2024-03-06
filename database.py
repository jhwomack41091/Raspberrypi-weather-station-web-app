import MySQLdb
import datetime
import os
import configparser
#from dotenv import load_dotenv

def create_tables_if_not_exist(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WEATHER_MEASUREMENT (
            ID BIGINT NOT NULL AUTO_INCREMENT,
            AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
            GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
            AIR_QUALITY DECIMAL(6,2) NOT NULL,
            AIR_PRESSURE DECIMAL(6,2) NOT NULL,
            HUMIDITY DECIMAL(6,2) NOT NULL,
            WIND_DIRECTION DECIMAL(6,2) NULL,
            WIND_SPEED DECIMAL(6,2) NOT NULL,
            WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
            RAINFALL DECIMAL (6,2) NOT NULL,
            DEWPOINT DECIMAL (6,2) NOT NULL,
            ALTITUDE DECIMAL (8,2) NOT NULL,
            CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (ID)
        );
    ''')
    connection.commit()

class MariaDBDatabase:
    def __init__(self):
        # Load environment variable from .env file
        #load_dotenv()
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Access MariaDB credentials from environment variables
        #host = os.environ.get('MYSQL_HOST')
        #username = os.environ.get('MYSQL_USERNAME')
        #password = os.environ.get('MYSQL_PASSWORD')
        #database = os.environ.get('MYSQL_DATABASE')
        host = config['database']['host']
        username = config['database']['username']
        password = config['database']['password']
        database = config['database']['database']
        
        # Connect to the MariaDB database
        self.connection = MySQLdb.connect(host=host, user=username, password=password, database=database)
        create_tables_if_not_exist(self.connection)

    def execute(self, query, params=[]):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

class WeatherDatabase:
    def __init__(self):
        self.db = MariaDBDatabase()
        # Define your SQL queries for insertion, upload, etc.

    def insert(self, ambient_temperature, ground_temperature, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall, dewpoint, altitude, created=None):
        if created is None:
            created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
            INSERT INTO WEATHER_MEASUREMENT (
                AMBIENT_TEMPERATURE, GROUND_TEMPERATURE, AIR_QUALITY, AIR_PRESSURE,
                HUMIDITY, WIND_DIRECTION, WIND_SPEED, WIND_GUST_SPEED,
                RAINFALL, DEWPOINT, ALTITUDE, CREATED
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        params = (ambient_temperature, ground_temperature, air_quality, air_pressure,
                  humidity, wind_direction, wind_speed, wind_gust_speed,
                  rainfall, dewpoint, altitude, created)

        self.db.execute(query, params)

    # Add other methods for querying, updating, uploading, etc.

    def upload(self):
        # Your upload logic goes here
        pass

    def get_latest_data(self):
        query = '''
            SELECT * FROM WEATHER_MEASUREMENT
            ORDER BY CREATED DESC
            LIMIT 1;
        '''
        return self.db.query(query)

    def get_data_last_24_hours(self):
        start_time = datetime.now() - timedelta(hours=24)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

        query = f'''
            SELECT * FROM WEATHER_MEASUREMENT
            WHERE CREATED >= '{start_time_str}'
            ORDER BY CREATED DESC;
        '''
        return self.db.query(query)

    def get_data_last_7_days(self):
        start_time = datetime.now() - timedelta(days=7)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

        query = f'''
            SELECT * FROM WEATHER_MEASUREMENT
            WHERE CREATED >= '{start_time_str}'
            ORDER BY CREATED DESC;
        '''
        return self.db.query(query)

    def get_data_last_month(self):
        start_time = datetime.now() - timedelta(days=30)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

        query = f'''
            SELECT * FROM WEATHER_MEASUREMENT
            WHERE CREATED >= '{start_time_str}'
            ORDER BY CREATED DESC;
        '''
        return self.db.query(query)

    def get_data_last_year(self):
        start_time = datetime.now() - timedelta(days=365)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

        query = f'''
            SELECT * FROM WEATHER_MEASUREMENT
            WHERE CREATED >= '{start_time_str}'
            ORDER BY CREATED DESC;
        '''
        return self.db.query(query)

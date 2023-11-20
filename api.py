import json
import requests
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller one-file mode """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

config_path = resource_path('config.json')

class APIManager:
    @staticmethod
    def get_weather_data(city):
        # Load API key from config.json
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('api_key')

        if not api_key:
            raise ValueError("API key not found in config.json")

        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=params)
        return response.json()

    @staticmethod
    def get_pollution_data(latitude, longitude):
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('api_key')

        if not api_key:
            raise ValueError("API key not found in config.json")

        params = {'lat': latitude, 'lon': longitude, 'appid': api_key}
        response = requests.get('http://api.openweathermap.org/data/2.5/air_pollution', params=params)
        return response.json()
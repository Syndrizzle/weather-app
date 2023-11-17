import json
import requests

class APIManager:
    @staticmethod
    def get_weather_data(city):
        # Load API key from config.json
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('api_key')

        if not api_key:
            raise ValueError("API key not found in config.json")

        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=params)
        return response.json()

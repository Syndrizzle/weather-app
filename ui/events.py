import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import requests 
import io
from api import APIManager
from ui.layout import WeatherUILayout

class WeatherUIEvents:
    def __init__(self, master, layout):
        self.master = master
        self.layout = layout
        self.layout.fetch_button.config(command=self.fetch_weather)

    def fetch_weather(self):
        city = self.layout.city_entry.get()
        weather_data = APIManager.get_weather_data(city)
        latitude = weather_data['city']['coord']['lat']
        longitude = weather_data['city']['coord']['lon']
        pollution_data = APIManager.get_pollution_data(latitude, longitude)
        if weather_data['cod'] == '200':
            self.update_ui(weather_data, pollution_data)
        else:
            self.layout.result_label.config(text='City not found')

    def update_ui(self, weather_data, pollution_data):
        # Display current weather
        current_weather = weather_data['list'][0]
        current_temperature = current_weather['main']['temp']
        current_description = current_weather['weather'][0]['description'].capitalize()
        current_wind_speed = current_weather['wind']['speed']
        current_aqi = pollution_data['list'][0]['components']['pm2_5']
        current_icon_code = current_weather['weather'][0]['icon']
        current_icon_url = f'icons/{current_icon_code}.png'
        current_icon = Image.open(current_icon_url)
        current_icon = current_icon.resize((100, 100), resample=Image.BICUBIC)
        current_icon = current_icon.filter(ImageFilter.SMOOTH)
        current_icon_image = ImageTk.PhotoImage(current_icon)

        self.layout.display_current_weather(current_temperature, current_description, current_icon_image)

        # Display upcoming forecast
        upcoming_forecast = [
            {
                "date_time": forecast['dt_txt'],
                "temperature": forecast['main']['temp'],
                "description": forecast['weather'][0]['description'].capitalize(),
            } for forecast in weather_data['list'][1:]
        ]
        self.layout.display_upcoming_forecast(upcoming_forecast)

        # Display AQI and wind speed
        self.layout.display_aqi_and_wind_speed(current_aqi, current_wind_speed)
        
        self.master.update_idletasks()
        x_position = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) // 2
        y_position = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) // 2
        self.master.geometry(f"+{x_position}+{y_position}")

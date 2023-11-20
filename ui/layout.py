import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFont
from datetime import datetime
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller one-file mode """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

font_path = resource_path("fonts/Raleway.ttf")
custom_font = ImageFont.truetype(font_path)  

class WeatherUILayout:
    def __init__(self, master):
        self.master = master
        self.image_references = []  # Store references to ImageTk.PhotoImage objects

        # UI Elements
        self.city_label = tk.Label(master, text='Enter City:', font=(custom_font, 14))
        self.city_label.grid(row=0, column=0, padx=10, pady=10)

        self.city_entry = tk.Entry(master, font=(custom_font, 14))
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        self.fetch_button = ttk.Button(master, text='Fetch Weather', command=self.handle_weather_fetch)
        self.fetch_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_frame = ttk.Frame(master)
        self.result_frame.grid(row=1, column=0, columnspan=3, pady=10)

        # Current weather
        self.current_frame = ttk.Frame(self.result_frame)
        self.current_frame.pack(pady=10)

        self.current_icon_label = tk.Label(self.current_frame)
        self.current_icon_label.grid(row=0, column=0, padx=10)

        # Treeview for displaying upcoming forecast
        columns = ('Date', 'Temperature (°C)', 'Description')
        self.tree = ttk.Treeview(self.result_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # AQI and wind speed display
        self.aqi_wind_frame = ttk.Frame(self.result_frame)

        self.aqi_wind_label = tk.Label(self.aqi_wind_frame, text='', font=(custom_font, 14))

        # Hide the Treeview and AQI/wind speed when not in use
        self.hide_forecast_info()

    def handle_weather_fetch(self):
        city = self.city_entry.get()
        if city:
            self.layout.events.fetch_weather()
        else:
            # Hide the Treeview and AQI/wind speed
            self.hide_forecast_info()

    def display_weather_info(self, weather_data, pollution_data):
        # Display current weather
        current_weather = weather_data['list'][0]
        current_temperature = current_weather['main']['temp']
        current_description = current_weather['weather'][0]['description'].capitalize()
        current_wind_speed = current_weather['wind']['speed']
        current_aqi = pollution_data['list'][0]['components']['pm2_5']
        current_icon_code = current_weather['weather'][0]['icon']
        current_icon_url = resource_path(f'icons/{current_icon_code}.png')
        current_icon = Image.open(current_icon_url)
        current_icon = current_icon.resize((100, 100), resample=Image.BICUBIC)
        current_icon_image = ImageTk.PhotoImage(current_icon)
        self.display_current_weather(current_temperature, current_description, current_icon_image)

        # Display upcoming forecast
        upcoming_forecast = [
            {
                "date_time": forecast['dt_txt'],
                "temperature": forecast['main']['temp'],
                "description": forecast['weather'][0]['description'].capitalize(),
            } for forecast in weather_data['list'][1:]
        ]
        self.display_upcoming_forecast(upcoming_forecast)

        # Display AQI and wind speed
        self.display_aqi_and_wind_speed(current_aqi, current_wind_speed)

    def display_current_weather(self, temperature, description, icon_image):
        # Display temperature
        temperature_label = tk.Label(self.current_frame, text=f'{round(temperature)}°C', font=(custom_font, 40))
        temperature_label.grid(row=0, column=1, padx=10)

        # Display description
        description_label = tk.Label(self.current_frame, text=description.capitalize(), font=(custom_font, 14))
        description_label.grid(row=1, column=1, padx=10)

        # Display icon
        self.current_icon_label.config(image=icon_image)
        self.current_icon_label.image = icon_image
        self.image_references.append(icon_image)  # Store reference to prevent garbage collection

    def display_upcoming_forecast(self, forecast_list):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Group forecast entries by date and display only one entry per day
        forecast_by_date = {}
        for forecast in forecast_list:
            date_time = datetime.strptime(forecast["date_time"], '%Y-%m-%d %H:%M:%S')
            date_key = date_time.date()

            if date_key not in forecast_by_date:
                forecast_by_date[date_key] = {
                    "temperature": round(forecast["temperature"]),
                    "description": forecast["description"]
                }

        # Insert rows into the Treeview
        for date, entry in forecast_by_date.items():
            temperature = entry["temperature"]
            description = entry["description"]
            formatted_date = date.strftime('%A')  # Format date as '11 Oct'
            self.tree.insert('', 'end', values=(formatted_date, temperature, description))

        # Adjust the height of the Treeview based on the number of rows
        table_height = min(len(forecast_by_date), 10)  # Set a maximum height of 10 rows
        self.tree.configure(height=table_height)

        # Show the Treeview
        self.tree.pack()

    def display_aqi_and_wind_speed(self, aqi, wind_speed):
        self.aqi_wind_label.config(text=f'AQI: {aqi}\nWind Speed: {wind_speed} m/s\n')

        # Show the AQI and wind speed
        self.aqi_wind_label.pack() 
        self.aqi_wind_frame.pack() 

    def hide_forecast_info(self):
        # Hide the Treeview and AQI/wind speed
        self.tree.pack_forget()
        self.aqi_wind_frame.pack_forget()

<img align="center" src="https://github.com/Syndrizzle/weather-app/assets/96112833/1d154dbe-e415-4c43-8072-8d091a972856"></img>

<h1 align="center">Simple Weather App</h1>
<p align="center">This is a weather app I created using python, tkinter and the openweathermap API. This is a university project but it is here, for reference purposes.</p>

## How to run?
This was made and tested with **Python 3.12**.
- Clone the repository:
  ```bash
  git clone https://github.com/syndrizzle/weather-app.git
  cd weather-app
  ```
- Next, install the requirements using pip:
  ```bash
  pip install -r requirements.txt
  ```
- Then run the app:
  ```bash
  python app.py
  ```

## Creating an executable using PyInstaller 
I made this compatible with pyinstaller (It was giving some problems initially), if you don't like running the `app.py` file again and again, you can create a one click executable to launch this.
- First install pyinstaller using pip:
  ```bash
  pip install pyinstaller
  ```
- Use this command when in the project's root directory to create an app:
  ```bash
  pyinstaller --onefile --add-data "path\to\weather-app\fonts;fonts" --add-data "path\to\weather-app\icons;icons" --add-data "path\to\weather-app\ui;ui" --add-data "path\to\weather-app\api.py;." --icon "path\to\weather-app\icons\launcher\icon.png" --add-data "path\to\weather-app\config.json;." --noconsole app.py
  ```
> [!WARNING]<br>
> Replace `path\to` with the actual path of the app, a complete path is necessary for it to work. For eg: `c:\weather-app`

## Credits
- [OpenWeatherMap](https://openweathermap.org)'s awesome [API](https://openweathermap.org/api)
- Icons used in this project are from [Icons8](https://icons8.com)
- Took some help from [ChatGPT](https;//chat.openai.com) (Sorry, I am a beginner programmer 😔)

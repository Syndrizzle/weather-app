from tkinter import ttk
from ttkthemes import ThemedTk
from ui.layout import WeatherUILayout
from ui.events import WeatherUIEvents
from PIL import Image, ImageTk
import os

if __name__ == "__main__":
    root = ThemedTk(theme='breeze')
    root.title('Weather App')

    # Set the icon for the application
    icon_path = os.path.join(os.getcwd(), 'icons', 'launcher', 'icon.png')
    
    # Check if the file exists before trying to set the icon
    if os.path.exists(icon_path):
        # Load the image and set it as the icon
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        root.tk.call('wm', 'iconphoto', root._w, icon_image)

    layout = WeatherUILayout(root)
    events = WeatherUIEvents(root, layout)

    root.mainloop()

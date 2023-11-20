from ttkthemes import ThemedTk
from ui.layout import WeatherUILayout
from ui.events import WeatherUIEvents
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller one-file mode """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = ThemedTk(theme='xpnative')
    root.title('Weather App')

    # Set the icon for the application
    icon_path = resource_path("icons/launcher/icon.png")

    # Check if the file exists before trying to set the icon
    if os.path.exists(icon_path):
        # Load the image and set it as the icon
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        root.tk.call('wm', 'iconphoto', root._w, icon_image)

        root.resizable(False, False)

    layout = WeatherUILayout(root)
    events = WeatherUIEvents(root, layout)

    
    # Force the window to update its size after drawing its content
    root.update_idletasks()

    # Center the window on the screen
    x_position = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
    y_position = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
    root.geometry(f"+{x_position}+{y_position}")

    root.mainloop()

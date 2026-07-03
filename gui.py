import json
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, ttk
from data import load_config, start_sounds, stop_sounds
import threading

image = Image.new('RGB', (64, 64), color=(73, 109, 137))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, 64, 64), fill=(73, 109, 137))

def create_tray_icon():
    """Create the system tray icon."""
    image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(73, 109, 137))
    
    def on_play(icon, item):
        start_sounds()
    
    def on_stop(icon, item):
        stop_sounds()
    
    def on_quit(icon, item):
        stop_sounds()
        icon.stop()
    
    menu = (
        item('Start Sounds', on_play),
        item('Stop Sounds', on_stop),
        pystray.Menu.SEPARATOR,
        item('Quit', on_quit),
    )
    
    icon = pystray.Icon("Random Sound Generator", image, "Random Sound Generator", menu)
    return icon


def create_gui():
    """Create and run the configuration GUI."""
    data = load_config()
    
    def select_folder():
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            print(f"Selected folder: {folder_path}")
            data["path"] = folder_path
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
            path_label.config(text=f"Current path: {folder_path}")
            
    def save_settings():
        try:
            min_interval = int(min_interval_entry.get())
            max_interval = int(max_interval_entry.get())
            if min_interval < 0 or max_interval < 0 or min_interval > max_interval:
                raise ValueError("Invalid interval values.")
            data["min_interval"] = min_interval
            data["max_interval"] = max_interval
            with open("config.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Settings saved successfully.")
        except ValueError as e:
            print(f"Error: {e}")
            
    def show_play_menu():
        start_sounds()
        print("Sounds activated. Minimize to tray to continue.")
    
    root = tk.Tk()
    root.title("Random Sound Generator")
    root.geometry("350x300")
    
    # Title
    title_label = tk.Label(root, text="Random Sound Generator Configuration", font=("Arial", 12, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)
    
    # Current path display
    path_label = tk.Label(root, text=f"Current path: {data['path']}", font=("Arial", 10))
    path_label.grid(row=1, column=0, columnspan=2, pady=5)
    
    # Select folder button
    btn = tk.Button(root, text="Select Sound Folder", command=select_folder, width=20)
    btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Short interval configuration
    min_interval_label = tk.Label(root, text="Min Interval (seconds):")
    min_interval_label.grid(row=3, column=0, sticky="e", padx=5)
    min_interval_entry = tk.Entry(root)
    min_interval_entry.insert(0, str(data["min_interval"]))
    min_interval_entry.grid(row=3, column=1, sticky="w", padx=5)

    # Max interval configuration
    max_interval_label = tk.Label(root, text="Max Interval (seconds):")
    max_interval_label.grid(row=4, column=0, sticky="e", padx=5)
    max_interval_entry = tk.Entry(root)
    max_interval_entry.insert(0, str(data["max_interval"]))
    max_interval_entry.grid(row=4, column=1, sticky="w", padx=5)
    
    # Save button
    save_btn = tk.Button(root, text="Save Settings", command=save_settings, width=20)
    save_btn.grid(row=5, column=0, columnspan=2, pady=5)
    
    # Activate sounds button
    play_btn = tk.Button(root, text="Start Playing Sounds", command=show_play_menu, width=20)
    play_btn.grid(row=6, column=0, columnspan=2, pady=5)
    
    # Close button
    close_btn = tk.Button(root, text="Close", command=root.quit, width=20)
    close_btn.grid(row=7, column=0, columnspan=2, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
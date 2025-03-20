import customtkinter as ctk
import threading
import time
from pynput.keyboard import Controller, Listener, Key
from tkinter import messagebox

# Initialize keyboard controller
keyboard = Controller()
typing_active = False  # Flag to control typing process

# Create main app window
ctk.set_appearance_mode("System")  # Supports "Light", "Dark", or "System"
ctk.set_default_color_theme("dark-blue")  # Notion-like theme

app = ctk.CTk()
app.title("Kalon Auto Typer")  # App name changed
app.geometry("500x400")

# Double-click detection variables
last_shift_time = 0
double_click_time_limit = 0.5  # Time in seconds to consider it a double-click

def show_permission_message():
    """Show a message box on first launch to explain permissions."""
    messagebox.showinfo(
        "Permissions Required",
        """
        To ensure the app works properly, please grant the following permissions:
        1. Full Disk Access
        2. Developer Tools
        3. Input Monitoring
        4. Accessibility
        
        You can grant these by going to:
        System Preferences > Security & Privacy > Privacy
        
        Click OK to continue using the app after granting these permissions.
        """
    )

def type_text():
    """Types the text letter by letter at the chosen speed."""
    global typing_active
    typing_active = True
    text = text_entry.get("1.0", "end").strip()
    speed = speed_var.get()
    
    for char in text:
        if not typing_active:
            break
        keyboard.type(char)
        time.sleep(speed / 1000)  # Convert ms to seconds

def start_typing():
    """Starts typing in a separate thread."""
    if not typing_active:
        threading.Thread(target=type_text, daemon=True).start()

def stop_typing():
    """Stops typing."""
    global typing_active
    typing_active = False

def toggle_theme():
    """Toggles between light and dark mode."""
    current_mode = ctk.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light"
    ctk.set_appearance_mode(new_mode)

def on_key_press(key):
    """Listens for the double-click of the shift key to start or stop typing."""
    global last_shift_time

    # Check if the key pressed is the Shift key
    if key == Key.shift:
        current_time = time.time()
        if current_time - last_shift_time < double_click_time_limit:
            # Double-click detected: Start or stop typing
            if typing_active:
                stop_typing()
            else:
                start_typing()
        last_shift_time = current_time

def show_help():
    """Shows a help message box with usage instructions."""
    messagebox.showinfo(
        "How to Use Kalon Auto Typer",
        """
        1. Type your text in the large text box.
        2. Set the typing speed using the slider (in milliseconds per letter).
        3. To start typing, double-click the Shift key.
        4. To stop typing, double-click the Shift key again.
        5. You can toggle between light and dark modes using the button below.
        """
    )

# UI Elements
title_label = ctk.CTkLabel(app, text="Kalon Auto Typer", font=("Arial", 18, "bold"))  # Updated title
title_label.pack(pady=10)

text_entry = ctk.CTkTextbox(app, height=100, width=450)
text_entry.pack(pady=10)

speed_var = ctk.IntVar(value=100)
speed_label = ctk.CTkLabel(app, text="Typing speed (ms per letter):")
speed_label.pack()
speed_slider = ctk.CTkSlider(app, from_=10, to=1000, variable=speed_var)
speed_slider.pack(pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

start_button = ctk.CTkButton(button_frame, text="Start Typing", command=start_typing)
start_button.grid(row=0, column=0, padx=5)
stop_button = ctk.CTkButton(button_frame, text="Stop Typing", command=stop_typing)
stop_button.grid(row=0, column=1, padx=5)

# Help button (smaller and rounder)
help_button = ctk.CTkButton(button_frame, text="?", width=30, height=30, font=("Arial", 14), command=show_help, fg_color="transparent", border_width=2, border_color="gray")
help_button.grid(row=0, column=2, padx=5)

theme_button = ctk.CTkButton(app, text="Toggle Light/Dark Mode", command=toggle_theme)
theme_button.pack(pady=10)

# Keyboard listener (runs in background)
listener = Listener(on_press=on_key_press)
listener.start()

# Show the permission message on first run
show_permission_message()

# Run the app
app.mainloop()

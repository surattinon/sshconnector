import os
import sys
import platform
import requests
import zipfile
import subprocess
import shutil
import tempfile
import tkinter as tk
from tkinter import ttk, simpledialog
from ttkthemes import ThemedStyle

def install_putty(temp_dir, progress_var, root):
    putty_url = "https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip"
    putty_zip = os.path.join(temp_dir, "putty.zip")
    putty_dir = os.path.join(temp_dir, "putty")

    # Download PuTTY zip file
    response = requests.get(putty_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    current_size = 0

    with open(putty_zip, 'wb') as f:
        for data in response.iter_content(chunk_size=1024):
            current_size += len(data)
            progress_var.set(int((current_size / total_size) * 100))
            f.write(data)

    # Extract PuTTY files
    with zipfile.ZipFile(putty_zip, 'r') as zip_ref:
        zip_ref.extractall(putty_dir)

    os.remove(putty_zip)

    # Move PuTTY files to temp directory
    putty_exe = os.path.join(temp_dir, "putty.exe")
    shutil.move(os.path.join(putty_dir, "putty.exe"), putty_exe)

    # Clean up
    shutil.rmtree(putty_dir)

    # Prompt user for password using a themed dialog box
    password = simpledialog.askstring("Password", "Enter SSH Password:", show='*', parent=root)

    # Close the installation window after password prompt
    root.destroy()

    # Launch PuTTY with font size configuration
    subprocess.run([putty_exe, "-ssh", f"{username}@{host}", "-pw", password, "-P", str(port)])

def install_putty_gui():
    root = tk.Tk()
    root.title("PuTTY Configuration")

    # Center the window on the screen
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    style = ThemedStyle(root)
    style.set_theme("breeze")  # Set the theme to 'breeze'

    # Create a custom title bar
    title_bar = ttk.Frame(root, style="TFrame")
    title_bar.pack(expand=1, fill='x')

    # Create a frame to hold the installation progress bar
    frame = ttk.Frame(root, style="TFrame")
    frame.pack(expand=True, fill='both')

    progress_label = ttk.Label(frame, text="Setting up PuTTY", style="TLabel")
    progress_label.pack(pady=10)

    progress_var = tk.IntVar()
    progress_var.set(0)

    progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100, mode='determinate', style="TProgressbar")
    progress_bar.pack(pady=10)

    root.update_idletasks()  # Force update to show progress bar

    temp_dir = tempfile.mkdtemp()

    # Run the installation in a separate thread to keep the GUI responsive
    root.after(100, lambda: install_putty(temp_dir, progress_var, root))

    root.mainloop()

def main():
    global host, username, password, port
    host = "ddns.ofbas.com"
    username = "lab"
    port = 2207

    install_putty_gui()

if __name__ == "__main__":
    main()


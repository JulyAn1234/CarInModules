import tkinter as tk
from PIL import ImageTk, Image
import re
import requests

def make_request(event=None):
    global entry_text
    number = entry.get()
    entry_text = number  # Save the entry text

    if not number:  # Check if the entry box is empty
        return
    if not number.isdigit() or len(number) != 8:  # Check if the number is not 8 digits or not a number
        show_custom_dialog("Error", "Número de control inválido.", 3000, entry)
        return

    url = f"https://us-central1-carin-66b87.cloudfunctions.net/checkOutStudent?ID={number}"
    response = requests.get(url)
    data = response.text

    message = data
    show_custom_dialog("Response", message, 3000, entry)
    
    restart()

def restart():
    entry.delete(0, tk.END)
    entry.focus_set()  # Set focus back to the entry widget

def show_custom_dialog(title, message, duration, entry_widget):
    global dialog_active
    dialog_active = True

    entry_widget.configure(state=tk.DISABLED)  # Disable the entry widget
    entry_text = entry_widget.get()  # Save the entry text

    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x150")  # Adjust the width of the dialog
    dialog.configure(bg="white")
    dialog.wm_attributes("-topmost", True)
    dialog.resizable(False, False)
    dialog.overrideredirect(True)  # Remove the window manager decorations

    # Position the dialog in the center of the main window
    dialog.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() // 2) - (dialog.winfo_width() // 2)
    y = root.winfo_rooty() + (root.winfo_height() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry("+{}+{}".format(x, y))

    message_label = tk.Label(dialog, text=message, font=("Arial", 18), wraplength=380, justify="center")
    message_label.pack(pady=30)  # Increase the vertical padding

    def on_dialog_close():
        global dialog_active
        dialog_active = False
        dialog.grab_release()  # Release the focus from the dialog window
        dialog.destroy()
        entry_widget.configure(state=tk.NORMAL)  # Enable the entry widget
        entry_widget.delete(0, tk.END)  # Clear the entry text
        entry_widget.focus_set()  # Set focus back to the entry widget

    # Close the dialog automatically after the specified duration
    dialog.after(duration, on_dialog_close)

def close_program(event):
    root.quit()

root = tk.Tk()
root.title("Módulo de sálida del estacionamiento")  # Add the title
root.attributes("-fullscreen", True)
root.geometry("800x600")  # Adjust the size of the main window
root.configure(bg="white")
root.resizable(False, False)
root.overrideredirect(True)

# Background Image
bg_image = Image.open("ITT2.jfif")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(root, text="Módulo de sálida del estacionamiento", bg="white", fg="#333333", font=("Arial", 24, "bold"))  # Adjust the font size and style
title_label.pack(pady=20)  # Adjust the vertical padding

intro_label = tk.Label(root, text="Introduce tu número de control:", bg="white", fg="#333333", font=("Arial", 18))  # Adjust the font size
intro_label.pack(pady=10)  # Add vertical padding

entry = tk.Entry(root, font=("Arial", 24))
entry.pack(pady=10)  # Add vertical padding
entry.focus_set()  # Set focus on the entry widget by default

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

make_request_button = tk.Button(button_frame, text="Presiona Enter para Aceptar", font=("Arial", 18), bg="#4caf50", fg="white", command=make_request)  # Adjust the font size
make_request_button.pack()

# Bind the custom command to the Control+Q key combination to close the program
root.bind("<Control-q>", close_program)

# Bind the Enter key to activate the "Aceptar" button
root.bind("<Return>", make_request)

dialog_active = False

def check_dialog(event):
    global dialog_active
    if dialog_active:
        return "break"

root.bind("<Button-1>", check_dialog)

root.mainloop()

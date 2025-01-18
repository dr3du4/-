import subprocess
import sys
from tkinter import messagebox
import tkinter as tk

class ScriptControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Omega - Record Your Boring Lecture")
        self.root.geometry("400x250")
        self.root.configure(bg="#f9aedc")  # Główne tło (jasny różowy)

        # Nagłówek
        self.header_label = tk.Label(
            root, text="Welcome to Omega!",
            font=("Helvetica", 16, "bold"),
            bg="#f9aedc", fg="#9e70cc"
        )
        self.header_label.pack(pady=10)

        # Sekcja dla emaila
        self.email_frame = tk.Frame(root, bg="#f9aedc")
        self.email_frame.pack(pady=10)

        self.email_label = tk.Label(
            self.email_frame, text="Email:",
            font=("Helvetica", 12), bg="#f9aedc", fg="#9e70cc"
        )
        self.email_label.grid(row=0, column=0, padx=5)

        self.email_entry = tk.Entry(
            self.email_frame, width=25, font=("Helvetica", 12),
            bg="white", fg="#9e70cc"
        )
        self.email_entry.grid(row=0, column=1, padx=5)

        self.save_email_button = tk.Button(
            self.email_frame, text="Save Email",
            command=self.save_email,
            font=("Helvetica", 10),
            bg="#f3ab49", fg="white"
        )
        self.save_email_button.grid(row=0, column=2, padx=5)

        # Sekcja przycisków Start/Stop
        self.button_frame = tk.Frame(root, bg="#f9aedc")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame, text="Start Recording",
            command=self.start_recording,
            font=("Helvetica", 12),
            bg="#f3ab49", fg="white", width=15
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(
            self.button_frame, text="Stop Recording",
            command=self.stop_recording,
            font=("Helvetica", 12),
            bg="#9e70cc", fg="white", width=15
        )
        self.stop_button.grid(row=0, column=1, padx=5)

        # Stopka
        self.footer_label = tk.Label(
            root, text="Powered by Wietowcy",
            font=("Helvetica", 10, "italic"),
            bg="#f9aedc", fg="#9e70cc"
        )
        self.footer_label.pack(side="bottom", pady=10)

        self.process = None
        self.email = None  # Placeholder for the email variable

    def save_email(self):
        self.email = self.email_entry.get()
        if not self.email:
            messagebox.showerror("Error", "Please enter a valid email.")
        else:
            messagebox.showinfo("Info", f"Email saved successfully: {self.email}")
    def start_recording(self):
        if self.process is not None and self.process.poll() is None:
            messagebox.showinfo("Info", "Recording is already running!")
            return

        try:
            # Use the full path to the Python executable
            python_path = sys.executable  # This will use the same Python interpreter as the GUI
            self.process = subprocess.Popen([python_path, "video.py"])
            messagebox.showinfo("Info", "Recording started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def stop_recording(self):
        if self.process is None or self.process.poll() is not None:
            messagebox.showinfo("Info", "Recording is not running!")
            return

        try:
            print("Attempting to terminate the process...")
            self.process.terminate()  # Wysyłanie sygnału SIGTERM
            self.process.wait(timeout=5)  # Czekanie na zakończenie procesu
            self.process = None
            print("Process terminated successfully.")
            messagebox.showinfo("Info", "Recording stopped successfully!")
        except subprocess.TimeoutExpired:
            print("Process did not terminate. Killing it...")
            self.process.kill()  # Wymuszenie zakończenia
            self.process = None
            messagebox.showwarning("Warning", "Recording was forcefully stopped!")
        except Exception as e:
            print(f"Error occurred while stopping the process: {e}")
            messagebox.showerror("Error", f"Failed to stop recording: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptControllerApp(root)
    root.mainloop()

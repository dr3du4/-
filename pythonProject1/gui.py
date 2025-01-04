import subprocess
import sys
from tkinter import messagebox
import tkinter as tk

class ScriptControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Controller")

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white")
        self.stop_button.pack(pady=10)

        self.process = None
    def start_recording(self):
        if self.process is not None and self.process.poll() is None:
            messagebox.showinfo("Info", "Recording is already running!")
            return

        try:
            # Use the full path to the Python executable
            python_path = sys.executable  # This will use the same Python interpreter as the GUI
            self.process = subprocess.Popen([python_path, "core.py"])
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

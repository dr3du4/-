import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import subprocess
import sys
import pyautogui
from speechToText import wav_to_text  # Importowanie funkcji do konwersji audio na tekst


def save_email():
    email = email_entry.get()
    if email:
        messagebox.showinfo("Success", f"Email saved: {email}")
    else:
        messagebox.showwarning("Warning", "Please enter an email!")


def start_recording():
    global recording_process_video, recording_process_audio
    if recording_process_video is not None and recording_process_video.poll() is None:
        messagebox.showinfo("Info", "Recording is already running!")
        return

    try:
        python_path = sys.executable

        # Start video recording
        recording_process_video = subprocess.Popen([python_path, "video.py"])

        # Start audio recording
        recording_process_audio = subprocess.Popen([python_path, "sound.py"])

        messagebox.showinfo("Info", "Recording started successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start recording: {e}")


def stop_recording():
    global recording_process_video, recording_process_audio
    if (recording_process_video is None or recording_process_video.poll() is not None) and \
            (recording_process_audio is None or recording_process_audio.poll() is not None):
        messagebox.showinfo("Info", "Recording is not running!")
        return

    try:
        if recording_process_video is not None:
            recording_process_video.terminate()
            recording_process_video.wait(timeout=5)
            recording_process_video = None

        if recording_process_audio is not None:
            recording_process_audio.terminate()
            recording_process_audio.wait(timeout=5)
            recording_process_audio = None

        messagebox.showinfo("Info", "Recording stopped successfully!")

        # Get the email from the entry field
        user_email = email_entry.get()

        # After stopping the recording, call wav_to_text to process audio
        audio_file_path = "loopback_record.wav"  # Ścieżka do pliku audio
        output_text_file = "output_text.txt"  # Ścieżka do pliku tekstowego, gdzie zapisany zostanie wynik

        # Call the wav_to_text function to process the audio and send email
        wav_to_text(audio_file_path, output_text_file, user_email)

        # Notify user when processing is complete
        messagebox.showinfo("Info", f"Text extraction complete. The result is saved in {output_text_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop recording: {e}")


    except subprocess.TimeoutExpired:
        if recording_process_video is not None:
            recording_process_video.kill()
            recording_process_video = None

        if recording_process_audio is not None:
            recording_process_audio.kill()
            recording_process_audio = None

        messagebox.showwarning("Warning", "Recording was forcefully stopped!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop recording: {e}")
def take_screenshot():
    folder_path = os.path.join(os.getcwd(), 'screenshots')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot = pyautogui.screenshot()

    screenshot_filename = f"screenshot_{current_time}.png"
    screenshot_path = os.path.join(folder_path, screenshot_filename)
    screenshot.save(screenshot_path)

    print(f"Screenshot saved at {screenshot_path}")


root = tk.Tk()
root.title("Passiflora - record your boring meeting")
root.geometry("700x550")
root.configure(bg="#f7f3e9")

recording_process_video = None
recording_process_audio = None

icon = tk.PhotoImage(file="icon.png")
root.iconphoto(True, icon)

title_label = tk.Label(root, text="Welcome to Passiflora!", font=("Helvetica", 22, "bold"), fg="#ff914d", bg="#f7f3e9")
title_label.pack(pady=20)

email_frame = tk.Frame(root, bg="#f7f3e9")
email_frame.pack(pady=10)

email_label = tk.Label(email_frame, text="Email:", font=("Helvetica", 14), fg="#7f8c8d", bg="#f7f3e9")
email_label.grid(row=0, column=0, padx=10)

email_entry = tk.Entry(email_frame, font=("Helvetica", 14), width=30, bg="#ffffff", fg="#000000")
email_entry.grid(row=0, column=1, padx=10)

save_email_button = tk.Button(email_frame, text="Save Email", font=("Helvetica", 12, "bold"), bg="#ff914d", fg="#ffffff", command=save_email)
save_email_button.grid(row=0, column=2, padx=10)

button_frame = tk.Frame(root, bg="#f7f3e9")
button_frame.pack(pady=20)



def create_parallelogram_button(parent, text, color, command, row, padx, pady, width=300, height=80, skew=40):
    button = tk.Canvas(parent, width=width, height=height, bg="#f7f3e9", highlightthickness=0)
    button.grid(row=row, column=0, padx=padx, pady=pady)
    button.create_polygon(
        skew, 0,
        width, 0,
        width - skew, height,
        0, height,
        fill=color, outline=color
    )
    button.create_text(
        width / 2,
        height / 2,
        text=text, fill="white", font=("Helvetica", 14, "bold")
    )
    button.bind("<Button-1>", lambda event: command())
    return button


create_parallelogram_button(button_frame, "Start Recording", "#FA5F55", start_recording, row=0, padx=20, pady=10)
create_parallelogram_button(button_frame, "Stop Recording", "#FA5F55", stop_recording, row=1, padx=20, pady=10)
create_parallelogram_button(button_frame, "Take Screenshot", "#FA5F55", take_screenshot, row=2, padx=20, pady=10)

footer_label = tk.Label(root, text="Powered by Passiflora", font=("Helvetica", 10, "italic"), fg="#7f8c8d", bg="#f7f3e9")
footer_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
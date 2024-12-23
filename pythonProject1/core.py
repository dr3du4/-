import sounddevice as sd
import wave
import threading
import cv2
import numpy as np
import pyautogui
import time

# Parametry nagrywania audio
SAMPLE_RATE = 44100  # Częstotliwość próbkowania
CHANNELS = 2         # Liczba kanałów
AUDIO_OUTPUT_FILENAME = "output_audio.wav"

# Parametry nagrywania wideo
SCREEN_SIZE = (1920, 1080)
VIDEO_OUTPUT_FILENAME = "output_video.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(VIDEO_OUTPUT_FILENAME, fourcc, 20.0, SCREEN_SIZE)

# Flaga nagrywania
recording = True
audio_frames = []

def record_audio():
    global audio_frames, recording

    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_frames.append(indata.copy())

    print("Rozpoczęto nagrywanie dźwięku.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        while recording:
            sd.sleep(100)
    print("Nagrywanie dźwięku zakończone.")

    # Zapis audio do pliku
    with wave.open(AUDIO_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # Rozmiar próbki: 16 bitów = 2 bajty
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(audio_frames))

def record_video():
    global recording

    print("Rozpoczęto nagrywanie obrazu.")
    fps = 20
    prev = 0
    while recording:
        time_elapsed = time.time() - prev
        if time_elapsed > 1.0 / fps:
            prev = time.time()
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        cv2.waitKey(10)
    print("Nagrywanie obrazu zakończone.")
    out.release()

def main():
    global recording

    # Uruchomienie wątków dla dźwięku i obrazu
    audio_thread = threading.Thread(target=record_audio)
    video_thread = threading.Thread(target=record_video)

    audio_thread.start()
    video_thread.start()

    print("Naciśnij Ctrl+C, aby zakończyć nagrywanie.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recording = False

    audio_thread.join()
    video_thread.join()
    print(f"Nagranie zakończone. Pliki: {VIDEO_OUTPUT_FILENAME}, {AUDIO_OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()

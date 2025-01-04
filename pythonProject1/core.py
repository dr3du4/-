import wave
import sounddevice as sd
import threading
import cv2
import numpy as np
import pyautogui
import time

# Parameters for audio recording
SAMPLE_RATE = 44100  # Sampling rate
CHANNELS = 2         # Number of channels
AUDIO_OUTPUT_FILENAME = "output_audio.wav"

# Parameters for video recording
SCREEN_SIZE = (1920, 1080)
VIDEO_OUTPUT_FILENAME = "output_video.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(VIDEO_OUTPUT_FILENAME, fourcc, 20.0, SCREEN_SIZE)

# Flag for recording
recording = True
audio_frames = []

import signal
import sys

def signal_handler(sig, frame):
    global recording
    print("Received termination signal. Stopping recording...")
    recording = False

signal.signal(signal.SIGTERM, signal_handler)

def record_audio():
    global audio_frames, recording

    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_frames.append(indata.copy())

    print("Started recording audio.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        while recording:
            sd.sleep(100)
    print("Audio recording finished.")

    # Save audio to a file
    with wave.open(AUDIO_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # Sample size: 16 bits = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(audio_frames))

def record_video():
    global recording

    print("Started recording video.")
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
    print("Video recording finished.")
    out.release()

def main():
    global recording

    # Start the threads for audio and video recording
    audio_thread = threading.Thread(target=record_audio)
    video_thread = threading.Thread(target=record_video)

    audio_thread.start()
    video_thread.start()

    print("Press Ctrl+C to stop recording.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recording = False

    audio_thread.join()
    video_thread.join()
    print(f"Recording finished. Files: {VIDEO_OUTPUT_FILENAME}, {AUDIO_OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()

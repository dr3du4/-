import wave
import threading
import cv2
import numpy as np
import pyautogui
import time
import signal
import sys

# Parameters for video recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20  # Frames per second
recording = False

def signal_handler(sig, frame):
    """Handle termination signal to stop recording."""
    global recording
    print("Received termination signal. Stopping recording...")
    recording = False

signal.signal(signal.SIGTERM, signal_handler)

def record_video(output_filename):
    """Record the screen and save it to a video file."""
    global recording

    # Get the screen size dynamically
    screen_size = pyautogui.size()
    out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)

    print("Started recording video.")
    prev_time = 0
    while recording:
        current_time = time.time()
        if current_time - prev_time > 1.0 / fps:
            prev_time = current_time
            try:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
            except Exception as e:
                print(f"Error during video recording: {e}")
                break
        cv2.waitKey(1)  # Small delay to allow proper handling
    out.release()
    print("Video recording finished.")
    #cv2.destroyAllWindows()

def main():
    global recording
    recording = True

    output_filename = "output_video.avi"
    video_thread = threading.Thread(target=record_video, args=(output_filename,))

    video_thread.start()

    print("Press Ctrl+C to stop recording.")
    try:
        while recording:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping recording...")
        recording = False

    video_thread.join()
    print(f"Recording finished. File saved as: {output_filename}")

if __name__ == "__main__":
    main()
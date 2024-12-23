import pyaudio

audio = pyaudio.PyAudio()

print("Dostępne urządzenia audio:")
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print(f"ID {i}: {device_info['name']}")
audio.terminate()
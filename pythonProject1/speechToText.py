import os
from pydub import AudioSegment
import math
import speech_recognition as sr

def split_audio(input_audio_path, chunk_length_ms=45000):
    audio = AudioSegment.from_wav(input_audio_path)
    chunks = []
    num_chunks = math.ceil(len(audio) / chunk_length_ms)

    for i in range(num_chunks):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, len(audio))
        chunk = audio[start_ms:end_ms]
        chunk_name = f"temp_chunk_{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)

    return chunks

def process_chunks(chunks):
    text = ""
    r = sr.Recognizer()
    for chunk in chunks:
        with sr.AudioFile(chunk) as source:
            audio = r.record(source)
        try:
            text += r.recognize_google(audio, language="pl-PL") + " "  # Polish language
            text += "\n"
        except sr.UnknownValueError:
            print(f"Could not recognize speech in file: {chunk}")
        except sr.RequestError as e:
            print(f"Could not connect to the speech recognition service: {e}")
    return text

def wav_to_text(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist!")
        return

    chunks = split_audio(input_file)
    text = process_chunks(chunks)

    with open(output_file, "w") as f:
        f.write(text)
    print(f"Text saved in file: {output_file}")

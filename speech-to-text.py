from moviepy.video.io.VideoFileClip import VideoFileClip
import speech_recognition as sr
import os
from pydub import AudioSegment
import math

def split_audio(input_audio_path, chunk_length_ms=45000):
    """
    Dzieli plik audio na mniejsze fragmenty o określonej długości.

    Args:
    input_audio_path: Ścieżka do pliku audio.
    chunk_length_ms: Długość fragmentu w milisekundach (domyślnie 60 sekund).

    Zwraca:
    Listę nazw plików z fragmentami audio.
    """
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
    """
    Przetwarza każdy fragment audio i rozpoznaje mowę na tekst.

    Args:
    chunks: Lista plików audio do przetworzenia.

    Zwraca:
    Łączny tekst z wszystkich fragmentów.
    """
    text = ""
    r = sr.Recognizer()
    for chunk in chunks:
        with sr.AudioFile(chunk) as source:
            audio = r.record(source)
        try:
            text += r.recognize_google(audio, language="pl-PL") + " " #dla polskiego/angielskiego:  language="pl-PL" / language="en-US"
            text += "\n"
        except sr.UnknownValueError:
            print(f"Nie udało się rozpoznać mowy w pliku: {chunk}")
        except sr.RequestError as e:
            print(f"Nie udało się połączyć z serwisem rozpoznawania mowy: {e}")
    return text


def mp4_to_text(input_file, output_file):
    """
    Konwertuje plik MP4 na tekst.

    Args:
    input_file: Ścieżka do pliku MP4.
    output_file: Ścieżka do pliku tekstowego z wynikowym tekstem.
    """
    if not os.path.exists(input_file):
        print(f"Plik {input_file} nie istnieje!")
        return
    
    # Załaduj plik wideo
    clip = VideoFileClip(input_file)
    
    # Wyodrębnij ścieżkę dźwiękową
    clip.audio.write_audiofile("temp.wav")
    
    # Podziel plik audio na mniejsze fragmenty
    chunks = split_audio("temp.wav")
    
    # Procesuj fragmenty
    text = process_chunks(chunks)
    
    # Zapisz wynik do pliku
    with open(output_file, "w") as f:
        f.write(text)


# Przykład użycia
input_file = "C:/sciezka/dp/pliku/video/input_file_pol.mp4"  # Ścieżka do pliku wideo
output_file = "C:/sciezka/do/pliku/wynikowego/wynik.txt"  # Ścieżka do pliku, gdzie zapisany będzie tekst

mp4_to_text(input_file, output_file)

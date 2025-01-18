import os
from pydub import AudioSegment
import math
import speech_recognition as sr


def split_audio(input_audio_path, chunk_length_ms=45000):
    """
    Dzieli plik audio na mniejsze fragmenty o określonej długości.

    Args:
    input_audio_path: Ścieżka do pliku audio.
    chunk_length_ms: Długość fragmentu w milisekundach (domyślnie 45 sekund).

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
            text += r.recognize_google(audio, language="pl-PL") + " "  # Język polski, zmień na "en-US" dla angielskiego
            text += "\n"
        except sr.UnknownValueError:
            print(f"Nie udało się rozpoznać mowy w pliku: {chunk}")
        except sr.RequestError as e:
            print(f"Nie udało się połączyć z serwisem rozpoznawania mowy: {e}")
    return text


def wav_to_text(input_file, output_file):
    """
    Konwertuje plik WAV na tekst.

    Args:
    input_file: Ścieżka do pliku WAV.
    output_file: Ścieżka do pliku tekstowego z wynikowym tekstem.
    """
    if not os.path.exists(input_file):
        print(f"Plik {input_file} nie istnieje!")
        return

    # Podziel plik audio na mniejsze fragmenty
    chunks = split_audio(input_file)

    # Procesuj fragmenty
    text = process_chunks(chunks)

    # Zapisz wynik do pliku
    with open(output_file, "w") as f:
        f.write(text)
    print(f"Tekst zapisano w pliku: {output_file}")


# Przykład użycia
input_file = "C:/sciezka/do/pliku/audio/input_file.wav"  # Ścieżka do pliku WAV
output_file = "C:/sciezka/do/pliku/wynikowego/wynik.txt"  # Ścieżka do pliku wynikowego

wav_to_text(input_file, output_file)

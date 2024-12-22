import moviepy.editor as mp
import speech_recognition as sr

def mp4_to_text(input_file, output_file):
  """
  Konwertuje plik MP4 na tekst.

  Args:
    input_file: Ścieżka do pliku MP4.
    output_file: Ścieżka do pliku tekstowego z wynikowym tekstem.
  """

  # Załaduj plik wideo
  clip = mp.VideoFileClip(input_file)

  # Wyodrębnij ścieżkę dźwiękową
  clip.audio.write_audiofile("temp.wav")

  # Utwórz obiekt rozpoznawania mowy
  r = sr.Recognizer()

  # Otwórz plik audio
  with sr.AudioFile("temp.wav") as source:
    audio = r.record(source)

  # Rozpoznaj mowę
  try:
      text = r.recognize_google(audio)
      print("Rozpoznany tekst:", text)

      # Zapisz tekst do pliku
      with open(output_file, "w") as f:
          f.write(text)
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Przykład użycia
input_file = "twoj_plik.mp4"
output_file = "wynik.txt"
mp4_to_text(input_file, output_file)
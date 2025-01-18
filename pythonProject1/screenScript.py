import pyautogui
import tkinter as tk
from PIL import ImageGrab

def take_screenshot():
    # Pobieramy informacje o oknie aplikacji Tkinter (współrzędne)
    window_x = root.winfo_rootx()  # współrzędna X lewego górnego rogu
    window_y = root.winfo_rooty()  # współrzędna Y lewego górnego rogu
    window_width = root.winfo_width()  # szerokość okna
    window_height = root.winfo_height()  # wysokość okna

    # Robimy zrzut ekranu, wykluczając obszar aplikacji Tkinter
    screenshot = pyautogui.screenshot()

    # Konwertujemy do obrazu z Pillow, by móc manipulować
    screenshot = screenshot.crop((0, 0, window_x, window_y))  # przycinamy w lewo/górę (np. pomijamy aplikację)

    # Zapisz screenshot do pliku
    screenshot.save("screenshot.png")
    print("Zrzut ekranu zapisany jako screenshot.png")

# Tworzymy okno Tkinter
root = tk.Tk()
root.title("Aplikacja Tkinter")
root.geometry("300x200")

# Przycisk wywołujący funkcję
button = tk.Button(root, text="Zrób zrzut ekranu", command=take_screenshot)
button.pack(pady=20)

root.mainloop()
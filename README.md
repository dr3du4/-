# Passiflora - Konfiguracja i Uruchomienie

### Instrukcja krok po kroku

1. **Zainstaluj wymagane pakiety:**
   - Upewnij się, że masz zainstalowanego Python 3.
   - W terminalu wykonaj poniższą komendę, aby zainstalować wszystkie wymagane biblioteki:
     ```bash
     pip install -r requirements.txt
     ```

2. **Skonfiguruj Groq AI API:**
   - Otwórz plik `groqPart.py`.
   - W **linii 7** wstaw swój klucz API Groq AI.

3. **Ustaw adres e-mail nadawcy:**
   - Otwórz plik `speechToText.py`.
   - W **linii 54** podaj swój adres e-mail, który będzie używany do wysyłania wiadomości.

4. **Konfiguracja wysyłania e-maili:**
   - Aby poprawnie wysyłać wiadomości e-mail, wykonaj następujące kroki:
     - Obejrzyj i postępuj zgodnie z instrukcjami w [tym filmie](https://youtu.be/g_j6ILT-X0k?si=Y9TkFyUjWAssfS5u) dotyczącym konfiguracji konta Gmail.
     - Po skonfigurowaniu konta Gmail, zapisz swoje hasło aplikacyjne jako zmienną środowiskową o nazwie: **EMAIL_PASSWORD**.

     Przykład dla systemu Linux/macOS:
     ```bash
     export EMAIL_PASSWORD="TwojeHasłoAplikacyjne"
     ```
     Przykład dla systemu Windows (PowerShell):
     ```powershell
     $Env:EMAIL_PASSWORD = "TwojeHasłoAplikacyjne"
     ```

5. **Uruchom aplikację:**
   - W terminalu wykonaj poniższą komendę, aby uruchomić graficzny interfejs aplikacji:
     ```bash
     python gui.py
     ```

---


import os
from gtts import gTTS
from playsound import playsound

def genereaza_audio(text: str, limba: str, cale_salvare: str) -> bool:
    """
    Preia textul și limba, apoi generează și salvează fișierul MP3.
    Returnează True dacă a reușit, altfel False.
    """
    try:
        tts = gTTS(text=text, lang=limba, slow=False)
        tts.save(cale_salvare)
        return True
    except Exception as e:
        print(f"Eroare la generarea audio: {e}")
        return False

def reda_audio(cale_fisier: str):
    """
    Verifică dacă fișierul MP3 există la calea specificată și îl redă.
    """
    if os.path.exists(cale_fisier):
        try:
            playsound(cale_fisier)
        except Exception as e:
            print(f"Eroare la redarea audio: {e}")
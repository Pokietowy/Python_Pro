import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

punkty = 0
proby = 3
duration = 5  # sekundy nagrania
sample_rate = 44100


words_by_level = {
    "łatwy": ["kot", "pies", "jabłko", "mleko", "słońce"],
    "średni": ["banan", "szkoła", "przyjaciel", "okno", "żółty"],  
    "trudny": ["technologia", "uniwersytet", "informacja", "wymowa", "wyobraźnia"]
}

wyb = input("🔀 Wybierz swój level (Łatwy, Średni, Trudny)").lower()

while True:
    if proby == 0:
        time.sleep(2)
        print("😭 Przegrałeś!")
        break
    elif punkty == 5:
        print("🤩 Zdobyłeś 5 punktów, i wygrałeś tą grę. Brawo!")
        break
    if wyb in words_by_level:
        time.sleep(2)
        x = random.choice(words_by_level[wyb])
        print("➡️ Twoje słowo to:", x)
        time.sleep(2)
    else:
        print("Nie ma takiego poziomu!")

    for i in range(5,0, -1):
        print("➡️ Przygotuj się, za", i,"sek. udzielasz odpowiedź.")
        time.sleep(1)

    print("Mów teraz...")
    recording = sd.rec(
    int(duration * sample_rate), # liczba próbek do nagrania
    samplerate=sample_rate,      # częstotliwość próbek
    channels=1,                  # 1 znaczy mono nagranie
    dtype="int16")               # typ danych dla nagranych próbek
    sd.wait()  # czekanie na zakończenie nagrywania

    wav.write("output.wav", sample_rate, recording)
    print("Nagrywanie zakończone, trwa rozpoznawanie...")
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-EN").lower()
        print("🗣️ Powiedziałeś:", text)
        time.sleep(2)
        translator = Translator()
        translated = translator.translate(x,src="PL", dest="en")
        print("✅ Poprawna odpowiedź to: ", translated.text)
        time.sleep(2)
        if translated.text == text:
            print("✅ Odpowiedziałeś poprawnie! Punkt dla ciebie 😝")
            punkty += 1
            print("‼️ Aktualnie masz", punkty," pkt. , oraz pozostało ci ", proby, " prób.")
            time.sleep(2)
        else:
            print("❌ Udzieliłeś niepoprawnej odpowiedzi.")
            proby -= 1
            time.sleep(2)
            print(proby,"/ 3")
    except sr.UnknownValueError:             # - jeśli Google nie mogło zrozumieć mowy z powodu hałasu lub ciszy
        print("Mowa nie została rozpoznana.")
    except sr.RequestError as e:             # - jeśli nie ma połączenia z Internetem lub API jest niedostępne
        print(f"Błąd usługi: {e}")

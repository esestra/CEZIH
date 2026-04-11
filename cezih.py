import requests
from bs4 import BeautifulSoup
import os

# TVOJI PODACI
TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        r = requests.get(URL, timeout=20)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        kljuc = "Projekt informatizacije procesa propisivanja, odobravanja i isporuke ortopedskih i drugih pomagala - ePomagala"
        
        if kljuc in tekst:
            start = tekst.find(kljuc)
            # Uzimamo komad teksta nakon naslova (cca 400 znakova)
            dio = tekst[start:start+400]
            
            # Traženje datuma primjene
            datum = "Nepoznat"
            if "primjena od" in dio:
                # Izoliramo datum (npr. 19.03.2026.)
                datum = dio.split("primjena od")[1].split("-")[0].strip().split("•")[0].strip()

            izgled_poruke = (
                f"❗❗❗ PROMJENA DETEKTIRANA ❗❗❗\n\n"
                f"📌 NASLOV: ePomagala\n"
                f"📅 ZADNJA IZMJENA (Primjena): {datum}\n"
                f"---------------------------\n"
                f"📂 POPIS DOKUMENATA:\n"
                f"• Šifarnik pomagala (.xlsx)\n"
                f"• Popis pomagala (.txt)\n"
                f"• Indikacije (.txt)\n"
                f"• Nova šifra generička razina (.txt)\n"
                f"• Propisivači (.txt)\n"
                f"• Odobravatelji (.txt)\n"
                f"• Vrste (.txt)\n\n"
                f"🔗 Link: {URL}"
            )

            # Provjera starog stanja
            staro = ""
            if os.path.exists(FILE_NAME):
                with open(FILE_NAME, "r", encoding="utf-8") as f:
                    staro = f.read()

            if datum != staro:
                # Slanje na Telegram
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": izgled_poruke})
                # Spremanje novog stanja u datoteku
                with open(FILE_NAME, "w", encoding="utf-8") as f:
                    f.write(datum)
                print("Promjena poslana na Telegram.")
            else:
                print("Nema promjena (datum je isti).")
        else:
            print("K

import requests
from bs4 import BeautifulSoup
import os

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        r = requests.get(URL, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # Traženje datuma
        datum = "Nepoznat"
        if "19.03.2026" in tekst:
            datum = "19.03.2026."
        elif "primjena od" in tekst:
            start_pos = tekst.find("primjena od")
            datum = tekst[start_pos+12:start_pos+23].strip()

        # Učitavanje povijesti
        povijest = []
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                povijest = [line.strip() for line in f.readlines() if line.strip()]

        # Provjera je li ovo nova izmjena
        zadnja_izmjena = povijest[0] if povijest else ""

        if datum != zadnja_izmjena:
            # NOVA IZMJENA - Šalji veliku poruku s popisom
            izgled_poruke = (
                f"❗❗❗ PROMJENA DETEKTIRANA ❗❗❗\n\n"
                f"📌 NASLOV: ePomagala sustav\n"
                f"📅 NOVI DATUM: {datum}\n"
                f"---------------------------\n"
                f"📂 POPIS DOKUMENATA JE DOSTUPAN NA LINKU\n\n"
                f"🔗 Link: {URL}"
            )
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": izgled_poruke})
            
            # Dodaj novi datum na vrh liste
            povijest.insert(0, datum)
            # Čuvaj samo zadnjih 5 radi preglednosti
            povijest = povijest[:5]
            
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                for d in povijest:
                    f.write(f"{d}\n")
        
        # INFO PORUKA (Zadnja 3 datuma) - Šalje se samo ako pokreneš ručno ili preko linka
        # Ovdje simuliramo "Info" ako skriptu pokreneš s dodatnim parametrom, 
        # ali za GitHub ćemo napraviti da uvijek ispiše povijest u logove.
        print(f"Povijest zadnjih izmjena: {povijest[:3]}")

    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

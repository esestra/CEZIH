import requests
from bs4 import BeautifulSoup
import os

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        # Dohvaćanje stranice
        r = requests.get(URL, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Tražimo tekst
        cijeli_tekst = soup.get_text()
        
        # Pokušaj pronaći datum (tražimo '19.03.2026')
        if "19.03.2026" in cijeli_tekst:
            datum = "19.03.2026."
        elif "primjena od" in cijeli_tekst:
            start_pos = cijeli_tekst.find("primjena od")
            datum = cijeli_tekst[start_pos:start_pos+25].strip()
        else:
            datum = "Datum nije prepoznat, provjeri stranicu ručno."

        izgled_poruke = (
            f"❗❗❗ PROMJENA DETEKTIRANA ❗❗❗\n\n"
            f"📌 NASLOV: ePomagala sustav\n"
            f"📅 TRENUTNO STANJE: {datum}\n"
            f"---------------------------\n"
            f"📂 POPIS DOKUMENATA JE DOSTUPAN NA LINKU\n\n"
            f"🔗 Link: {URL}"
        )

        # Provjera starog stanja
        staro = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                staro = f.read()

        # AKO JE NOVO, ŠALJI PORUKU
        if datum != staro:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": izgled_poruke})
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                f.write(datum)
            print("Poruka poslana!")
        else:
            print("Sve je isto, ne šaljem ništa.")

    except Exception as e:
        # Ako se desi greška, pošalji poruku o grešci da znamo što je
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": f"Greska u skripti: {str(e)}"})

if __name__ == "__main__":
    provjeri()

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
CHAT_ID = "7742294612"
BASE_URL = "http://www.cezih.hr/"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        r = requests.get(URL, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        cijeli_tekst = soup.get_text()
        kljucna_rijec = "ePomagala"
        
        if kljucna_rijec in cijeli_tekst:
            # 1. Pronađi datum
            datum = "Nepoznat"
            if "primjena od" in cijeli_tekst:
                start_pos = cijeli_tekst.find("primjena od")
                datum = cijeli_tekst[start_pos:start_pos+25].replace("-", "").strip()

            # 2. Pronađi pravi link za .xlsx šifarnik
            sifarnik_link = URL # Default ako ne nađe
            for link in soup.find_all('a', href=True):
                if ".xlsx" in link['href']:
                    sifarnik_link = urllib.parse.urljoin(BASE_URL, link['href'])
                    break

            # PORUKA
            is_manual = os.getenv('GITHUB_EVENT_NAME') == "workflow_dispatch"
            ikona = "ℹ️" if is_manual else "❗❗❗"
            naslov = "INFO STANJE" if is_manual else "PROMJENA DETEKTIRANA"

            poruka = (
                f"{ikona} *{naslov}*\n\n"
                f"📝 *Projekt:* ePomagala\n"
                f"📅 *Datum:* {datum}\n\n"
                f"📂 *Dokumenti:* \n"
                f"• [Preuzmi Šifarnik (.xlsx)]({sifarnik_link})\n\n"
                f"🔗 [Otvori CEZIH stranicu]({URL})"
            )

            # Provjera starog stanja
            staro = ""
            if os.path.exists(FILE_NAME):
                with open(FILE_NAME, "r", encoding="utf-8") as f:
                    staro = f.read().strip()

            # Šalji ako je ručno pokrenuto ILI ako je datum novi
            if is_manual or datum != staro:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": poruka, "parse_mode": "Markdown"})
                
                with open(FILE_NAME, "w", encoding="utf-8") as f:
                    f.write(datum)
    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

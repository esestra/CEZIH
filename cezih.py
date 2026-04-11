import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

# Uzimamo token iz Secrets-a koje si maloprije postavio
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        # 1. Učitaj stranicu
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(URL, headers=headers, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # 2. Pronađi datum (tražimo format npr. 19.03.2026.)
        datum_match = re.search(r'(\d{2}\.\d{2}\.\d{4}\.)', tekst)
        datum = datum_match.group(1) if datum_match else "Datum nije pronađen"

        # 3. Pronalaženje linka za Excel (.xlsx)
        sifarnik_link = URL
        for link in soup.find_all('a', href=True):
            if ".xlsx" in link['href'].lower():
                sifarnik_link = urllib.parse.urljoin("http://www.cezih.hr/", link['href'])
                break

        # 4. Provjeri je li kliknuto ručno ili se datum stvarno promijenio
        is_manual = os.getenv('GITHUB_EVENT_NAME') == "workflow_dispatch"
        
        staro_stanje = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                staro_stanje = f.read().strip()

        # Šalji poruku samo ako je ručni klik ili ako je novi datum na vidiku
        if is_manual or datum != staro_stanje:
            # Tvoj link za "Gumb za silu"
            force_link = "https://github.com/esestra/CEZIH/actions/workflows/check.yml"
            
            poruka = (
                f"ℹ️ *INFO STANJE*\n\n"
                f"📝 Projekt: ePomagala\n"
                f"📅 Datum na stranici: *{datum}*\n\n"
                f"📂 Dokumenti: \n"
                f"• [Preuzmi Šifarnik (.xlsx)]({sifarnik_link})\n\n"
                f"🔗 [Otvori CEZIH stranicu]({URL})\n\n"
                f"🚀 *Želiš novu provjeru odmah?*\n"
                f"[KLIKNI OVDJE ZA RUČNI RUN]({force_link})"
            )
            
            url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url_tg, data={"chat_id": CHAT_ID, "text": poruka, "parse_mode": "Markdown"})
            
            # Zapiši ovaj datum kao "viđeno"
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                f.write(datum)
                
    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

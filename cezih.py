import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Dohvaćanje podataka iz GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "7742294612"
BASE_URL = "http://www.cezih.hr/"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        # 1. Dohvaćanje stranice
        r = requests.get(URL, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # 2. Izvlačenje datuma (tražimo 'primjena od')
        datum = "Nije pronađen"
        if "primjena od" in tekst:
            start_pos = tekst.find("primjena od")
            datum = tekst[start_pos:start_pos+25].strip()

        # 3. Pronalaženje pravog linka za .xlsx šifarnik
        sifarnik_link = URL
        for link in soup.find_all('a', href=True):
            if ".xlsx" in link['href']:
                sifarnik_link = urllib.parse.urljoin(BASE_URL, link['href'])
                break

        # 4. Provjera je li pokrenuto ručno (gumb) ili automatski (promjena)
        is_manual = os.getenv('GITHUB_EVENT_NAME') == "workflow_dispatch"
        
        staro_stanje = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                staro_stanje = f.read().strip()

        # Šalji poruku ako je ručni klik ILI ako se datum na stranici promijenio
        if is_manual or datum != staro_stanje:
            # FORMAT KOJI SI TRAŽIO
            poruka = (
                f"ℹ️ INFO STANJE\n\n"
                f"📝 Projekt: ePomagala\n"
                f"📅 Datum: {datum}\n\n"
                f"📂 Dokumenti: \n"
                f"• [Preuzmi Šifarnik (.xlsx)]({sifarnik_link})\n\n"
                f"🔗 [Otvori CEZIH stranicu]({URL})\n\n"
                f"🔄 *Za ručnu provjeru klikni:* [OVDJE](https://github.com/esestra/CEZIH/actions/workflows/check.yml)"
            )
            
            url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url_tg, data={"chat_id": CHAT_ID, "text": poruka, "parse_mode": "Markdown"})
            
            # Spremi novo stanje
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                f.write(datum)
                
    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

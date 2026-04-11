import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

# Podaci iz GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def provjeri():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(URL, headers=headers, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # Izvlačenje datuma
        datum_match = re.search(r'primjena od (\d{2}\.\d{2}\.\d{4}\.)', tekst)
        datum = datum_match.group(0) if datum_match else "Datum nije pronađen"

        # Pronalaženje .xlsx linka
        sifarnik_link = URL
        for link in soup.find_all('a', href=True):
            if ".xlsx" in link['href'].lower():
                sifarnik_link = urllib.parse.urljoin("http://www.cezih.hr/", link['href'])
                break

        # Provjera je li pokrenuto ručno ili je došlo do promjene
        is_manual = os.getenv('GITHUB_EVENT_NAME') == "workflow_dispatch"
        
        staro_stanje = ""
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                staro_stanje = f.read().strip()

        # ŠALJI PORUKU ako je ručni klik ILI ako je datum novi
        if is_manual or datum != staro_stanje:
            force_link = "https://github.com/esestra/CEZIH/actions/workflows/check.yml"
            
            poruka = (
                f"ℹ️ *INFO STANJE*\n\n"
                f"📝 Projekt: ePomagala\n"
                f"📅 Datum: *{datum}*\n\n"
                f"📂 Dokumenti: \n"
                f"• [Preuzmi Šifarnik (.xlsx)]({sifarnik_link})\n\n"
                f"🔗 [Otvori CEZIH stranicu]({URL})\n\n"
                f"🚀 *Želiš ponovnu provjeru?*\n"
                f"[KLIKNI OVDJE ZA GUMB]({force_link})"
            )
            
            url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url_tg, data={"chat_id": CHAT_ID, "text": poruka, "parse_mode": "Markdown"})
            
            # Spremi novo stanje u datoteku
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                f.write(datum)
                
    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Dohvaćanje podataka iz GitHuba (Sigurnost)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "7742294612"
BASE_URL = "http://www.cezih.hr/"
URL = "http://www.cezih.hr/cezih_pzz.html"

def provjeri():
    try:
        r = requests.get(URL, timeout=30)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # 1. Traženje datuma primjene
        datum = "primjena od 19.03.2026."
        if "primjena od" in tekst:
            start_pos = tekst.find("primjena od")
            datum = tekst[start_pos:start_pos+25].strip()

        # 2. Pronalaženje pravog linka za .xlsx šifarnik
        sifarnik_link = URL
        for link in soup.find_all('a', href=True):
            if ".xlsx" in link['href']:
                sifarnik_link = urllib.parse.urljoin(BASE_URL, link['href'])
                break

        # FORMAT KOJI SI TRAŽIO
        poruka = (
            f"ℹ️ INFO STANJE\n\n"
            f"📝 Projekt: ePomagala\n"
            f"📅 Datum: {datum}\n\n"
            f"📂 Dokumenti: \n"
            f"• [Preuzmi Šifarnik (.xlsx)]({sifarnik_link})\n\n"
            f"🔗 [Otvori CEZIH stranicu]({URL})"
        )

        # Slanje poruke
        url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": poruka, "parse_mode": "Markdown"}
        requests.post(url_telegram, data=payload)
        
    except Exception as e:
        print(f"Greska: {e}")

if __name__ == "__main__":
    provjeri()

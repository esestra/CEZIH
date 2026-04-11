import requests
from bs4 import BeautifulSoup
import os
import sys

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
CHAT_ID = "7742294612"
URL = "http://www.cezih.hr/cezih_pzz.html"
FILE_NAME = "zadnje_stanje.txt"

def dohvati_podatke():
    try:
        r = requests.get(URL, timeout=20)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # Pronalaženje datuma
        datum = "Nepoznat"
        if "primjena od" in tekst:
            start_pos = tekst.find("primjena od")
            datum = tekst[start_pos+12:start_pos+23].strip()
        
        return datum
    except:
        return None

def provjeri():
    datum = dohvati_podatke()
    if not datum: return

    # Učitavanje starog stanja
    staro = ""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            staro = f.read().strip()

    # IZGLED INFO PORUKE (Plava ikona + Linkovi)
    info_poruka = (
        f"ℹ️ **STATUS PROVJERE**\n\n"
        f"📅 **Zadnja izmjena na stranici:** {datum}\n"
        f"📌 **Naslov:** ePomagala sustav\n\n"
        f"🔗 **Korisni linkovi:**\n"
        f"• [Šifarnik pomagala (XLSX)](http://www.cezih.hr/sifarnici/epomagala_sifarnik.xlsx)\n"
        f"• [Popis pomagala (TXT)](http://www.cezih.hr/sifarnici/epomagala_popis.txt)\n"
        f"• [PZZ Glavna stranica]({URL})\n\n"
        f"✅ Sustav je uredan."
    )

    # IZGLED PORUKE O PROMJENI (Crveni uskličnici)
    promjena_poruka = (
        f"❗❗❗ **PROMJENA DETEKTIRANA** ❗❗❗\n\n"
        f"Novi datum primjene: **{datum}**\n\n"
        f"Provjeri nove datoteke na: {URL}"
    )

    # LOGIKA:
    # Ako je pokrenuto ručno (klikom na gumb), šalje INFO
    # Ako je pokrenuto automatski, šalje samo ako je PROMJENA
    
    run_type = os.getenv('GITHUB_EVENT_NAME')

    if run_type == "workflow_dispatch": # Ručno pokretanje
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": info_poruka, "parse_mode": "Markdown"})
    
    elif datum != staro: # Automatska promjena
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": promjena_poruka, "parse_mode": "Markdown"})
        
    # Spremi novo stanje
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(datum)

if __name__ == "__main__":
    provjeri()

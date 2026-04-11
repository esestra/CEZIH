import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
URL = "http://www.cezih.hr/cezih_pzz.html"

def dohvati_stanje():
    try:
        r = requests.get(URL, timeout=10)
        r.encoding = 'windows-1250'
        soup = BeautifulSoup(r.text, 'html.parser')
        tekst = soup.get_text()
        
        # Tražimo datum nakon "primjena od"
        if "primjena od" in tekst:
            datum = tekst.split("primjena od")[1][:12].strip()
        else:
            datum = "Datum nije pronađen"
            
        return f"ℹ️ **INFO - ZADNJA IZMJENA**\n\n📅 Datum: {datum}\n📌 Naslov: ePomagala sustav\n\n🔗 Linkovi:\n• [Šifarnik pomagala](http://www.cezih.hr/sifarnici/epomagala_sifarnik.xlsx)\n• [CEZIH PZZ Stranica]({URL})"
    except:
        return "❌ Greška pri dohvaćanju podataka."

def slusaj():
    offset = 0
    print("Bot radi... Čekam tvoju poruku 'info' na Telegramu.")
    while True:
        try:
            # Provjerava ima li novih poruka svakih 2 sekunde
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=5").json()
            for update in r.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                tekst_poruke = msg.get("text", "").lower()
                chat_id = msg.get("chat", {}).get("id")

                if "info" in tekst_poruke:
                    odgovor = dohvati_stanje()
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                  data={"chat_id": chat_id, "text": odgovor, "parse_mode": "Markdown"})
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    slusaj()

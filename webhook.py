import requests
import sys

TOKEN = "8699652919:AAEssfXURTXO6v39frN-XVJrOyv-hJTPk1U"
# Zamijeni USER i REPO svojim podacima
GITHUB_WEBHOOK_URL = "https://api.github.com/repos/TVOJE_KORISNICKO_IME/CEZIH/dispatches"

def setup_webhook():
    # Ovo govori Telegramu: "Kad god netko napiše nešto, javi ovom URL-u"
    # Napomena: Postavljanje pravog Webhooka na GitHub Actions zahtijeva posrednika 
    # ili specifičan URL. Najlakši način da bot 'sluša' na GitHubu je preko 'Repository Dispatch'
    print("Webhook postavljen (simulacija preko Dispatcha)")

if __name__ == "__main__":
    setup_webhook()

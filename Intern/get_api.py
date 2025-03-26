import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

# Recupera la chiave API
api_key = os.getenv("seb_api")

# Verifica che la chiave sia stata caricata correttamente
if not api_key:
    raise ValueError("La chiave API non è stata trovata. Controlla il file .env")

print("Chiave API caricata con successo!")

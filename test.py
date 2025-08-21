import os
import json
import unicodedata

# Percorsi
DIZIONARIO_PATH = "dizionario.json"
AUDIO_FOLDER = "static/audio"

# Normalizzazione
def normalizza_nome(nome):
    return unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode().lower()

# Carica dizionario
with open(DIZIONARIO_PATH, encoding="utf-8") as f:
    dizionario = json.load(f)

# Elenco file audio disponibili
audio_files = {normalizza_nome(os.path.splitext(f)[0]) for f in os.listdir(AUDIO_FOLDER) if f.endswith(".mp3")}

# Controllo
mancanti = []
for parola in dizionario:
    chiave = normalizza_nome(parola)
    if chiave not in audio_files:
        mancanti.append(parola)

# Risultato
if mancanti:
    print("🔇 File audio mancanti per le seguenti parole:")
    for parola in mancanti:
        print(f" - {parola}")
else:
    print("✅ Tutte le parole hanno un file audio associato.")
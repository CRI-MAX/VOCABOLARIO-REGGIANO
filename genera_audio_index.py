import os
import json
import unicodedata

# 📍 Percorso della cartella audio
cartella_audio = "static/audio"

# 🔤 Normalizza stringhe
def normalizza_nome(nome):
    return unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode().lower()

# 📁 Dizionario per la mappatura
audio_index = {}

# 🔍 Scansiona tutte le sottocartelle
for radice, _, files in os.walk(cartella_audio):
    for nome_file in files:
        if nome_file.lower().endswith(".mp3"):
            parola = os.path.splitext(nome_file)[0]
            chiave = normalizza_nome(parola)

            sottocartella = os.path.relpath(radice, cartella_audio)
            percorso_relativo = f"{sottocartella}/{nome_file}" if sottocartella != "." else nome_file

            audio_index[chiave] = percorso_relativo

# 💾 Salva il file JSON
with open("audio_index.json", "w", encoding="utf-8") as f:
    json.dump(audio_index, f, ensure_ascii=False, indent=2)

print("✅ File audio_index.json generato con successo!")
import os
import shutil

# Percorso della cartella originale
cartella_originale = "static/audio"

# Scansiona tutti i file nella cartella
for nome_file in os.listdir(cartella_originale):
    percorso_file = os.path.join(cartella_originale, nome_file)

    # Salta se non è un file .mp3
    if not nome_file.lower().endswith(".mp3"):
        continue

    # Prende la prima lettera alfabetica del nome (ignorando parentesi, spazi, ecc.)
    nome_pulito = nome_file.strip().lstrip(" (").lower()
    prima_lettera = nome_pulito[0]

    # Crea la sottocartella se non esiste
    cartella_destinazione = os.path.join(cartella_originale, prima_lettera)
    os.makedirs(cartella_destinazione, exist_ok=True)

    # Sposta il file nella sottocartella
    nuovo_percorso = os.path.join(cartella_destinazione, nome_file)
    shutil.move(percorso_file, nuovo_percorso)

print("✅ Suddivisione completata!")
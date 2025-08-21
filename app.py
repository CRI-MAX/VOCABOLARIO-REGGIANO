from flask import Flask, render_template, request, redirect, url_for
import json, os, logging
from datetime import date
import unicodedata
def normalizza_nome(nome):
    return unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode().lower()

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

app = Flask(__name__, static_folder='static', template_folder='templates')

# Percorsi file
DIZIONARIO_PATH = "dizionario.json"
FRASI_PATH = "frasi.json"
FRASI_SUGGERITE_PATH = "frasi_suggerite.json"
AUDIO_FOLDER = "static/audio"

# Funzione per creare file vuoto se non esiste
def crea_file_vuoto(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("{}" if "dizionario" in path else "[]")
        logging.info(f"📁 File creato: {path}")

# Funzioni di caricamento e salvataggio
def carica_json(path):
    crea_file_vuoto(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenuto = f.read().strip()
            if contenuto:
                return json.loads(contenuto)
            else:
                logging.warning(f"ℹ️ Il file {path} è vuoto.")
    except json.JSONDecodeError as e:
        logging.error(f"❌ Errore nel parsing di {path}: {e}")
    except Exception as e:
        logging.error(f"❌ Errore generico nel caricamento di {path}: {e}")
    return {} if "dizionario" in path else []

def salva_json(path, dati):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=4)
        logging.info(f"✅ Salvataggio riuscito: {path}")
    except Exception as e:
        logging.error(f"❌ Errore nel salvataggio di {path}: {e}")

# Parola del giorno
def parola_del_giorno():
    dizionario = carica_json(DIZIONARIO_PATH)
    if dizionario:
        chiavi = list(dizionario.keys())
        giorno = date.today().toordinal()
        parola = chiavi[giorno % len(chiavi)]
        info = dizionario[parola]
    else:
        parola = "Nessuna parola"
        info = {"traduzione": "", "spiegazione": "", "audio": ""}
    return parola, info

# Frase del giorno
def frase_del_giorno():
    frasi = carica_json(FRASI_PATH)
    if frasi:
        giorno = date.today().toordinal()
        return frasi[giorno % len(frasi)]
    return "Nessuna frase disponibile"

# Rotte principali
@app.route("/")
def index():
    parola, info = parola_del_giorno()
    frase = frase_del_giorno()
    return render_template("index.html", parola=parola, info=info, frase=frase)

@app.route("/dizionario")
def dizionario():
    dizionario = carica_json(DIZIONARIO_PATH)
    lettera = request.args.get("lettera", "").upper()
    filtrate = {p: d for p, d in dizionario.items() if p.upper().startswith(lettera)} if lettera else dizionario
    return render_template("dizionario.html", dizionario=filtrate, lettera=lettera)

# Proposta nuova parola
@app.route("/proponi", methods=["POST"])
def proponi():
    dialetto = request.form.get("dialetto", "").strip()
    italiano = request.form.get("italiano", "").strip()
    spiegazione = request.form.get("spiegazione", "").strip()

    if dialetto and italiano:
        dizionario = carica_json(DIZIONARIO_PATH)
        chiave = dialetto.lower()
        dizionario[chiave] = {
            "traduzione": italiano,
            "spiegazione": spiegazione,
            "audio": f"{chiave}.mp3",
            "sinonimi": ""
        }
        salva_json(DIZIONARIO_PATH, dizionario)
    else:
        logging.warning("⚠️ Dati incompleti nel form. Nessuna voce aggiunta.")
    return redirect(url_for("index"))

# Frasi suggerite
@app.route("/frasi-suggerite")
def frasi_suggerite():
    suggerite = carica_json(FRASI_SUGGERITE_PATH)
    return render_template("frasi_suggerite.html", frasi=suggerite)

@app.route("/approva-frase", methods=["POST"])
def approva_frase():
    frase = request.form.get("frase", "").strip()
    if frase:
        frasi = carica_json(FRASI_PATH)
        frasi.append(frase)
        salva_json(FRASI_PATH, frasi)

        suggerite = carica_json(FRASI_SUGGERITE_PATH)
        suggerite = [f for f in suggerite if f != frase]
        salva_json(FRASI_SUGGERITE_PATH, suggerite)

        return redirect(url_for("frasi_suggerite"))
    return "Frase non valida", 400

# Avvio server
if __name__ == "__main__":
    app.run(debug=False)  # Imposta a True solo in sviluppo
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, random, os
from datetime import date

app = Flask(__name__)

# Percorsi file
DIZIONARIO_PATH = "dizionario.json"
FRASI_PATH = "frasi.json"
PROPOSTE_PATH = "proposte.json"
FRASI_SUGGERITE_PATH = "frasi_suggerite.json"
AUDIO_FOLDER = "static/audio"

# Funzioni di caricamento e salvataggio
def carica_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                contenuto = f.read().strip()
                if contenuto:
                    return json.loads(contenuto)
                else:
                    print(f"ℹ️ Il file {path} è vuoto.")
        except json.JSONDecodeError as e:
            print(f"❌ Errore nel parsing di {path}: {e}")
        except Exception as e:
            print(f"❌ Errore generico nel caricamento di {path}: {e}")
    else:
        print(f"📁 Il file {path} non esiste. Creazione automatica.")
    return []

def salva_json(path, dati):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=4)
        print(f"✅ File {path} salvato correttamente.")
    except Exception as e:
        print(f"❌ Errore nel salvataggio di {path}: {e}")

# Parola del giorno
def parola_del_giorno():
    dizionario = carica_json(DIZIONARIO_PATH)
    if dizionario:
        parola = random.choice(list(dizionario.keys()))
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
        dizionario[dialetto] = {
            "traduzione": italiano,
            "spiegazione": spiegazione,
            "audio": f"{dialetto}.mp3",
            "sinonimi": ""
        }
        salva_json(DIZIONARIO_PATH, dizionario)
    else:
        print("⚠️ Dati incompleti nel form. Nessuna voce aggiunta.")
    return redirect(url_for("index"))

# Proposta nuova frase
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

if __name__ == "__main__":
    app.run(debug=True)
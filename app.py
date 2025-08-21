from flask import Flask, render_template, request, redirect, url_for
import json, random, os

app = Flask(__name__)

DIZIONARIO_PATH = "dizionario.json"
AUDIO_FOLDER = "static/audio"

def carica_dizionario():
    if os.path.exists(DIZIONARIO_PATH):
        with open(DIZIONARIO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salva_dizionario(dizionario):
    with open(DIZIONARIO_PATH, "w", encoding="utf-8") as f:
        json.dump(dizionario, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    dizionario = carica_dizionario()
    if dizionario:
        parola = random.choice(list(dizionario.keys()))
        info = dizionario[parola]
    else:
        parola = "Nessuna frase"
        info = {"traduzione": "", "spiegazione": "", "audio": ""}
    return render_template("index.html", parola=parola, info=info)

@app.route("/dizionario")
def dizionario():
    dizionario = carica_dizionario()
    lettera = request.args.get("lettera", "").upper()
    filtrate = {p: d for p, d in dizionario.items() if p.upper().startswith(lettera)} if lettera else dizionario
    return render_template("dizionario.html", dizionario=filtrate, lettera=lettera)

@app.route("/proponi", methods=["POST"])
def proponi():
    dialetto = request.form.get("dialetto", "").strip()
    italiano = request.form.get("italiano", "").strip()
    spiegazione = request.form.get("spiegazione", "").strip()

    if dialetto and italiano and spiegazione:
        dizionario = carica_dizionario()
        dizionario[dialetto] = {
            "traduzione": italiano,
            "spiegazione": spiegazione,
            "audio": f"{dialetto}.mp3",
            "sinonimi": ""
        }
        salva_dizionario(dizionario)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
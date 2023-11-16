import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

registrace_data = []

def je_validni_nick(nick): #validace nicku
    return bool(re.match("^[a-zA-Z0-9]{2,20}$", nick))

def zpracuj_formular(formular): #zpracovani formulare
    nick = formular.get('nick') #jmeno
    je_plavec = formular.get('je_plavec') #place
    kanoe_kamarad = formular.get('kanoe_kamarad') #friend

    if je_plavec == '1': #validace zda-li je plavec ci nikoliv. Pokud neni tak ho to nepusti dal a dostane alert
        if je_validni_nick(nick): #kontrola validniho nicku
            if kanoe_kamarad and not je_validni_nick(kanoe_kamarad):
                return jsonify({"message": "Chybný formát přezdívky kanoe kamaráda.", "status": 400}), 400
            else: #zda-li vse projde posle je do db
                registrace_data.append({"nick": nick, "je_plavec": je_plavec, "kanoe_kamarad": kanoe_kamarad})
                return jsonify({"message": "Registrace úspěšná.", "status": 200}), 200
        else:
            return jsonify({"message": "Chybný formát přezdívky.", "status": 400}), 400
    else:
        return jsonify({"message": "Osoba musí být plavec.", "status": 400}), 400

@app.route('/', methods=['GET']) #main page
def index():
    return render_template('index.html', title="Rozsazení v lodích na vodáckém kurzu 2023 SPŠE Ječná", ucastnici=registrace_data), 200

@app.route('/registrace', methods=['GET', 'POST']) #register page
def registrace():
    if request.method == 'POST':
        result = zpracuj_formular(request.form)
        if result[1] == 200:
            return redirect(url_for('index'))
        else:
            return result[0], result[1]
    return render_template('registrace.html'), 200

@app.route('/api/check-nickname/<nick>', methods=['GET']) #nickname validator
def check_nickname(nick):
    for ucastnik in registrace_data:
        if ucastnik['nick'] == nick:
            return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

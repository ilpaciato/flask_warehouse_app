'''Il codice implementa una semplice applicazione Flask per la gestione di un magazzino, 
   con funzioni per aggiungere prodotti, modificare le quantità, e visualizzare le scorte basse, 
   salvando i dati in un file CSV. Sono presenti controlli di validazione e messaggi di feedback per l'utente.
'''

from flask import Flask, render_template, request, redirect, url_for, flash # Importa le funzioni necessarie da Flask
import csv # Importa il modulo csv per gestire i file CSV
import os # Importa il modulo os per gestire i file e le directory
import logging # Importa il modulo logging per la gestione dei log

# Inizializzazione dell'app Flask
app = Flask(__name__) # Imposta il nome dell'applicazione
# Imposta la chiave segreta per le sessioni e i messaggi flash
app.secret_key = 'chiave_segreta_per_flash_messages'  # Necessario per i messaggi flash 

CSV_FILE = 'magazzino.csv'  # Nome del file CSV dove vengono salvati i dati

# Crea il file CSV se non esiste, aggiungendo l'intestazione
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';') # Crea un writer CSV
        # Scrive l'intestazione del file CSV
        writer.writerow(["nome", "categoria", "quantità", "prezzo"])

# Funzione per leggere tutti i prodotti dal magazzino (dal file CSV)
def leggi_magazzino():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file,delimiter=';') # Crea un reader CSV per leggere le righe come dizionari
        # Converte il reader in una lista di dizionari
        return list(reader)

# Funzione per scrivere la lista aggiornata dei prodotti nel file CSV
def scrivi_magazzino(magazzino):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ["nome", "categoria", "quantità", "prezzo"]
        writer = csv.DictWriter(file, fieldnames=fieldnames,delimiter=';') # Crea un writer CSV con le intestazioni
        # Scrive l'intestazione nel file CSV
        writer.writeheader()
        # Scrive tutte le righe del magazzino nel file CSV
        writer.writerows(magazzino)

# Rotta principale: mostra la lista dei prodotti in magazzino
@app.route('/')
def index():
    magazzino = leggi_magazzino()
    return render_template('index.html', magazzino=magazzino) # Renderizza la pagina principale con la lista dei prodotti

# Rotta per aggiungere un nuovo prodotto
@app.route('/aggiungi', methods=['GET', 'POST']) 
def aggiungi():
    if request.method == 'POST': # Se il metodo della richiesta è POST, significa che l'utente sta inviando il form
        # Recupera i dati dal form e rimuove gli spazi vuoti
        nome = request.form['nome'].strip()
        categoria = request.form['categoria'].strip()
        
        # Validazione input: quantità e prezzo devono essere numerici
        try:
            quantita = int(request.form['quantità'])
            prezzo = float(request.form['prezzo'])
        except ValueError:
            flash("Inserire valori numerici validi per quantità e prezzo", "error")
            return redirect(url_for('aggiungi'))
        
        # Quantità e prezzo devono essere maggiori di zero
        if quantita <= 0 or prezzo <= 0:
            flash("Quantità e prezzo devono essere maggiori di zero", "error")
            return redirect(url_for('aggiungi'))
        
        # Tutti i campi devono essere compilati
        if not nome or not categoria:
            flash("Compilare tutti i campi obbligatori", "error")
            return redirect(url_for('aggiungi'))

        # Controlla se il prodotto esiste già (case insensitive)
        magazzino = leggi_magazzino()
        if any(p['nome'].lower() == nome.lower() for p in magazzino):
            flash("Prodotto già esistente", "error")
            return redirect(url_for('aggiungi'))

        # Crea il nuovo prodotto e lo aggiunge al magazzino
        nuovo_prodotto = {
            "nome": nome,
            "categoria": categoria,
            "quantità": quantita,
            "prezzo": prezzo
        }

        magazzino.append(nuovo_prodotto)
        scrivi_magazzino(magazzino)
        flash("Prodotto aggiunto con successo", "success")
        return redirect(url_for('index'))

    # Se GET, mostra il form per aggiungere
    return render_template('aggiungi.html') # Renderizza la pagina per aggiungere un nuovo prodotto

# Rotta per modificare la quantità di un prodotto esistente
@app.route('/modifica/<nome>', methods=['GET', 'POST'])
def modifica(nome):
    magazzino = leggi_magazzino()
    prodotto = next((p for p in magazzino if p['nome'] == nome), None)

    if not prodotto:
        flash("Prodotto non trovato", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            modifica = int(request.form['modifica'])
        except ValueError:
            flash("Inserire un valore numerico valido", "error")
            return redirect(url_for('modifica', nome=nome))
        
        nuova_quantita = int(prodotto['quantità']) + modifica
        
        # La quantità non può diventare negativa
        if nuova_quantita <= 0:
            flash("La quantità non può essere negativa o uguale a 0", "error")
            return redirect(url_for('modifica', nome=nome))
        # Limite massimo di modifica per evitare errori grossolani
        if abs(modifica) > 100:
            flash("Modifica troppo grande (max ±100 unità)", "error")
            return redirect(url_for('modifica', nome=nome))
        
        prodotto['quantità'] = str(nuova_quantita)
        scrivi_magazzino(magazzino)
        flash("Quantità aggiornata con successo", "success")
        return redirect(url_for('index'))

    # Se GET, mostra il form per modificare
    return render_template('modifica.html', prodotto=prodotto)

# Rotta per visualizzare i prodotti con scorte basse (<5)
@app.route('/stato_scorte')
def stato_scorte():
    magazzino = leggi_magazzino()
    scorte_basse = [p for p in magazzino if int(p['quantità']) < 5]
    return render_template('stato_scorte.html', scorte_basse=scorte_basse)
# Rotta per eliminare un prodotto (opzionale, non implementata in questo esempio)
@app.route('/elimina/<nome>', methods=['POST']) 
def elimina(nome):
    try:
        magazzino = leggi_magazzino()
        # Filtra il prodotto da eliminare
        magazzino_aggiornato = [p for p in magazzino if p['nome'] != nome]
        
        if len(magazzino_aggiornato) == len(magazzino):
            flash("Prodotto non trovato", "error")
        else:
            scrivi_magazzino(magazzino_aggiornato)
            flash(f"Prodotto '{nome}' eliminato con successo", "success")
            
    except Exception as e:
        logging.error(f"Errore eliminazione {nome}: {str(e)}")
        flash("Errore durante l'eliminazione", "error")
    return redirect(url_for('index'))


# Avvio dell'app Flask in modalità debug
if __name__ == '__main__':
    app.run(debug=True)



# Per eseguire l'app, assicurati di avere Flask installato e poi lancia il comando:
# python app.py
# Per installare Flask, puoi usare il comando:
# pip install Flask
# Per fermare l'app, premi Ctrl+C nel terminale dove è in esecuzione
# Per accedere all'app, apri un browser e vai su http://localhost:5000
# Per testare le funzionalità, puoi usare strumenti come Postman o semplicemente il browser 
# Per aggiungere prodotti, vai su http://localhost:5000/aggiungi
# Per modificare le quantità, vai su http://localhost:5000/modifica/nome_prodotto
# Per visualizzare le scorte basse, vai su http://localhost:5000/stato_scorte


# Web App per la Gestione di un Magazzino di Elettronica
Questo è un semplice progetto web sviluppato con il framework Flask di Python. Serve come esempio didattico per mostrare i concetti base di Flask, la gestione dei form HTML, la persistenza su file CSV e l'interazione tra diverse pagine web.

## Caratteristiche:
- Gestione prodotti di un magazzino di elettronica :I prodotti inseriti dall'amministratore vengono inseriti in un file locale che rappresenta il magazzino  .
- Accumulo e Salvataggio su CSV: I prodotti inseriti vengono accumulati temporaneamente in memoria e possono essere salvate in un file magazzino.csv su richiesta.

### Prerequisiti


#### Installazione delle Dipendenze
Per installare le librerie Python necessarie per questo progetto (principalmente Flask), apri il tuo terminale o prompt dei comandi e esegui questo comando:


````
pip install Flask
````
##### Struttura del Progetto

Il progetto è organizzato come segue:
````
flask_warehouse_app/
├── app.py           # Il codice principale dell'applicazione
└── static/
    ├── style.css    # File css per gestire lo stile delle pagine HTML
└── templates/       # Cartella per i template HTML
    ├── index.html   # Pagina html principale del magazzino
    ├── modifica.html # Sezione per incrementare o diminuire le scorte
    ├── aggiungi.html # Sezione per aggiungere un prodotto in magazzino
    ├── stato_scorte.html # Sezione per la visualizzazion delle scorte (<5) in magazzino 
    
````

Quando avvierai l'applicazione e salverai i prodotti, verrà creato il seguente file CSV nella cartella principale del progetto:

``
magazzino.csv
``

### Come Avviare l'Applicazione
Segui questi passaggi per avviare l'applicazione web:

##### Naviga nella cartella del progetto:
Apri il terminale o il prompt dei comandi e spostati nella directory flask_magazine_app (o qualunque sia il nome della cartella principale del tuo progetto).

````
cd /percorso/alla/tua/cartella/flask_magazine_app

(Sostituisci /percorso/alla/tua/cartella/ con il percorso effettivo sul tuo computer.)
````
##### Avvia l'applicazione Flask:
Esegui il seguente comando:

````
python app.py
````
##### Accedi all'applicazione:
Dopo aver avviato il server, vedrai un messaggio nel terminale simile a questo:

 * Running on http://127.0.0.1:5000


Apri il tuo browser web preferito (Chrome, Firefox, Edge, Safari, ecc.) e vai all'indirizzo:
http://127.0.0.1:5000

L'applicazione è ora in esecuzione e pronta per l'uso!

### Utilizzo dell'Applicazione

- Gestione dei prodotti di un magazzino di elettronica: inserisci un prodotto, seleziona la categoria, la quantità ed il prezzo. Il risultato apparirà nella stessa pagina.
- Salvataggio dei prodotti: Dopo aver fatto inserito i prodotti quest'ultimi verranno salvati in real-time in un file .cvs in locale. Un pop-up confermerà che l'aggiunta del prodotto sia avvenuta correttamente.
- Eliminazione dei prodotti: Utilizzando l'apposito bottone è possibile eliminare il prodotto selezionato
- Stato scorte prodotti: Utilizzando l'apposito bottone è possibile accedere alla sezione della visualizzazione delle scorte (minori di 5)

### Implementazioni future possibili

- Possibilità di un backup automatico del file .csv
- Collegamento con un database esterno
- Storico delle modifiche
- Autenticazione degli utenti
- Statistiche ed analisi dei prodotti
- Supporto alla ricerca e filtri (con l'aggiunta di una barra di ricerca e filtri per categoria, quantità, prezzo etc.)
- Notifiche automatiche scorte basse

# TestoMaestro

Gestione avanzata di file testuali a larghezza fissa o delimitati, con strumenti di ordinamento, filtraggio e rilevamento duplicati.  
TestoMaestro è pensato per chi ha bisogno di manipolare file di testo complessi in modo semplice, intuitivo e affidabile, con una GUI chiara e moderna.

## Obiettivi del progetto

- Fornire uno strumento **facile da usare** per manipolare file testuali.
- Supportare sia **file a larghezza fissa** che **file delimitati** (es. CSV, TSV, ecc.).
- Permettere **ordinamento multi-criterio** su colonne o intervalli di colonne.
- Applicare **filtri multipli** su valori presenti nelle colonne.
- Gestire **righe duplicate** con opzione per eliminarle o aggiungere un flag identificativo.
- Mostrare **anteprima pre/post** delle trasformazioni.
- Salvare automaticamente i file modificati con estensione fissa `.out.txt`.
- Fornire un **tool utile, stabile e condivisibile**, pronto per GitHub o distribuzione interna.

## Funzionalità principali

### 1. Caricamento file
- Selezione file da percorso locale.
- Supporto per file a larghezza fissa o delimitati.
- Rilevazione automatica delle colonne o configurazione manuale.

### 2. Ordinamento
- Ordinamento su intervalli di colonne multipli.
- Direzione **ascendente o discendente** per ciascun intervallo.
- Multi-criterio: esempio, prima colonne 1–3 ascendente, poi colonne 10–15 discendente.

### 3. Filtri
- Cancellazione righe se le colonne selezionate contengono determinati valori.
- Possibilità di definire **più filtri simultaneamente**.
- Applicazione sequenziale dei filtri con anteprima dei risultati.

### 4. Duplicati
- Identificazione righe duplicate in base a colonne chiave.
- Opzioni:
  - Eliminare tutte le righe duplicate tranne una.
  - Mantenere tutte le righe e aggiungere **flag** identificativo.

### 5. Anteprima
- Visualizzazione delle prime **20 righe** prima e dopo le trasformazioni.
- Parametro facilmente modificabile per mostrare più righe.

### 6. Output
- File salvato automaticamente con estensione `.out.txt`.
- Posizione di salvataggio configurabile nel file di configurazione.

## Architettura del progetto

TestoMaestro/
├── src/ # codice sorgente
│ ├── main.py # punto di ingresso
│ ├── gui.py # gestione GUI
│ ├── processors/ # pipeline di elaborazione
│ ├── parsers/ # parser fixed-width e delimitati
│ └── rules/ # regole di ordinamento, filtri, duplicati
├── examples/ # esempi di file testuali
├── screenshots/ # immagini della GUI
├── README.md # questa documentazione
├── requirements.txt # eventuali dipendenze Python
└── LICENSE # licenza open source

## Considerazioni tecniche

- Python gestisce i file **in memoria**, ottimo per file piccoli e medi (<500 MB).  
- Per file molto grandi (>500 MB) si può adottare strategia **chunk + merge** per ordinamenti e filtri, evitando sovraccarichi di memoria.
- GUI leggera, realizzata con **Tkinter** o in futuro **PyQt**, con layout reattivo per schermi di diverse dimensioni.

## Note future
- Espandere la GUI con **preset di regole salvabili**.
- Aggiungere **nuovi tipi di flag per duplicati**.
- Implementare supporto per **pipeline batch** di più file.
- Possibile versione distribuita come **eseguibile standalone** con PyInstaller.

---

**TestoMaestro** nasce per risolvere esigenze concrete di gestione dei file testuali, con un occhio alla **chiarezza**, alla **usabilità** e alla **presentazione professionale** su GitHub o LinkedIn.

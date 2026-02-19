# TestoMaestro

Gestione avanzata di file testuali a larghezza fissa o delimitati, con strumenti di ordinamento, filtraggio e anteprima.  
TestoMaestro è pensato per chi ha bisogno di manipolare file di testo complessi in modo semplice, intuitivo e affidabile, con una GUI chiara e moderna.

## Obiettivi del progetto

- Fornire uno strumento **facile da usare** per manipolare file testuali.
- Supportare sia **file a larghezza fissa** che **file delimitati** (es. CSV, TSV, ecc.).
- Permettere **ordinamento multi-criterio** su colonne o intervalli di colonne.
- Applicare **filtri multipli** su valori presenti nelle colonne.
- Mostrare **anteprima** delle trasformazioni con evidenziazione dei filtri e ordinamenti.
- Salvare automaticamente i file modificati con nome generato in base al timestamp.
- Fornire un **tool stabile e condivisibile**, pronto per GitHub o distribuzione interna.

## Funzionalità principali

### 1. Caricamento file
- Selezione file da percorso locale.
- Supporto per file a larghezza fissa o delimitati (CSV/TSV).
- Preview delle prime **10 righe** nel widget dedicato.
- Rilevazione automatica delle colonne per CSV (con header) o possibilità di impostare manualmente.
- GUI reattiva con scroll verticale e orizzontale in base al contenuto del box di anteprima.

### 2. Ordinamento
- Ordinamento su intervalli di colonne multipli (solo file a larghezza fissa) o su singole colonne (CSV).
- Direzione **ascendente o discendente** per ciascun intervallo/colonna.
- Multi-criterio: esempio, prima colonne 1–3 ascendente, poi colonne 5 discendente.
- Ordinamento CSV rispetta l’header mantenendolo in prima riga.
- Widget di gestione ordinamenti posizionati a destra rispetto ai filtri per miglior layout.

### 3. Filtri
- Applicazione di filtri multipli su intervalli di colonne (file fisso) o su colonne singole (CSV).
- Evidenzia le colonne filtrate direttamente nell’anteprima.
- Supporta operatori di confronto per file a larghezza fissa (`=`, `!=`, `>`, `<`, `>=`, `<=`, `~`, `!~`).

### 4. Anteprima
- Visualizzazione delle prime **10 righe** prima e dopo le trasformazioni.
- Evidenziazione delle colonne interessate dai filtri e dagli ordinamenti.
- Scroll verticale e orizzontale automatico se necessario.
- La sezione anteprima è **responsive**, si ridimensiona con la finestra.

### 5. Output
- File salvato automaticamente con nome generato secondo pattern:  
  `<nomefile>_TestoMaestro_<timestamp>.<estensione originale>`
- Gestione separata per file CSV e file a larghezza fissa.
- Filtri e ordinamenti applicati in memoria prima della scrittura.

## Architettura del progetto

TestoMaestro/
├── src/ # codice sorgente
│ ├── main.py # punto di ingresso
│ ├── engine.py # motore di elaborazione (filtri, ordinamenti)
│ ├── utils.py # funzioni di supporto
│ ├── gui.py # gestione GUI principale
│ └── pycache/
├── examples/ # esempi di file testuali
├── screenshots/ # immagini della GUI
├── README.md # questa documentazione
├── requirements.txt # eventuali dipendenze Python
└── LICENSE # licenza MIT

## Considerazioni tecniche

- Python gestisce i file **in memoria**, ottimo per file piccoli e medi (<500 MB).  
- GUI leggera, realizzata con **Tkinter**, con layout reattivo per schermi di diverse dimensioni.
- File CSV supporta separatori personalizzabili e header opzionale.
- Il motore interno (`engine.py`) applica filtri e ordinamenti in modo sequenziale, mantenendo consistenza tra anteprima e output.

## Note future / TODO

- Gestione duplicati (flag o eliminazione) per CSV e file fisso.
- Possibilità di salvare **preset di filtri e ordinamenti**.
- Pipeline batch per elaborare **più file in sequenza**.
- Distribuzione come **eseguibile standalone** con PyInstaller.
- Ottimizzazione per file molto grandi (>500 MB) con approccio **chunk + merge**.

---

**TestoMaestro** è pensato per la gestione pratica e professionale di file testuali, con un’interfaccia **chiara**, **moderna** e **responsiva**, pronta per uso personale o distribuzione.  

**Licenza:** MIT (vedi `LICENSE`)  
**Copyright:** (c) 2026 Igor Vesentini
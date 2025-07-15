# 📂 File Organizer – Dispaccio 02

Script Python per organizzare automaticamente i file `.pdf` in base alla loro data di ultima modifica.  
I file vengono copiati da una cartella di input in una struttura `output/anno/mese`.

---

## 🚀 Funzionalità attuali

- Lettura di configurazione da `config.ini`
- Scansione cartella `input` e filtraggio dei soli file `.pdf`
- Estrazione della data di ultima modifica
- Creazione automatica delle cartelle `output/anno/mese`
- Copia dei file nella cartella corrispondente

---

## 🛠️ Requisiti

- Python 3.10+
- [fpdf](https://pypi.org/project/fpdf/) (solo per lo script di generazione PDF)

Installa i pacchetti con:

```bash
pip install fpdf
```

---

## 🔧 Configurazione (`config.ini`)

```ini
[percorsi]
input = input
output = output
```

Assicurati di creare le cartelle `input/` e `output/` o indicare percorsi assoluti.

---

## 🎯 Obiettivi futuri

- [ ] ✏️ Logging su `log.txt` per ogni operazione effettuata
- [ ] 🔢 Rinomina automatica dei file (`documento_001.pdf`, `documento_002.pdf`, ...)
- [ ] ⚠️ Gestione errori e logging avanzato
- [ ] 🧪 Modalità "dry-run" per simulare l'esecuzione
- [ ] 📦 Estensione ad altri tipi di file oltre i `.pdf`

---

## 📁 Struttura del progetto

```
organizza_file/
│
├── main.py              # Script principale
├── crea_pdf_fake.py     # Generatore di PDF di esempio
├── config.ini           # File di configurazione
└── README.md            # Questo file
```

---

## ✅ Esecuzione

```bash
python main.py
```

---

## 📬 Ispirato da: Dispaccio 02 - Organizza i file con Python 🗂️

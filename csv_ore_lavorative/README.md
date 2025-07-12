# DISPACCIO 01 – Calcolo ore lavorative 🕒

Questo script legge un file CSV contenente gli orari di entrata e uscita giornalieri, calcola la durata della giornata lavorativa e scrive il risultato in un nuovo file CSV.

---

## 📁 File coinvolti

- `main.py` → Script principale
- `config.ini` → File di configurazione (percorso file input/output)
- `input/ore.csv` → File di input (con le giornate e gli orari)
- `output/ore_totali.csv` → File generato con il totale ore

---

## 📄 Struttura CSV di input

```csv
giorno,entrata,uscita
2024-07-08,08:30,17:15
2024-07-09,09:00,18:00
```

---

## ✅ Output atteso

```csv
giorno,ore_lavorate
2024-07-08,8h 45min
2024-07-09,9h 0min
```

---

## ▶️ Come eseguirlo

Apri un terminale nella cartella `csv_ore_lavorative/` e lancia:

```bash
python main.py
```

Assicurati che `input/ore.csv` esista e che `config.ini` contenga i percorsi corretti.

---

## ⚙️ Configurazione (`config.ini`)

```ini
[percorsi]
input = input/ore.csv
output = output/ore_totali.csv
```

---

## ✍️ Note finali

Questo è un esercizio didattico per imparare:
- lettura/scrittura file CSV in Python
- uso di `datetime`
- separazione tra codice e configurazione

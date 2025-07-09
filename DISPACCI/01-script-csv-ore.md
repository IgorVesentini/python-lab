# DISPACCIO 01 – Script CSV per calcolo ore lavorative 🕒

## 🎯 Obiettivo
Imparare a leggere un file CSV, elaborare i dati e scrivere un nuovo file di output. In questo esempio, calcolerai il totale delle ore lavorative giornaliere da un file CSV.

## 📘 Concetti chiave
- Lettura e scrittura file (`open`, `csv.reader`, `csv.writer`)
- Manipolazione stringhe e numeri
- Uso di `with` per gestire file

## 🧪 Esercizio
### Dato:
Un file `input/ore.csv` con struttura:

```
giorno,entrata,uscita
2024-07-08,08:30,17:15
2024-07-09,09:00,18:00
```

### Fai:
1. Leggi il file CSV
2. Calcola le ore totali giornaliere (es. 8h 45min)
3. Scrivi un file `output/ore_totali.csv` con:

```
giorno,ore_lavorate
2024-07-08,8.75
2024-07-09,9.0
```

## 🎁 Bonus
- Aggiungi supporto per la pausa pranzo (es. -1h)
- Convertilo in un mini script riutilizzabile
- Esponilo su GitHub con `README.md`

## 📦 Come pubblicarlo su GitHub
- Nome repo: `csv-work-hours`
- Tag: `python`, `csv`, `automation`
- Aggiungi screenshot o esempio nel README
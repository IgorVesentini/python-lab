# DISPACCIO 03 – Organizer immagini per data EXIF 📸

## 🎯 Obiettivo
Imparare a creare script che accettano parametri da terminale per elaborare immagini e organizzarle automaticamente in base alla loro data di scatto.

## 📘 Concetti chiave
- Uso di `argparse`
- Lettura metadati EXIF con `Pillow`
- Gestione file, cartelle e logging
- Modalità `--dry-run` per test sicuri

## 🧪 Esercizio
Crea uno script `ordina_foto.py` che accetta:
- `--input` (cartella con immagini)
- `--output` (cartella di destinazione)
- `--estensione` (default: `.jpg`)
- `--dry-run` (non copia i file, mostra solo cosa farebbe)
- `--verbose` (log su console)
- `--ignore-no-exif` (ignora immagini senza data EXIF)

## 🎁 Bonus
- Supporta `.jpeg`, `.png` ecc.
- Gestione dei nomi duplicati
- Logging su `output/log.txt`
- Stampa riepilogo a fine esecuzione

## 📦 Come pubblicarlo su GitHub
- Nome repo: `photo-organizer-cli`
- Tag: `python`, `argparse`, `cli`, `exif`, `images`
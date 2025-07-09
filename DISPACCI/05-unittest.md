# DISPACCIO 05 – Test automatici con `unittest` ✅

## 🎯 Obiettivo
Imparare a testare le tue funzioni con test automatizzati.

## 📘 Concetti chiave
- `import unittest`
- `assertEqual`, `assertTrue`, ecc.
- Scrivere test per funzioni esistenti

## 🧪 Esercizio
1. Crea un file `tests/test_version_utils.py`
2. Scrivi test per:
    - `parse_version("6.95.1") == (6, 95, 1)`
    - `compare_versions((6, 95, 1), (6, 96, 0)) == -1`
3. Lancia i test con:
```bash
python -m unittest discover tests/
```

## 🎁 Bonus
- Aggiungi test per funzioni di filtro
- Crea workflow GitHub Actions per eseguire i test al push

## 📦 Come pubblicarlo su GitHub
- Crea cartella `tests/`
- Badge "build passing" nel README
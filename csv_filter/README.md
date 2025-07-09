# CSV Version Filter Tool 🛠️

Questo progetto è uno strumento da linea di comando per filtrare un file CSV contenente informazioni su rilasci software.

Permette di selezionare:
- ✅ **Rilasci di tipo MAJOR o MINOR** (basati su intervalli di versioni)
- 🔧 **Rilasci di tipo FIX** (basati su una versione specifica)

---

## 📁 Struttura del progetto

```
.
├── main.py                 # Script principale
├── filter_logic.py         # Logica di filtro per versioni
├── version_utils.py        # Funzioni per il parsing e confronto versioni
├── input/
│   └── input.csv           # File CSV da analizzare
├── output/
│   └── filtered_output.csv # File risultante dopo il filtro
├── LICENSE                 # Licenza MIT
```

---

## ▶️ Come si usa

### 1. Prepara il tuo CSV

Assicurati che il file `input/input.csv` sia formattato così:

```
#;Oggetto;# Fixed on;# Fixed also on;# Major release
12345;Descrizione issue;6.95.1;6.96.1;6.97.0
```

Il separatore può essere `;` o `,`, a tua scelta.

---

### 2. Avvia lo script

```bash
python main.py
```

Ti verrà chiesto:

- Il separatore di campo
- Il tipo di rilascio (1 per MAJOR, 2 per FIX)
- Le versioni di riferimento

---

## 🧩 Esempio

```
👉 Inserisci il separatore di campo (es. , oppure ;): ;
1. Rilascio di tipo MAJOR (o minor)
2. Rilascio di tipo FIX
Scegli il tipo di rilascio [1/2]: 2
🔧 Versione di FIX esatta da rilasciare (es. 6.96.1): 6.95.1
✅ 2 righe trovate e scritte in output/filtered_output.csv
```

---

## 🔧 Da migliorare

- Aggiunta di `argparse` per passare parametri da CLI
- Test automatici (`pytest`)
- Logging
- Packaging come modulo Python installabile

---

## 📜 Requisiti

- Python 3.6+
- Nessuna libreria esterna necessaria

---

## 📄 Licenza

Questo progetto è distribuito con licenza [MIT](./LICENSE).
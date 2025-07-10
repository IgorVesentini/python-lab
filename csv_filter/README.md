# CSV Version Filter Tool 🛠️

Questo progetto è uno strumento per filtrare un file CSV contenente informazioni su rilasci software.

**Disponibile in due modalità:**
- 🖥️ **Interfaccia Grafica** (GUI) - Facile da usare con click e selezione
- 💻 **Linea di Comando** (CLI) - Per uso avanzato e automazione

Permette di selezionare:
- ✅ **Rilasci di tipo MAJOR o MINOR** (basati su intervalli di versioni)
- 🔧 **Rilasci di tipo FIX** (basati su una versione specifica)

---

## 📁 Struttura del progetto

```
.
├── main.py                 # Script CLI (linea di comando)
├── gui.py                  # Interfaccia grafica (GUI)
├── filter_logic.py         # Logica di filtro per versioni
├── version_utils.py        # Funzioni per il parsing e confronto versioni
├── requirements.txt        # Dipendenze Python
├── input/
│   └── input.csv           # File CSV da analizzare
├── output/
│   └── filtered_output.csv # File risultante dopo il filtro
├── LICENSE                 # Licenza MIT
```

---

## ▶️ Come si usa

### 🖥️ Interfaccia Grafica (Raccomandato)

1. **Installa le dipendenze di base:**
   ```bash
   pip install -r requirements.txt
   ```

2. **(Opzionale, solo per Drag & Drop su Windows):**
   Per abilitare il drag & drop dei file CSV nella GUI su Windows, installa anche:
   ```bash
   pip install tkinterdnd2
   ```
   Se non installi questa libreria, la GUI funzionerà comunque ma senza la funzione di drag & drop.

3. **Avvia l'interfaccia grafica:**
   ```bash
   python gui.py
   ```

4. **Usa l'interfaccia:**
   - Da linea di comando lancia lo script: python.exe .\gui.py
   - Clicca "Sfoglia" per selezionare il file CSV di input
   - (Opzionale) Trascina il file CSV nella finestra (se drag & drop abilitato)
   - Scegli il tipo di filtro (Major Release o Fix Release)
   - Inserisci le versioni richieste
   - Clicca "🚀 Esegui Filtro"

### 💻 Linea di Comando

1. **Prepara il tuo CSV**

   Assicurati che il file `input/input.csv` sia formattato così:

   ```
   #;Oggetto;# Fixed on;# Fixed also on;# Major release
   12345;Descrizione issue;6.95.1;6.96.1;6.97.0
   ```

   Il separatore può essere `;` o `,`, a tua scelta.

2. **Avvia lo script CLI:**

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
- **Per GUI:** `chardet` (installato automaticamente con `pip install -r requirements.txt`)
- **Per Drag & Drop su Windows:** `tkinterdnd2` (`pip install tkinterdnd2`)
- **Per CLI:** Nessuna libreria esterna necessaria

---

## 📄 Licenza

Questo progetto è distribuito con licenza [MIT](./LICENSE).

---

## 📋 Colonne richieste per il CSV da Redmine

Per funzionare correttamente, il filtro richiede che il CSV esportato da Redmine abbia **esattamente queste colonne, in questo ordine**:

1. **#** — Numero del ticket
2. **Oggetto** — Titolo o descrizione breve del ticket
3. **# Fixed on** — Versione in cui il ticket è stato risolto
4. **# Fixed also on** — Altre versioni in cui il ticket è stato risolto (separati da virgola o "e")
5. **# Major release** — Versione di rilascio principale

**Esempio di intestazione corretta:**
```
#;Oggetto;# Fixed on;# Fixed also on;# Major release
```

> ⚠️ **Nota:** L’ordine e i nomi delle colonne devono essere esattamente questi. Se esporti da Redmine, seleziona solo queste colonne e assicurati che i nomi coincidano.

---
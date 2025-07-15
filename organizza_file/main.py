import configparser
import os
import shutil
from datetime import datetime

def main():
    # imposta variabili
    input_dir, output_dir = set_variable()
    
    # cicla la cartella di input
    for nome_file in os.listdir(input_dir):
        # filtra e quindi tratta solo i pdf
        if nome_file.lower().endswith(".pdf"):
            # calcola anno e mese di modifica del file
            anno, mese, percorso_file = get_anno_mese_pdf(input_dir, nome_file)
        
            # Crea cartelle anno/mese
            cartella_mese = os.path.join(output_dir, anno, mese)
            os.makedirs(cartella_mese, exist_ok=True)

            # Copia il file
            destinazione = os.path.join(cartella_mese, nome_file)
            shutil.copy2(percorso_file, destinazione)  

            print(f"📄 {nome_file} copiato in {cartella_mese}")     

def get_anno_mese_pdf(input_dir, nome_file):
    # ottieni il percorso completo del file
    percorso_completo = os.path.join(input_dir, nome_file)
    print(percorso_completo)
            
    # ottieni timestamp di ultima modifica (in secondi)
    timestamp = os.path.getmtime(percorso_completo)

    # convertilo in oggetto datetime
    data_modifica = datetime.fromtimestamp(timestamp)
    print(data_modifica)

    # estrai anno e mese
    anno = str(data_modifica.year)
    mese = f"{data_modifica.month:02d}"  # aggiunge lo zero davanti, es. "03"

    return anno, mese, percorso_completo

def set_variable():
    config = configparser.ConfigParser()
    config.read("config.ini")

    try:
        input_dir = config["percorsi"]["input"]
        output_dir = config["percorsi"]["output"]
    except KeyError as e:
        print(f"❌ Errore nel file di configurazione: {e}")
        exit(1)

    return input_dir, output_dir

if __name__ == "__main__":
    main()
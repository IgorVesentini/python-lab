import configparser
import csv
from datetime import datetime
from utils import getCalcoloDifferenza

def main():

    righe_lette = 0
    righe_scritte = 0
    righe_scartate = 0

    input_file, output_file = setVariable()

    with open(input_file, "r", newline="", encoding="utf-8") as file, \
         open(output_file, "w", newline="", encoding="utf-8") as output_file:
        
        writer = csv.writer(output_file)
        writer.writerow(["giorno", "ore_lavorate"]) # scrive la riga di testata

        reader = csv.reader(file)
        
        next(reader)  # salta l’intestazione

        for riga in reader:
            
            righe_lette += 1  # Conta sempre

            giorno, entrata, uscita = getRiga(riga, righe_lette) # attua i controlli e ritorna i dati
            if giorno is None or entrata is None or uscita  is None:
                righe_scartate += 1
                continue  # salta questa riga e passa alla successiva

            # Calcolo differenza entrata e uscita
            ore_formattate = getCalcoloDifferenza(entrata, uscita)
            
            writer.writerow([giorno, ore_formattate])
            righe_scritte += 1

        printTotali(righe_lette, righe_scritte, righe_scartate)

def setVariable():
    config = configparser.ConfigParser()
    config.read("config.ini")

    try:
        input_file = config["percorsi"]["input"]
        output_file = config["percorsi"]["output"]
    except KeyError as e:
        print(f"❌ Errore nel file di configurazione: {e}")
        exit(1)

    return input_file, output_file

def getRiga(riga, righe_lette):

    if len(riga) < 3:
        print(f"⚠️ Riga {righe_lette} troppo corta: {riga}")
        return None, None, None

    giorno = riga[0].strip()
    entrata = riga[1].strip()
    uscita = riga[2].strip()
    print("Riga letta: ", giorno, entrata, uscita)

    try:
        # Controlla che la data sia nel formato corretto
        data = datetime.strptime(giorno, "%Y-%m-%d")
        giorno = data.strftime("%Y-%m-%d")
        entrata = datetime.strptime(entrata, "%H:%M")
        uscita = datetime.strptime(uscita, "%H:%M")
        
        if entrata > uscita:
            print("⚠️ Errore: ora di entrata successiva all’uscita")
            return None, None, None

        return giorno, entrata, uscita
    except ValueError as e:
        print(f"Errore nella riga {righe_lette}")
        print(f"Errore nella riga {riga}: {e}")
        return None, None, None

def printTotali(righe_lette, righe_scritte, righe_scartate):
    print("\n--- REPORT FINALE ---")
    print(f" Righe lette     : {righe_lette}")
    print(f" Righe scritte   : {righe_scritte}")
    print(f" Righe scartate  : {righe_scartate}")
    print("----------------------\n")

if __name__ == "__main__":
    main()
import configparser
import csv
from datetime import datetime

def main():

    config = configparser.ConfigParser()
    config.read("config.ini")

    input_file = config["percorsi"]["input"]
    output_file = config["percorsi"]["output"]

    with open(input_file, "r", newline="", encoding="utf-8") as file, \
         open(output_file, "w", newline="", encoding="utf-8") as output_file:
        
        writer = csv.writer(output_file)
        writer.writerow(["giorno", "ore_lavorate"]) # scrive la riga di testata

        reader = csv.reader(file)
        
        next(reader)  # salta l’intestazione
        for riga in reader:
            giorno = riga[0]
            entrata = riga[1]
            uscita = riga[2]
            print("Riga letta: ", giorno, entrata, uscita)
            ora_entrata = datetime.strptime(entrata, "%H:%M")
            ora_uscita = datetime.strptime(uscita, "%H:%M")
            delta = ora_uscita - ora_entrata

            totale_minuti = int(delta.total_seconds() / 60)
            ore = totale_minuti // 60
            minuti = totale_minuti % 60
            ore_formattate = f"{ore}h {minuti}min"
            print("Riga scritta: ", ore_formattate)
            
            writer.writerow([giorno, ore_formattate])
    

if __name__ == "__main__":
    main()
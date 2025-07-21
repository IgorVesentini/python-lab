import configparser
import os
import shutil
from datetime import datetime
import logging

def setup_logger(output_dir):
    logger_name = os.path.splitext(os.path.basename(__file__))[0]
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_path = os.path.join(output_dir, "log.txt")
        file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Salvo riferimento al file handler per eventuale chiusura manuale
        logger.file_handler = file_handler

    return logger

def main():
    input_dir, output_dir = set_variable()
    logger = setup_logger(output_dir)
    logger.info("📂 Avvio script di organizzazione file PDF")

    try:
        for nome_file in os.listdir(input_dir):
            if nome_file.lower().endswith(".pdf"):
                anno, mese, percorso_file = get_anno_mese_pdf(input_dir, nome_file)

                cartella_mese = os.path.join(output_dir, anno, mese)
                os.makedirs(cartella_mese, exist_ok=True)

                destinazione = os.path.join(cartella_mese, nome_file)
                shutil.copy2(percorso_file, destinazione)

                logger.info(f"✅ {nome_file} copiato in {cartella_mese}")
    except Exception as e:
        logger.exception("❌ Errore durante l'elaborazione dei file PDF")
    finally:
        logger.file_handler.close()
        logger.removeHandler(logger.file_handler)

def get_anno_mese_pdf(input_dir, nome_file):
    percorso_completo = os.path.join(input_dir, nome_file)
    timestamp = os.path.getmtime(percorso_completo)
    data_modifica = datetime.fromtimestamp(timestamp)

    anno = str(data_modifica.year)
    mese = f"{data_modifica.month:02d}"

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
import argparse
from engine import process_file, DEFAULT_MAX_FILE_SIZE_MB

def main():
    parser = argparse.ArgumentParser(
        description="TestoMaestro - Motore di elaborazione file testuali"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Percorso del file di input"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Mostra solo le prime 20 righe"
    )

    parser.add_argument(
        "--max-size",
        type=int,
        default=DEFAULT_MAX_FILE_SIZE_MB,
        help=f"Dimensione massima file in MB (default={DEFAULT_MAX_FILE_SIZE_MB})"
    )

    args = parser.parse_args()

    try:
        result = process_file(
            input_path=args.input,
            preview=args.preview,
            max_size=args.max_size
        )
    except ValueError as e:
        print(f"ERRORE: {e}")
        return

    if args.preview:
        print("=== ANTEPRIMA ===")
        for line in result:
            print(line.rstrip())
    else:
        print(f"File letto correttamente: {len(result)} righe")


if __name__ == "__main__":
    main()

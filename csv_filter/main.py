from filter_logic import filter_major_release, filter_fix_release
from version_utils import parse_version

def main():
    input_file = "input/input.csv"
    output_file = "output/filtered_output.csv"

    print("🔧 Filtro CSV per versione software")
    delimiter = input("👉 Inserisci il separatore di campo (es. , oppure ;): ").strip() or ";"

    print("1. Rilascio di tipo MAJOR (o minor)")
    print("2. Rilascio di tipo FIX")
    choice = input("Scegli il tipo di rilascio [1/2]: ").strip()

    if choice == "1":
        v_from = input("👉 Versione precedente (es. 6.95.0): ").strip()
        v_to = input("🚀 Versione che stai rilasciando (es. 6.97.0): ").strip()

        if parse_version(v_from) and parse_version(v_to):
            try:
                count = filter_major_release(input_file, output_file, v_from, v_to, delimiter)
                print(f"✅ {count} righe trovate e scritte in {output_file}")
            except ValueError as ve:
                print(ve)
        else:
            print("⚠️ Versioni mal formattate.")

    elif choice == "2":
        v_exact = input("🔧 Versione di FIX esatta da rilasciare (es. 6.96.1): ").strip()

        if parse_version(v_exact):
            try:
                count = filter_fix_release(input_file, output_file, v_exact, delimiter)
                print(f"✅ {count} righe trovate e scritte in {output_file}")
            except ValueError as ve:
                print(ve)
        else:
            print("⚠️ Versione non valida.")

    else:
        print("❌ Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()
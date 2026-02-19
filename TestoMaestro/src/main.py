# TestoMaestro
# Diritti d'autore (c) 2026 Igor Vesentini
# Licenza: MIT

import argparse
import re
from engine import (
    process_file,
    sort_csv,
    sort_fixed,
    apply_filters_csv,
    apply_filters_fixed
)
from utils import split_csv_line, DEFAULT_MAX_FILE_SIZE_MB, COLUMN_TYPES, auto_cast

# ---------------------------
# Helper parsing CLI
# ---------------------------

def parse_csv_sort_sets(arg_list):
    sets = []
    for item in arg_list:
        if ':' in item:
            col_str, order = item.split(':')
            ascending = order.lower() == 'asc'
        else:
            col_str = item
            ascending = True
        if '-' in col_str:
            start, end = map(int, col_str.split('-'))
            cols = list(range(start, end+1))
        else:
            cols = [int(col_str)]
        sets.append((cols, ascending))
    return sets

def parse_fixed_sort_sets(arg_list):
    sets = []
    for item in arg_list:
        if ':' in item:
            range_str, order = item.split(':')
            ascending = order.lower() == 'asc'
        else:
            range_str = item
            ascending = True
        start, end = map(int, range_str.split('-'))
        sets.append(((start, end), ascending))
    return sets

def parse_col_types(arg_list):
    for item in arg_list:
        col, typ = item.split("=")
        col = int(col)
        typ = typ.lower()
        if typ == "int":
            COLUMN_TYPES[col] = int
        elif typ == "float":
            COLUMN_TYPES[col] = float
        elif typ == "date":
            COLUMN_TYPES[col] = "date"
        elif typ == "timestamp":
            COLUMN_TYPES[col] = "timestamp"
        else:
            COLUMN_TYPES[col] = str

# ---------------------------
# Parsing filtri CLI
# ---------------------------

def parse_filters(filter_args):
    """
    Converte lista di stringhe CLI in tuple per engine.
    Esempi:
    CSV: 3=IT 5>100
    Fixed: 10-15=ABC
    """
    filters = []
    pattern = r"(\d+(?:-\d+)?)(>=|<=|!=|=|>|<|~|!~|in)(.+)"

    for f in filter_args:
        m = re.match(pattern, f)
        if not m:
            raise ValueError(f"Filtro non valido: {f}")

        target, op, val = m.groups()
        val = auto_cast(val.strip())

        if "-" in target:
            start, end = map(int, target.split("-"))
            filters.append((start, end, op, val))
        else:
            filters.append((int(target), op, val))

    return filters

# ---------------------------
# Funzione di scrittura output
# ---------------------------

def write_output(lines, output_path=None):
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            for line in lines:
                if isinstance(line, list):
                    f.write(",".join([str(col).rstrip() for col in line]) + "\n")
                else:
                    f.write(line.rstrip() + "\n")
    else:
        for line in lines:
            if isinstance(line, list):
                print([str(col).rstrip() for col in line])
            else:
                print(line.rstrip())

# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser(description="TestoMaestro - Motore di elaborazione file testuali")
    
    parser.add_argument("--input", required=True, help="Percorso del file di input")
    parser.add_argument("--file-type", required=True, choices=["csv", "fixed"], help="Tipo file")
    parser.add_argument(
        "--preview", nargs='?', const=20, type=int,
        help="Mostra le prime N righe (default=20 se solo --preview)"
    )
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_FILE_SIZE_MB,
                        help=f"Dimensione massima file in MB (default={DEFAULT_MAX_FILE_SIZE_MB})")
    parser.add_argument("--sort-cols", nargs="+", help="Ordinamento multi-set: es 3-5:desc 8-23:asc (fixed) o 3:desc 5:asc (CSV)")
    parser.add_argument("--col-types", nargs="+", help="Override tipi colonne CSV: es 1=int 3=float 5=date")
    parser.add_argument("--output", type=str, help="Percorso file di output. Se non specificato, stampa a video.")
    parser.add_argument("--has-header", action="store_true", help="Indica che il CSV ha una riga di intestazione")
    parser.add_argument("--filter", nargs="+", help="Filtri da applicare, es. 3=IT 5>100")
    parser.add_argument("--sep", type=str, help="Separatore colonne CSV (obbligatorio se file CSV)")

    args = parser.parse_args()

    # ----------------------------
    # Controllo obbligatorietà condizionata
    # ----------------------------
    if args.file_type == "csv" and not args.has_header:
        parser.error("--has-header è obbligatorio per i file CSV")

    if args.file_type == "csv" and not args.sep:
        parser.error("--sep è obbligatorio per i file CSV")

    if args.col_types:
        parse_col_types(args.col_types)

    try:
        lines = process_file(args.input, preview=args.preview, max_size=args.max_size)
    except ValueError as e:
        print(f"ERRORE: {e}")
        return

    if args.preview:
        n = args.preview
        write_output(lines[:n], output_path=args.output)
        return

    # -------------------- pipeline --------------------
    if args.file_type == "csv":
        rows = [split_csv_line(line, sep=args.sep) for line in lines]
        header = rows[0] if args.has_header else None
        data_rows = rows[1:] if args.has_header else rows

        # --- filtri ---
        if args.filter:
            filters = parse_filters(args.filter)
            data_rows = apply_filters_csv(data_rows, filters)

        # --- ordinamento ---
        if args.sort_cols:
            sort_sets = parse_csv_sort_sets(args.sort_cols)
            sorted_rows = sort_csv(data_rows, sort_sets)
            if header:
                sorted_rows.insert(0, header)
            write_output(sorted_rows, output_path=args.output)
        else:
            write_output(data_rows, output_path=args.output)

    else:  # fixed
        # --- filtri ---
        if args.filter:
            filters = parse_filters(args.filter)
            lines = apply_filters_fixed(lines, filters)

        # --- ordinamento ---
        if args.sort_cols:
            sort_sets = parse_fixed_sort_sets(args.sort_cols)
            sorted_rows = sort_fixed(lines, sort_sets)
            write_output(sorted_rows, output_path=args.output)
        else:
            write_output(lines, output_path=args.output)

if __name__ == "__main__":
    main()

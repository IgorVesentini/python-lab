from typing import List, Tuple
from utils import read_file_lines, preview_lines, cast_value, split_csv_line, DEFAULT_MAX_FILE_SIZE_MB

# ---------------------------
# Funzioni principali del motore
# ---------------------------

def process_file(input_path: str, preview: bool = False, max_size: int = DEFAULT_MAX_FILE_SIZE_MB) -> List[str]:
    """Legge il file e gestisce preview e dimensione massima."""
    lines = read_file_lines(input_path, max_size=max_size)
    if preview:
        return preview_lines(lines)
    return lines

# ---------------------------
# Ordinamento CSV
# ---------------------------

def sort_csv(rows: List[List[str]], sort_sets: List[Tuple[List[int], bool]]) -> List[List[str]]:
    """Ordina CSV con casting smart, multi-colonna asc/desc"""
    def key_func(row):
        key = []
        for cols, ascending in sort_sets:
            for col in cols:
                val = cast_value(row[col-1], col)
                key.append(val if ascending else _invert_value(val))
        return tuple(key)
    return sorted(rows, key=key_func)

# ---------------------------
# Ordinamento fixed
# ---------------------------

def sort_fixed(rows: List[str], sort_sets: List[Tuple[Tuple[int,int], bool]]) -> List[str]:
    """
    Ordina file fixed su sottostringhe.
    sort_sets: lista di tuple ((start_col, end_col), ascending)
    start_col, end_col: 1-based inclusivo
    """
    def key_func(line):
        key = []
        for (start, end), ascending in sort_sets:
            # python slicing 0-based, end non incluso
            substr = line[start-1:end]
            key.append(substr if ascending else _invert_value(substr))
        return tuple(key)
    return sorted(rows, key=key_func)

def _invert_value(val):
    """Inverte valore per descending. Funziona per stringhe, numeri, date."""
    try:
        if isinstance(val, (int, float)):
            return -val
        elif hasattr(val, "timestamp"):
            return -val.timestamp()
        else:  # stringa
            return "".join(chr(255 - ord(c)) for c in str(val))
    except Exception:
        return val

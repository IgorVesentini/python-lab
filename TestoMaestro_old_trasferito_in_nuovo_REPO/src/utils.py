# TestoMaestro
# Diritti d'autore (c) 2026 Igor Vesentini
# Licenza: MIT

import os
from typing import List
from datetime import datetime

PREVIEW_LINES = 20
DEFAULT_MAX_FILE_SIZE_MB = 200  # limite prudente

# Mappa dei tipi colonna (1-based). Viene aggiornata da CLI se l'utente fornisce override.
COLUMN_TYPES = {}

# ---------------------------
# Lettura e preview
# ---------------------------

def read_file_lines(path: str, max_size: int = DEFAULT_MAX_FILE_SIZE_MB) -> List[str]:
    file_size_mb = os.path.getsize(path) / (1024 * 1024)
    if file_size_mb > max_size:
        raise ValueError(
            f"Attenzione: il file è troppo grande ({file_size_mb:.1f} MB). "
            f"Limite massimo consentito: {max_size} MB."
        )
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def preview_lines(lines: List[str], n: int = PREVIEW_LINES) -> List[str]:
    return lines[:n]

# ---------------------------
# Casting smart
# ---------------------------

def cast_value(value, col_idx: int):
    """Cerca di convertire value al tipo definito in COLUMN_TYPES o stringa."""
    typ = COLUMN_TYPES.get(col_idx, None)
    if typ is None:
        # casting dinamico automatico
        return auto_cast(value)
    try:
        if typ == int:
            return int(value)
        elif typ == float:
            return float(value)
        elif typ == "date":
            return datetime.strptime(value, "%Y-%m-%d").date()
        elif typ == "timestamp":
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        else:
            return str(value)
    except Exception:
        return value

def auto_cast(value):
    """Tenta di castare automaticamente a int, float, date, timestamp, altrimenti stringa"""
    v = value.strip()
    if v == "":
        return v
    try:
        return int(v)
    except:
        pass
    try:
        return float(v)
    except:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(v, fmt)
            if fmt.endswith("H:%M:%S"):
                return dt
            else:
                return dt.date()
        except:
            continue
    return v

# ---------------------------
# Split CSV
# ---------------------------

def split_csv_line(line: str, sep: str = ",") -> List[str]:
    return [col.strip() for col in line.rstrip().split(sep)]

# ---------------------------
# Confronti generici per filtri
# ---------------------------

def compare(cell, operator, value):
    """Confronta cell con value usando operator"""
    if operator == "=":
        return cell == value
    if operator == "!=":
        return cell != value
    if operator == ">":
        return cell > value
    if operator == "<":
        return cell < value
    if operator == ">=":
        return cell >= value
    if operator == "<=":
        return cell <= value
    if operator == "~":
        return str(value) in str(cell)
    if operator == "!~":
        return str(value) not in str(cell)
    if operator == "in":
        return cell in value

    raise ValueError(f"Operatore non valido: {operator}")

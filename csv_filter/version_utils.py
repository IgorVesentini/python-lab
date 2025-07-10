import chardet
import re

def parse_version(ver_str):
    """
    Estrae la prima occorrenza valida di una versione nel formato X.Y.Z (es. 6.95.0)
    da una stringa, ignorando prefissi/suffissi come 'v6.95.0' o '_v.6.95.0'.
    Ritorna una tupla di interi (X, Y, Z) oppure None se non trovata.
    """
    if not ver_str:
        return None
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', ver_str)
    if match:
        return tuple(map(int, match.groups()))
    return None

def compare_versions(v1, v2):
    """Compara due versioni tuple: ritorna -1, 0, 1"""
    return (v1 > v2) - (v1 < v2)

def detect_encoding(filepath, sample_size=10000):
    """Tenta di rilevare automaticamente l'encoding del file."""
    with open(filepath, 'rb') as f:
        raw_data = f.read(sample_size)
    result = chardet.detect(raw_data)
    return result['encoding'] or 'utf-8'  # fallback sicuro
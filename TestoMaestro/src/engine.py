import os
from typing import List

PREVIEW_LINES = 20
DEFAULT_MAX_FILE_SIZE_MB = 200  # limite prudente

def read_file_lines(path: str, max_size: int = DEFAULT_MAX_FILE_SIZE_MB) -> List[str]:
    """Legge tutte le righe del file, controllando la dimensione massima."""
    
    file_size_mb = os.path.getsize(path) / (1024 * 1024)  # dimensione in MB
    if file_size_mb > max_size:
        raise ValueError(
            f"Attenzione: il file è troppo grande ({file_size_mb:.1f} MB). "
            f"Limite massimo consentito: {max_size} MB."
        )
    
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def preview_lines(lines: List[str], n: int = PREVIEW_LINES) -> List[str]:
    """Restituisce le prime n righe."""
    return lines[:n]


def process_file(input_path: str, preview: bool = False, max_size: int = DEFAULT_MAX_FILE_SIZE_MB) -> List[str]:
    """
    Punto centrale del motore.
    - legge il file
    - gestisce il limite massimo di dimensione
    """
    lines = read_file_lines(input_path, max_size=max_size)

    if preview:
        return preview_lines(lines)

    return lines

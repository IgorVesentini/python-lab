def parse_version(ver_str):
    try:
        cleaned = ver_str.strip().replace('"', '').replace('\r', '').replace('\n', '')
        return tuple(map(int, cleaned.split(".")))
    except Exception:
        return None

def compare_versions(v1, v2):
    """Compara due versioni tuple: ritorna -1, 0, 1"""
    return (v1 > v2) - (v1 < v2)
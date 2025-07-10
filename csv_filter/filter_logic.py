import csv
from version_utils import parse_version, compare_versions, detect_encoding

EXPECTED_HEADERS = ["#", "Oggetto", "# Fixed on", "# Fixed also on", "# Major release"]

def validate_headers(actual_headers, expected_headers):
    actual_clean = [h.strip() for h in actual_headers]
    expected_clean = [h.strip() for h in expected_headers]
    if actual_clean != expected_clean:
        raise ValueError(f"❌ Header non valido.\nAtteso: {expected_clean}\nTrovato: {actual_clean}")

def clean_cell(value):
    return value.strip().replace('"', '').replace('\r', '').replace('\n', '').strip()

def filter_major_release(input_file, output_file, version_from_str, version_to_str, delimiter):
    version_from = parse_version(version_from_str)
    version_to = parse_version(version_to_str)
    filtered = []

    encoding = detect_encoding(input_file)
    with open(input_file, newline='', encoding=encoding) as infile:
        reader = csv.DictReader(infile, delimiter=delimiter)
        headers_map = {h.strip(): h for h in reader.fieldnames}
        headers = reader.fieldnames
        validate_headers(list(headers_map.keys()), EXPECTED_HEADERS)

        for row in reader:
            major_str = clean_cell(row.get(headers_map["# Major release"], ""))
            rel_ver = parse_version(major_str)
            if rel_ver and compare_versions(version_from, rel_ver) < 0 and compare_versions(rel_ver, version_to) <= 0:
                filtered.append(row)

    with open(output_file, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(filtered)

    return len(filtered)

def filter_fix_release(input_file, output_file, target_version_str, delimiter):
    target_version = parse_version(target_version_str)
    filtered = []

    encoding = detect_encoding(input_file)
    with open(input_file, newline='', encoding=encoding) as infile:
        reader = csv.DictReader(infile, delimiter=delimiter)
        headers_map = {h.strip(): h for h in reader.fieldnames}
        headers = reader.fieldnames
        validate_headers(list(headers_map.keys()), EXPECTED_HEADERS)

        for row in reader:
            fixed_on = clean_cell(row.get(headers_map["# Fixed on"], ""))
            fixed_also = clean_cell(row.get(headers_map["# Fixed also on"], ""))

            matches = False
            if parse_version(fixed_on) == target_version:
                matches = True
            elif fixed_also:
                for part in fixed_also.replace(" e ", ",").split(","):
                    if parse_version(part.strip()) == target_version:
                        matches = True
                        break

            if matches:
                filtered.append(row)

    with open(output_file, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(filtered)

    return len(filtered)
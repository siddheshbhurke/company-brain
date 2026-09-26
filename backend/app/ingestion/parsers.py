from pathlib import Path
import json
import csv


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".json",
    ".csv",
}


def parse_text_file(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def parse_json_file(path: Path) -> str:
    data = json.loads(
        path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    )

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )


def parse_csv_file(path: Path) -> str:
    rows = []

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return json.dumps(
        rows,
        indent=2,
        ensure_ascii=False
    )


def parse_file(path: Path) -> str:

    suffix = path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return parse_text_file(path)

    if suffix == ".json":
        return parse_json_file(path)

    if suffix == ".csv":
        return parse_csv_file(path)

    raise ValueError(
        f"Unsupported file type: {suffix}"
    )

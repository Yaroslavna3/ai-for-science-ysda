from __future__ import annotations

# Навигация по проекту и сжатиям статьи: см. ../INDEX.md и ../memory/L1.md–L3.md.

import csv
import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "measurements.csv"
RESULTS_DIR = ROOT / "results"
PV_TABLE_PATH = RESULTS_DIR / "pv_table.csv"
SUMMARY_PATH = RESULTS_DIR / "summary.json"
SUSPICIOUS_THRESHOLD = 0.10


def load_rows() -> list[dict[str, float]]:
    with DATA_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            {
                "row": index,
                "volume_l": float(row["volume_l"]),
                "pressure_kpa": float(row["pressure_kpa"]),
                "temperature_k": float(row["temperature_k"]),
            }
            for index, row in enumerate(reader, start=1)
        ]


def main() -> None:
    rows = load_rows()
    for row in rows:
        row["pv_kpa_l"] = row["volume_l"] * row["pressure_kpa"]

    median_pv = statistics.median(row["pv_kpa_l"] for row in rows)
    for row in rows:
        row["relative_deviation_from_median"] = row["pv_kpa_l"] / median_pv - 1.0
        row["suspicious"] = abs(row["relative_deviation_from_median"]) > SUSPICIOUS_THRESHOLD

    clean_rows = [row for row in rows if not row["suspicious"]]
    clean_pv = [row["pv_kpa_l"] for row in clean_rows]
    summary = {
        "rows_total": len(rows),
        "median_pv_kpa_l": median_pv,
        "suspicious_threshold": SUSPICIOUS_THRESHOLD,
        "suspicious_rows": [
            {
                "row": row["row"],
                "volume_l": row["volume_l"],
                "pressure_kpa": row["pressure_kpa"],
                "pv_kpa_l": row["pv_kpa_l"],
                "relative_deviation_from_median": row["relative_deviation_from_median"],
            }
            for row in rows
            if row["suspicious"]
        ],
        "clean_rows": len(clean_rows),
        "clean_mean_pv_kpa_l": statistics.mean(clean_pv),
        "clean_relative_stdev": statistics.stdev(clean_pv) / statistics.mean(clean_pv),
        "conclusion": (
            "The data support Boyle-Mariotte's law after excluding one suspicious row; "
            "row 7 likely has a pressure-unit or decimal-place error."
        ),
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    with PV_TABLE_PATH.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "row",
            "volume_l",
            "pressure_kpa",
            "temperature_k",
            "pv_kpa_l",
            "relative_deviation_from_median",
            "suspicious",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with SUMMARY_PATH.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

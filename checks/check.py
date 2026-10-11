"""Independent acceptance check for the week 2 Boyle-law task."""

from __future__ import annotations

import csv
import math
import re
import statistics
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "measurements.csv"
RESULT = ROOT / "results" / "week2_boyle.csv"
SUMMARY = ROOT / "results" / "week2_summary.md"
EXPECTED_COLUMNS = {
    "row",
    "volume_l",
    "pressure_kpa",
    "pv_kpa_l",
    "relative_deviation",
    "is_outlier",
}
FLOAT_ABS_TOL = 1e-4


def read_csv(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader), set(reader.fieldnames or [])


def parse_float(value: str | None, label: str, errors: list[str]) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        errors.append(f"{label}: ожидалось число, получено {value!r}")
        return None


def parse_bool(value: str | None) -> bool | None:
    normalized = (value or "").strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    return None


def contains_close(numbers: list[float], target: float, abs_tol: float) -> bool:
    return any(math.isclose(number, target, rel_tol=1e-4, abs_tol=abs_tol) for number in numbers)


def main() -> int:
    errors: list[str] = []

    if not DATA.is_file():
        print(f"нет исходного файла {DATA.relative_to(ROOT)}")
        return 1
    if not RESULT.is_file():
        print(f"нет файла {RESULT.relative_to(ROOT)}")
        return 1
    if not SUMMARY.is_file():
        print(f"нет файла {SUMMARY.relative_to(ROOT)}")
        return 1

    source_rows, source_columns = read_csv(DATA)
    if not {"volume_l", "pressure_kpa"} <= source_columns:
        print("в исходных данных нет столбцов volume_l и pressure_kpa")
        return 1

    expected: list[dict[str, float | int | bool]] = []
    pvs = [float(row["volume_l"]) * float(row["pressure_kpa"]) for row in source_rows]
    median_pv = statistics.median(pvs)
    for index, (source, pv) in enumerate(zip(source_rows, pvs), start=1):
        deviation = (pv - median_pv) / median_pv
        expected.append(
            {
                "row": index,
                "volume_l": float(source["volume_l"]),
                "pressure_kpa": float(source["pressure_kpa"]),
                "pv_kpa_l": pv,
                "relative_deviation": deviation,
                "is_outlier": abs(deviation) > 0.10,
            }
        )

    result_rows, result_columns = read_csv(RESULT)
    missing_columns = EXPECTED_COLUMNS - result_columns
    if missing_columns:
        errors.append(f"не хватает столбцов: {', '.join(sorted(missing_columns))}")
    if len(result_rows) != len(expected):
        errors.append(f"строк в результате {len(result_rows)}, ожидалось {len(expected)}")

    for index, (got, ref) in enumerate(zip(result_rows, expected), start=1):
        row_number = parse_float(got.get("row"), f"строка результата {index}, row", errors)
        if row_number is not None and row_number != ref["row"]:
            errors.append(f"строка результата {index}: нарушен исходный порядок")

        for column in ("volume_l", "pressure_kpa", "pv_kpa_l", "relative_deviation"):
            value = parse_float(got.get(column), f"строка {index}, {column}", errors)
            if value is not None and not math.isclose(
                value, float(ref[column]), rel_tol=1e-6, abs_tol=FLOAT_ABS_TOL
            ):
                errors.append(
                    f"строка {index}, {column}: {value} вместо {float(ref[column]):.8g}"
                )

        outlier = parse_bool(got.get("is_outlier"))
        if outlier is None:
            errors.append(f"строка {index}, is_outlier: нужно true или false")
        elif outlier != ref["is_outlier"]:
            errors.append(f"строка {index}: неверная отметка выброса")

    clean_pvs = [pv for pv, row in zip(pvs, expected) if not row["is_outlier"]]
    clean_mean = statistics.fmean(clean_pvs)
    relative_scatter = statistics.pstdev(clean_pvs) / clean_mean
    outlier_rows = [int(row["row"]) for row in expected if row["is_outlier"]]

    summary_text = SUMMARY.read_text(encoding="utf-8-sig")
    normalized_summary = summary_text.replace(",", ".")
    numbers = [float(value) for value in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", normalized_summary)]

    required_summary_values = [
        (float(len(source_rows)), 0.0, "число измерений"),
        (median_pv, 0.02, "медиана pV"),
        (clean_mean, 0.02, "среднее pV без выбросов"),
    ]
    for target, tolerance, label in required_summary_values:
        if not contains_close(numbers, target, tolerance):
            errors.append(f"в отчёте не найдено значение: {label} ({target:.4g})")

    for row_number in outlier_rows:
        if not re.search(rf"(?<!\d){row_number}(?!\d)", normalized_summary):
            errors.append(f"в отчёте не указан выброс в строке {row_number}")

    scatter_as_ratio = contains_close(numbers, relative_scatter, 5e-4)
    scatter_as_percent = contains_close(numbers, relative_scatter * 100, 0.05)
    if not (scatter_as_ratio or scatter_as_percent):
        errors.append("в отчёте не найден относительный разброс без выбросов")
    if "бойл" not in normalized_summary.lower():
        errors.append("в отчёте нет вывода о законе Бойля–Мариотта")

    if errors:
        print("НЕ ПРИНЯТО:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "принято: "
        f"{len(expected)} измерений, выбросы {outlier_rows}, "
        f"медиана pV={median_pv:.3f}, разброс без выбросов={relative_scatter:.2%}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

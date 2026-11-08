from __future__ import annotations

import math
import statistics
from collections.abc import Mapping, Sequence
from typing import Any


REQUIRED_FIELDS = {"row", "volume_l", "pressure_kpa", "temperature_k"}


def pv_product(volume_l: float, pressure_kpa: float) -> float:
    if not math.isfinite(volume_l) or not math.isfinite(pressure_kpa):
        raise ValueError("volume and pressure must be finite")
    if volume_l <= 0 or pressure_kpa <= 0:
        raise ValueError("volume and pressure must be positive")
    return volume_l * pressure_kpa


def classify_outliers(pv_values: Sequence[float], threshold: float = 0.10) -> list[bool]:
    """Return flags for values whose relative deviation from the median exceeds threshold."""
    raise NotImplementedError("G5: implement and verify outlier classification")


def validate_rows(rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError("measurements must not be empty")

    temperatures: list[float] = []
    for index, row in enumerate(rows, start=1):
        missing = REQUIRED_FIELDS - set(row)
        if missing:
            raise ValueError(f"row {index}: missing fields {sorted(missing)}")
        if row["row"] != index:
            raise ValueError(f"row numbers must be sequential; expected {index}")
        for field in ("volume_l", "pressure_kpa", "temperature_k"):
            value = row[field]
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"row {index}: {field} must be finite numeric")
            if value <= 0:
                raise ValueError(f"row {index}: {field} must be positive")
        temperatures.append(float(row["temperature_k"]))

    reference = temperatures[0]
    if any(not math.isclose(t, reference, rel_tol=0.0, abs_tol=1e-9) for t in temperatures[1:]):
        raise ValueError("measurements are not isothermal")


def analyze_rows(
    rows: Sequence[Mapping[str, Any]], threshold: float = 0.10
) -> list[dict[str, Any]]:
    validate_rows(rows)
    pvs = [pv_product(float(row["volume_l"]), float(row["pressure_kpa"])) for row in rows]
    flags = classify_outliers(pvs, threshold)
    median_pv = statistics.median(pvs)
    return [
        {
            **dict(row),
            "pv_kpa_l": pv,
            "relative_deviation_from_median": pv / median_pv - 1.0,
            "suspicious": flag,
        }
        for row, pv, flag in zip(rows, pvs, flags, strict=True)
    ]

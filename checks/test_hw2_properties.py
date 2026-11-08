from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analyze_boyle import load_rows
from boyle_core import analyze_rows, classify_outliers, pv_product, validate_rows


FINITE_POSITIVE = st.floats(
    min_value=0.01,
    max_value=1_000_000,
    allow_nan=False,
    allow_infinity=False,
    width=64,
)


@settings(max_examples=100, deadline=None, database=None)
@given(volume=FINITE_POSITIVE, pressure=FINITE_POSITIVE)
def test_pv_is_product(volume: float, pressure: float) -> None:
    assert pv_product(volume, pressure) == pytest.approx(volume * pressure, rel=1e-12)


@settings(max_examples=100, deadline=None, database=None)
@given(volume_l=FINITE_POSITIVE, pressure_kpa=FINITE_POSITIVE)
def test_pv_unit_conversion_invariant(volume_l: float, pressure_kpa: float) -> None:
    value_kpa_l = pv_product(volume_l, pressure_kpa)
    value_pa_m3 = (volume_l / 1000.0) * (pressure_kpa * 1000.0)
    assert value_pa_m3 == pytest.approx(value_kpa_l, rel=1e-12)


@settings(max_examples=100, deadline=None, database=None)
@given(
    pv_constant=FINITE_POSITIVE,
    volume_l=st.floats(min_value=0.1, max_value=1000, allow_nan=False, allow_infinity=False),
    factor=st.floats(min_value=1.01, max_value=10, allow_nan=False, allow_infinity=False),
)
def test_pressure_decreases_with_volume(
    pv_constant: float, volume_l: float, factor: float
) -> None:
    larger_volume = volume_l * factor
    pressure_1 = pv_constant / volume_l
    pressure_2 = pv_constant / larger_volume
    assert pressure_2 < pressure_1
    assert pv_product(volume_l, pressure_1) == pytest.approx(pv_constant, rel=1e-12)
    assert pv_product(larger_volume, pressure_2) == pytest.approx(pv_constant, rel=1e-12)


@settings(max_examples=100, deadline=None, database=None)
@given(pv_constant=st.floats(min_value=1, max_value=10000, allow_nan=False, allow_infinity=False))
def test_ideal_boyle_rows_keep_constant_pv(pv_constant: float) -> None:
    volumes = [0.5, 0.8, 1.0, 2.0, 4.0]
    rows = [
        {
            "row": i,
            "volume_l": volume,
            "pressure_kpa": pv_constant / volume,
            "temperature_k": 293.15,
        }
        for i, volume in enumerate(volumes, start=1)
    ]
    result = analyze_rows(rows, threshold=0.10)
    assert all(not row["suspicious"] for row in result)
    assert all(row["pv_kpa_l"] == pytest.approx(pv_constant, rel=1e-12) for row in result)


@settings(max_examples=100, deadline=None, database=None)
@given(
    values=st.lists(
        st.floats(min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False),
        min_size=3,
        max_size=30,
    ),
    scale=st.floats(min_value=0.1, max_value=10, allow_nan=False, allow_infinity=False),
)
def test_outlier_flags_are_scale_invariant(values: list[float], scale: float) -> None:
    assert classify_outliers(values, 0.10) == classify_outliers(
        [value * scale for value in values], 0.10
    )


def test_values_exactly_on_threshold_are_not_outliers() -> None:
    assert classify_outliers([75.0, 100.0, 125.0], 0.25) == [False, False, False]


def test_source_data_contract_and_week2_flag() -> None:
    rows = load_rows()
    validate_rows(rows)
    assert len(rows) == 12
    result = analyze_rows(rows, threshold=0.10)
    assert [row["row"] for row in result] == list(range(1, 13))
    assert [row["row"] for row in result if row["suspicious"]] == [7]
    assert all(math.isfinite(row["pv_kpa_l"]) for row in result)


def test_analysis_is_deterministic_and_does_not_mutate_input() -> None:
    rows = load_rows()
    before = copy.deepcopy(rows)
    first = analyze_rows(rows)
    second = analyze_rows(rows)
    assert rows == before
    assert first == second


@pytest.mark.parametrize(
    "rows",
    [
        [],
        [{"row": 1, "volume_l": 1.0, "pressure_kpa": 2.0}],
        [{"row": 2, "volume_l": 1.0, "pressure_kpa": 2.0, "temperature_k": 293.15}],
        [{"row": 1, "volume_l": 0.0, "pressure_kpa": 2.0, "temperature_k": 293.15}],
        [{"row": 1, "volume_l": 1.0, "pressure_kpa": float("nan"), "temperature_k": 293.15}],
        [
            {"row": 1, "volume_l": 1.0, "pressure_kpa": 2.0, "temperature_k": 293.15},
            {"row": 2, "volume_l": 2.0, "pressure_kpa": 1.0, "temperature_k": 294.15},
        ],
    ],
)
def test_invalid_measurement_contract_is_rejected(rows: list[dict[str, float]]) -> None:
    with pytest.raises(ValueError):
        validate_rows(rows)

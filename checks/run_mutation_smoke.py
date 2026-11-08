"""Run intentional one-line mutants in disposable project copies and record detection."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "src" / "boyle_core.py"
ANALYZER = ROOT / "src" / "analyze_boyle.py"


def main() -> None:
    core_text = CORE.read_text(encoding="utf-8")
    analyzer_text = ANALYZER.read_text(encoding="utf-8")
    cases = [
        (
            "pV арифметика",
            "src/boyle_core.py",
            "return volume_l * pressure_kpa",
            "return volume_l + pressure_kpa",
            "test_pv_is_product",
        ),
        (
            "перевод единиц",
            "src/boyle_core.py",
            "return volume_l * pressure_kpa",
            "return volume_l * pressure_kpa * 1000",
            "test_pv_unit_conversion_invariant",
        ),
        (
            "постоянство pV при изотермическом изменении объёма",
            "src/boyle_core.py",
            "return volume_l * pressure_kpa",
            "return volume_l * pressure_kpa + 1",
            "test_pressure_decreases_with_volume",
        ),
        (
            "идеальные измерения и классификация",
            "src/boyle_core.py",
            "return [abs(value / median_pv - 1.0) > threshold for value in values]",
            "return [True for _ in values]",
            "test_ideal_boyle_rows_keep_constant_pv",
        ),
        (
            "масштабная инвариантность",
            "src/boyle_core.py",
            "abs(value / median_pv - 1.0) > threshold",
            "abs(value - median_pv) > threshold",
            "test_outlier_flags_are_scale_invariant",
        ),
        (
            "строгость границы порога",
            "src/boyle_core.py",
            "abs(value / median_pv - 1.0) > threshold",
            "abs(value / median_pv - 1.0) >= threshold",
            "test_values_exactly_on_threshold_are_not_outliers",
        ),
        (
            "неизменность входа",
            "src/boyle_core.py",
            "    validate_rows(rows)\n    pvs =",
            '    rows[0]["mutation"] = True\n    validate_rows(rows)\n    pvs =',
            "test_analysis_is_deterministic_and_does_not_mutate_input",
        ),
        (
            "изотермический контракт",
            "src/boyle_core.py",
            "if any(not math.isclose(t, reference, rel_tol=0.0, abs_tol=1e-9) for t in temperatures[1:]):",
            "if False and any(not math.isclose(t, reference, rel_tol=0.0, abs_tol=1e-9) for t in temperatures[1:]):",
            "test_invalid_measurement_contract_is_rejected",
        ),
        (
            "контракт исходного набора",
            "src/analyze_boyle.py",
            "for index, row in enumerate(reader, start=1)",
            "for index, row in enumerate(reader, start=1) if index != 1",
            "test_source_data_contract_and_week2_flag",
        ),
        (
            "целостность CSV по хэшу",
            "data/measurements.csv",
            "1.00,247.036,293.15",
            "1.00,247.037,293.15",
            "test_source_csv_matches_frozen_hash",
        ),
    ]

    outcomes: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="hw2_mutations_") as temp:
        base = Path(temp)
        for number, (name, rel_file, old, new, test_name) in enumerate(cases, start=1):
            project = base / f"mutant_{number}"
            for directory in ("src", "checks", "data"):
                shutil.copytree(ROOT / directory, project / directory)
            target = project / rel_file
            text = target.read_text(encoding="utf-8")
            if old not in text:
                raise RuntimeError(f"mutation target not found: {name}")
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--hypothesis-seed=17",
                f"checks/test_hw2_properties.py::{test_name}",
            ]
            run = subprocess.run(command, cwd=project, text=True, capture_output=True)
            outcomes.append(
                {
                    "mutation": name,
                    "test": test_name,
                    "exit_code": run.returncode,
                    "caught": run.returncode != 0,
                    "tail": (run.stdout + run.stderr)[-1000:],
                }
            )

    output = ROOT / "results" / "hw2" / "mutations.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(outcomes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    boundary_case = next(item for item in outcomes if item["mutation"] == "строгость границы порога")
    (output.parent / "caught_error_before.txt").write_text(
        "Intentional mutant: > changed to >= in classify_outliers\n"
        "Expected: the exact-threshold boundary test fails.\n\n"
        + str(boundary_case["tail"]),
        encoding="utf-8",
    )
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "checks/test_hw2_properties.py::test_values_exactly_on_threshold_are_not_outliers",
    ]
    clean = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (output.parent / "caught_error_after.txt").write_text(
        "Correct implementation; same boundary test.\n\n" + clean.stdout + clean.stderr,
        encoding="utf-8",
    )
    for item in outcomes:
        print(f"{'CAUGHT' if item['caught'] else 'MISSED'}: {item['mutation']} -> {item['test']} (exit {item['exit_code']})")
    print(f"Подробный вывод: {output.relative_to(ROOT)}")
    if not all(item["caught"] for item in outcomes) or clean.returncode != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

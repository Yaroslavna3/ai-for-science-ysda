"""Reproducible threshold sensitivity and descriptive bootstrap summary."""
from __future__ import annotations

import json
import hashlib
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analyze_boyle import load_rows
from boyle_core import analyze_rows, classify_outliers


SEEDS = (17, 29, 41)
THRESHOLDS = (0.08, 0.10, 0.12)
BOOTSTRAP_REPLICATES = 2_000


def interval(values: list[float]) -> list[float]:
    ordered = sorted(values)
    return [ordered[int(0.025 * len(ordered))], ordered[int(0.975 * len(ordered))]]


def bootstrap_summary(values: list[float], seed: int) -> tuple[list[float], list[list[int]]]:
    rng = random.Random(seed)
    n = len(values)
    samples = [rng.choices(range(n), k=n) for _ in range(BOOTSTRAP_REPLICATES)]
    means = [statistics.mean(values[index] for index in indices) for indices in samples]
    return means, samples


def main() -> None:
    rows = load_rows()
    data_path = ROOT / "data" / "measurements.csv"
    source_hash = hashlib.sha256(data_path.read_bytes()).hexdigest().upper()
    expected_hash = "93E92BF03CD81AE09F8D86E603C19E414C9CFAD6FD17CDCA8C95B3FB031AFF74"
    if source_hash != expected_hash:
        raise SystemExit(f"source CSV hash changed: {source_hash}")
    pvs = [row["volume_l"] * row["pressure_kpa"] for row in rows]
    sweep = []
    for threshold in THRESHOLDS:
        result = analyze_rows(rows, threshold)
        clean = [row["pv_kpa_l"] for row in result if not row["suspicious"]]
        sweep.append(
            {
                "threshold": threshold,
                "suspicious_rows": [row["row"] for row in result if row["suspicious"]],
                "clean_n": len(clean),
                "clean_mean_pv_kpa_l": statistics.mean(clean),
                "clean_cv": statistics.stdev(clean) / statistics.mean(clean),
            }
        )

    bootstraps = []
    clean_pvs = [value for value, row in zip(pvs, analyze_rows(rows), strict=True) if not row["suspicious"]]
    for seed in SEEDS:
        full_draws, sampled_indices = bootstrap_summary(pvs, seed)
        filtered_draws = []
        for indices in sampled_indices:
            # Resample rows jointly, then reapply the fixed 10% median rule.
            sample_pvs = [pvs[index] for index in indices]
            flags = classify_outliers(sample_pvs, 0.10)
            retained = [value for value, flag in zip(sample_pvs, flags, strict=True) if not flag]
            filtered_draws.append(statistics.mean(retained) if retained else float("nan"))
        differences = [filtered - full for filtered, full in zip(filtered_draws, full_draws, strict=True)]
        bootstraps.append(
            {
                "seed": seed,
                "replicates": BOOTSTRAP_REPLICATES,
                "all_rows_mean_pv_kpa_l": statistics.mean(pvs),
                "all_rows_sample_sd_pv_kpa_l": statistics.stdev(pvs),
                "all_rows_bootstrap_95_percentile_interval": interval(full_draws),
                "clean_rows_mean_pv_kpa_l": statistics.mean(clean_pvs),
                "clean_rows_sample_sd_pv_kpa_l": statistics.stdev(clean_pvs),
                "clean_rows_bootstrap_95_percentile_interval": interval(filtered_draws),
                "paired_filtered_minus_all_mean_interval": interval(differences),
            }
        )

    result = {
        "description": "Descriptive resampling of these rows; not instrument accuracy or population inference.",
        "n_rows": len(rows),
        "median_pv_kpa_l": statistics.median(pvs),
        "full_sample_mean_pv_kpa_l": statistics.mean(pvs),
        "filtered_mean_pv_kpa_l": statistics.mean(clean_pvs),
        "filtered_minus_full_mean_pv_kpa_l": statistics.mean(clean_pvs) - statistics.mean(pvs),
        "filtered_minus_full_relative_to_filtered_mean": (
            statistics.mean(clean_pvs) - statistics.mean(pvs)
        )
        / statistics.mean(clean_pvs),
        "source_sha256": source_hash,
        "threshold_sweep": sweep,
        "bootstrap": bootstraps,
    }
    output = ROOT / "results" / "hw2" / "analysis.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

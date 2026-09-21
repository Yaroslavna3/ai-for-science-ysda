# Week 1 artifact: environment and first generate-check cycle

## Project

- Topic: educational Boyle-Mariotte law example.
- Project folder: `completed_boyle_project/`.
- Contract/context file: `AGENT.md`.
- Journal: `diary.md`.
- Data: `data/measurements.csv`.

## Environment check

- `git --version`: `git version 2.51.0.windows.1`.
- `python --version`: `Python 3.12.14` from the bundled Codex runtime.
- `ai4science doctor`: not run here because the `ai4science` command is not installed in this machine context and the course Yandex AI Studio credentials are not available in the shared materials.

## Git history

The project was initialized as a git repository.

1. `Начало проекта: AGENT.md и материалы`
2. `Первый цикл: проверка закона Бойля-Мариотта`

## Agent task

Request: compute `p*V` for each row in `data/measurements.csv`, assess whether it is approximately constant at fixed temperature, flag suspicious rows, and provide an independent verification point.

Generated files:

- `src/analyze_boyle.py`
- `results/pv_table.csv`
- `results/summary.json`

## Result

- Median `pV`: 247.8 kPa*l.
- Suspicious row: row 7, `V=2.20` l, `p=1.136` kPa, `pV=2.50` kPa*l, about -99% from the median.
- Clean-data estimate after excluding the suspicious row: `pV=249.3` kPa*l.
- Clean-data relative scatter: 1.1%.

Interpretation: the measurements support Boyle-Mariotte's law after excluding the suspicious row; row 7 likely contains a unit or decimal-place error in pressure.

## Independent verification

External checker:

```powershell
$env:PYTHONIOENCODING='utf-8'
python ..\materials\example_boyle\check_boyle.py .\data\measurements.csv
```

Verified output:

```text
строк: 12; медиана pV = 247.8 кПа·л
ПОДОЗРИТЕЛЬНО: строка 7: V=2.20 л, p=1.136 кПа, pV=2.50 (отклонение -99%) — проверьте единицы
без подозрительных строк: pV = 249.3 кПа·л, относительный разброс 1.1%
```

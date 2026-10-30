# CLAUDE.md — Environmental Economics, Track 2

## Project
Group project (5 people), BSc AIDAMS Environmental Economics.
Question: are climate extremes becoming more frequent/intense, and is that because the whole
distribution has **shifted** or because its **tail has changed shape**? Answer for both
frequency and intensity, and test how much the answer depends on the threshold.

- Paper: max 10 pages incl. figures/tables (excl. references + AI statement). Due **Mon 2 Nov 2026**.
- Presentation: 10 min + 3 min Q&A, **Mon 9 Nov 2026**.
- The result is **descriptive, not causal**. Never write causal claims.

## Roles
- A – Data (done): raw data, data log, §2
- B – Code lead: the reproducible pipeline, summary table, §3
- C – Figures: 5–6 figures max, §4
- D – Tails & econometrics: threshold analysis, trends, quantile regression, §5
- E – Lit & editing: §1, §6, AI statement, final edit

## Repo layout
- `data/raw/` — downloaded CSVs. **Never modify.**
- `data/README.md` — data log (sources, definitions, limitations). Read it before touching data.
- `data/atlas_info_spei6.txt` — verbatim Atlas definition of SPEI-6 (source of the reference period).
- `scripts/check_raw.py` — validates raw files; run it after any data change.
- `scripts/config.py` — periods, thresholds, quantiles, bootstrap settings. Import from here.
- `scripts/analysis.py` — the entry point: `python scripts/analysis.py` writes every result
  to `outputs/`. Other scripts get the data with `load_data.load_analysis_data()`.
- `outputs/` — generated; never edit by hand. Column glossary in `README.md`.
- `tests/` — `python -m pytest`; run after any change to `scripts/`.
- `paper/0X_*.md` — one file per paper section.

## Data (do not re-derive these facts; they are documented)
- Source: Copernicus Interactive Climate Atlas v2.5, dataset **ERA5-Land** (0.1°), accessed 2026-10-29.
- Country averages (cosine-latitude weighted, land cells). Countries: ESP, FRA, GER, SWE.
- `txx_{CTRY}_{JUN,JUL,AUG}.csv`: TXx = monthly max of daily max 2 m temperature, °C.
  Stack Jun/Jul/Aug per country (~90 obs per 30-year period).
- `spei6_{CTRY}_SEP.csv`: SPEI-6, dimensionless, negative = drier. September value covers
  Apr–Sep. Reference period 1971–2005. Country-level SD is 0.75–0.90, not 1.
- All files: 1950–2025, no missing values.
- Load with: `pd.read_csv(path, comment="#")`, then rename columns to `["year", "value"]`.

## Method conventions
- Periods: **TBD by the group** (proposal: 1961–1990 vs 1996–2025, currently set in
  `scripts/config.py`). Define them in ONE place in the code and import everywhere.
- Thresholds: percentiles computed on the **early** period, applied to both periods.
- TXx extremes = upper tail (P75/P90/P95/P99). SPEI extremes = **lower** tail (P25/P10/P5/P1).
- Always report the number of observations behind each tail statistic.
- Shift vs shape headline: compare change in P95 (P5 for SPEI) with change in the mean.
- Trends: OLS with HAC standard errors; quantile regression on time. Report coefficients
  with standard errors, in index units per decade.
- Known limitation: ERA5-Land may be inconsistent before 1978 (Atlas disables trends
  before then). Flag it wherever early-period results are interpreted.

## Rules
- Everything must reproduce from `data/raw/` with one entry-point script. No hand-edited
  numbers, no manual steps.
- Every number in the paper must come from script output. Never type or invent a number.
- Figures: axes labelled with units, coverage and period stated, source given, one-line
  takeaway caption. Each must stand on its own.
- If a fact is not confirmed from the data or a cited source, mark it `[VERIFY]` instead
  of guessing.
- Use pandas, numpy, matplotlib, statsmodels. Keep code readable — every group member must
  be able to explain it in Q&A.
- Git: one branch per task, open a PR, never push directly to `main`.
- Note AI use: tell E what Claude drafted, for the AI statement.

# Data log

All numbers in this file come from the output of `scripts/check_raw.py`
(saved in `data/raw_check.csv`). Re-run the script after any change to
`data/raw/`; files in `data/raw/` are never edited by hand.

```
python scripts/check_raw.py
```

## Common source information

| Item | Value |
|---|---|
| Producer | Copernicus Climate Change Service (C3S) |
| Tool | Copernicus Interactive Climate Atlas, "Regional information" export |
| URL | https://atlas.climate.copernicus.eu/ |
| Atlas version | v2.5 (identical across all 16 files) |
| Underlying dataset | ERA5-Land (identical across all 16 files) |
| Access / download date | 2026-10-29 (file timestamps 2026-10-29T16:11:03.327Z to 2026-10-29T16:20:22.078Z) |
| Countries | Spain (ESP), France (FRA), Germany (GER), Sweden (SWE) |
| Spatial aggregation | Country average of grid-cell values ("Mean of ... series for <country>"), cosine-latitude weighted on the regular lat-lon grid; land cells only (ERA5-Land covers land only) |
| Documentation | C3S Atlas User Guide, https://confluence.ecmwf.int/x/aZZ-Fw (consulted 2026-10-29) |
| Coverage | 1950-2025, 76 years per file, no missing values, no duplicated years, no gaps |

### Raw file format

Each CSV has 5 comment lines starting with `#`:

1. Atlas name (`Copernicus Interactive Climate Atlas - Regional information`)
2. `Version: v2.5`
3. `Generated at: <ISO timestamp, UTC>`
4. `Columns: year, model, value`
5. A quoted description, e.g.
   `"Maximum of daily maximum temperature (°C) - ERA5-Land - Value - 1961-1990 - Mean of june series for Spain"`

followed by the header `Year,0` and one row per year. The column `0` holds
the value.

The string `1961-1990` in the description is the period highlighted in the
Atlas chart. It does not truncate the data: every file covers 1950-2025.

## TXx

- **Definition**: monthly maximum of daily maximum near-surface air
  temperature.
- **Units**: °C.
- **Temporal resolution**: monthly; we downloaded June, July and August,
  one file per month and country (12 files).
- **Coverage**: 1950-2025, 76 values per file.
- **Country average**: the Atlas averages the grid-cell TXx values over the
  country, with cosine-latitude weights, over land cells only. The result is a country mean of local monthly maxima, not the
  hottest grid cell.

## SPEI-6

- **Definition**: Standardised Precipitation-Evapotranspiration Index on a
  6-month accumulation window: precipitation minus potential
  evapotranspiration (PET), accumulated over 6 months and standardised
  against the reference period 1971-2005 (C3S Atlas User Guide, v2.5).
  Expressed in standardised units; negative = drier than the reference,
  positive = wetter.
- **PET method**: Hargreaves formulation (used by the Atlas since v2.0).
- **Units**: dimensionless (the Atlas labels it "fraction of unity").
- **Temporal resolution**: monthly; we downloaded September only (4 files).
  The September value covers April-September.
- **Coverage**: 1950-2025, 76 values per file.
- **Note from the check**: the country-level series have a standard
  deviation below 1 (0.754 to 0.902) and sample means below 0
  (-0.285 to -0.037). The standardisation is done per grid cell over the
  reference period, so a country average over 1950-2025 need not have mean 0
  and SD 1.

## File inventory

Output of `scripts/check_raw.py` (`data/raw_check.csv`). Values rounded to
3 decimals.

| file | index | country | month | units | n_rows | first_year | last_year | missing_values | duplicated_years | min | mean | max | sd | generated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spei6_ESP_SEP.csv | SPEI-6 | Spain | September | fraction of unity | 76 | 1950 | 2025 | 0 | 0 | -1.819 | -0.285 | 2.300 | 0.808 | 2026-10-29T16:19:40.433Z |
| spei6_FRA_SEP.csv | SPEI-6 | France | September | fraction of unity | 76 | 1950 | 2025 | 0 | 0 | -1.984 | -0.275 | 1.246 | 0.858 | 2026-10-29T16:19:53.771Z |
| spei6_GER_SEP.csv | SPEI-6 | Germany | September | fraction of unity | 76 | 1950 | 2025 | 0 | 0 | -2.801 | -0.119 | 1.698 | 0.902 | 2026-10-29T16:20:09.467Z |
| spei6_SWE_SEP.csv | SPEI-6 | Sweden | September | fraction of unity | 76 | 1950 | 2025 | 0 | 0 | -1.987 | -0.037 | 1.558 | 0.754 | 2026-10-29T16:20:22.078Z |
| txx_ESP_AUG.csv | TXx | Spain | August | °C | 76 | 1950 | 2025 | 0 | 0 | 29.813 | 33.809 | 38.175 | 1.775 | 2026-10-29T16:16:39.703Z |
| txx_ESP_JUL.csv | TXx | Spain | July | °C | 76 | 1950 | 2025 | 0 | 0 | 29.724 | 34.103 | 37.879 | 1.485 | 2026-10-29T16:13:30.398Z |
| txx_ESP_JUN.csv | TXx | Spain | June | °C | 76 | 1950 | 2025 | 0 | 0 | 25.089 | 31.320 | 36.031 | 2.328 | 2026-10-29T16:11:03.327Z |
| txx_FRA_AUG.csv | TXx | France | August | °C | 76 | 1950 | 2025 | 0 | 0 | 24.927 | 30.051 | 36.082 | 2.311 | 2026-10-29T16:16:55.748Z |
| txx_FRA_JUL.csv | TXx | France | July | °C | 76 | 1950 | 2025 | 0 | 0 | 26.439 | 30.345 | 36.208 | 2.172 | 2026-10-29T16:13:49.587Z |
| txx_FRA_JUN.csv | TXx | France | June | °C | 76 | 1950 | 2025 | 0 | 0 | 23.874 | 28.159 | 35.054 | 2.535 | 2026-10-29T16:11:58.192Z |
| txx_GER_AUG.csv | TXx | Germany | August | °C | 76 | 1950 | 2025 | 0 | 0 | 24.134 | 28.842 | 33.756 | 2.285 | 2026-10-29T16:17:12.777Z |
| txx_GER_JUL.csv | TXx | Germany | July | °C | 76 | 1950 | 2025 | 0 | 0 | 22.104 | 29.148 | 34.329 | 2.618 | 2026-10-29T16:14:04.015Z |
| txx_GER_JUN.csv | TXx | Germany | June | °C | 76 | 1950 | 2025 | 0 | 0 | 22.930 | 27.699 | 33.600 | 2.135 | 2026-10-29T16:12:19.476Z |
| txx_SWE_AUG.csv | TXx | Sweden | August | °C | 76 | 1950 | 2025 | 0 | 0 | 17.415 | 22.663 | 26.930 | 2.225 | 2026-10-29T16:17:27.021Z |
| txx_SWE_JUL.csv | TXx | Sweden | July | °C | 76 | 1950 | 2025 | 0 | 0 | 19.461 | 24.416 | 29.045 | 2.070 | 2026-10-29T16:14:19.172Z |
| txx_SWE_JUN.csv | TXx | Sweden | June | °C | 76 | 1950 | 2025 | 0 | 0 | 17.203 | 23.079 | 27.361 | 2.273 | 2026-10-29T16:12:36.170Z |

## Known data limitations (from the C3S Atlas User Guide)

Source: C3S Atlas User Guide, https://confluence.ecmwf.int/x/aZZ-Fw
(consulted 2026-10-29).

- **Border cells**: the guide does not document how grid cells that straddle
  a national border are treated in the country average.
- **ERA5-Land before 1978**: the Atlas disables ERA5-Land trends before 1978
  because of a potential inconsistency in the ERA5 forcing used for that
  period. Our sample starts in 1950, so part of any early-vs-recent
  difference could be a data artefact rather than a climate signal.

## TO VERIFY

Remaining open points in `paper/02_data.md` (marked [VERIFY] there).

- [ ] ERA5-Land horizontal resolution (about 9 km).
- [ ] Lower density of the observing network in the early decades of the
      sample.
- [ ] Closing sentence on tail inference: align with the methods section
      (Section 3).
